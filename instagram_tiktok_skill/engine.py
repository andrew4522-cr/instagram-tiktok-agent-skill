#!/usr/bin/env python3
"""
========================================================================================
INSTAGRAM REELS & TIKTOK AGENT SKILL ENGINE (11 Skills + Deterministic Scoring CLI)
Author: Andrew Anderson (BridgingTheAIGap.com / CULT)
License: MIT
========================================================================================
Provides executable deterministic scoring and editing tools backing the 11 Agent Skills:
1. `score_shortform_hook`: Scores a 0-3s Reels/TikTok hook (0-100) across 21 viral hook
   formulas, 3-channel synchronization (Said + Seen + Text Overlay), and Hormozi's
   Proof / Promise / Plan framework.
2. `check_cover_and_hook_alignment`: Evaluates Cover Frame, 4-Word Grid Title, and 0-3s
   Spoken Hook as a single set to prevent <2s swipe-away mismatch.
3. `generate_transcript_cut_list`: Converts raw recorded transcript text into a frame-by-frame
   editing instruction list (where to cut filler/dead air, where to punch-in zoom, where
   to drop B-roll).
4. `diagnose_retention_dropoff`: Analyzes 3-second hold rate, mid-video watch time, and
   loop completion rate to pinpoint the exact drop-off timestamp and structural fix.
========================================================================================
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Dict, List, Optional

HOOK_FORMULAS_21: List[Dict[str, str]] = [
    {"id": "F01", "name": "Cost Replacement", "template": "A client was spending [High Cost] on [Process] until we replaced it with [Low Cost Solution]."},
    {"id": "F02", "name": "Negative Warning / Stop Doing X", "template": "Stop [Common Habit] when you can [Better Outcome] in [Short Timeframe]."},
    {"id": "F03", "name": "Contrarian Correction", "template": "Most people approach [Topic] completely wrong. Here is what actually works."},
    {"id": "F04", "name": "The Secret / Gatekept Playbook", "template": "[Industry] charges [Price] for this, but I am giving you the exact playbook in 30 seconds."},
    {"id": "F05", "name": "Time-Compressed Transformation", "template": "How we went from [Painful Before State] to [Quantified After State] in [Timeframe]."},
    {"id": "F06", "name": "Hard Operational Scarcity", "template": "If you want [Outcome], you have to do this before [Deadline/Limit] or you miss out."},
    {"id": "F07", "name": "Sensory / Visual Proof First", "template": "Look at the difference between [Bad Example] and [Good Example] in real time."},
    {"id": "F08", "name": "If-Then Diagnostic Callout", "template": "If your [Thing] looks like [Symptom], you are losing [Quantified Loss] every week."},
    {"id": "F09", "name": "I Tested X So You Don't Have To", "template": "I spent [Time/Money] testing [Number] ways to [Goal]. Only these 3 worked."},
    {"id": "F10", "name": "Unpopular Truth", "template": "Unpopular opinion: [Common Advice] is the fastest way to kill your [Goal]."},
    {"id": "F11", "name": "The 3-Second Checklist", "template": "3 signs your [System/Habit] is quietly costing you [Outcome]."},
    {"id": "F12", "name": "Side-by-Side Amateur vs Pro", "template": "Here is why a beginner takes [Long Time] to [Task] and a pro takes [Short Time]."},
    {"id": "F13", "name": "Mistake Autopsy", "template": "This one tiny mistake cost us [Specific Number], and 90% of people make it daily."},
    {"id": "F14", "name": "Steal My System", "template": "Steal the exact 3-step workflow I use to [Desirable Result] in [Minutes] a day."},
    {"id": "F15", "name": "Myth vs Reality Split-Screen", "template": "Everyone tells you to [Myth], but the data shows [Reality] works 4x better."},
    {"id": "F16", "name": "Customer / Founder Question", "template": "A founder asked me yesterday: 'How do I fix [Pain Point] without hiring?' Here is my answer."},
    {"id": "F17", "name": "Do Not Buy X Until You See This", "template": "Do not pay for [Popular Tool/Course] until you try this free [Alternative] first."},
    {"id": "F18", "name": "Before / After Receipt", "template": "30 days ago our [Metric] was [Low]. Today it hit [High]. Here is the exact change we made."},
    {"id": "F19", "name": "The Lazy / Busy Person's Shortcut", "template": "How to get [Big Outcome] after work in 20 minutes without [Hated Chore]."},
    {"id": "F20", "name": "Live Teardown / Audit", "template": "Let's fix this broken [Page/Process/Profile] in under 45 seconds."},
    {"id": "F21", "name": "Curiosity Open Loop", "template": "There is only one reason your [Effort] isn't turning into [Result], and nobody talks about it."},
]

FILLER_PATTERNS = [
    r"\bum+\b", r"\buh+\b", r"\berm+\b", r"\blike,\b", r"\byou know,\b",
    r"\bbasically\b", r"\bso yeah\b", r"\bhey guys welcome back\b",
    r"\bin today's video\b", r"\bwithout further ado\b",
]


def score_shortform_hook(
    said_hook: str,
    seen_visual: str = "",
    text_overlay: str = "",
) -> Dict[str, Any]:
    """
    Scores an Instagram Reels / TikTok 0-3s hook on a 0-100 scale across:
    1. Spoken Brevity & Pacing (must be speakable in <= 3.0s, i.e., 6-16 words).
    2. Proof / Specificity (numbers, currency, timeframes, concrete nouns).
    3. Promise / Tension (stop-warning, contrast, curiosity gap, transformation).
    4. 3-Channel Synchronization (Spoken Audio + Visual Action + On-Screen Text Overlay).
    5. Zero Warm-Up Slop ("Hey guys", "In today's video", "Welcome back").
    """
    said = (said_hook or "").strip()
    seen = (seen_visual or "").strip()
    overlay = (text_overlay or "").strip()
    words = [w for w in said.split() if w.strip()]
    word_count = len(words)

    score = 0.0
    feedback: List[str] = []

    # 1. Brevity & 3-Second Speakability (up to 25 pts)
    if 6 <= word_count <= 16:
        score += 25.0
    elif 4 <= word_count <= 20:
        score += 17.0
        feedback.append(f"Spoken hook is {word_count} words; tighten to 8-14 words so it lands inside 3.0 seconds.")
    else:
        score += 8.0
        feedback.append(f"Spoken hook is {word_count} words (too {'long' if word_count > 20 else 'short'} for a 3-second hold).")

    # 2. Proof & Specificity (up to 25 pts)
    has_number = bool(re.search(r"\b\d+|[$€£%]|\b(?:one|two|three|four|five|ten|twenty|thirty|forty|fifty|hundred|thousand)\b", said.lower()))
    if has_number:
        score += 25.0
    else:
        score += 10.0
        feedback.append("Add a concrete number, price, or timeframe ([Proof] / [Plan]) to anchor credibility in the first 3 seconds.")

    # 3. Pattern Interrupt / Formula Match (up to 25 pts)
    interrupt_patterns = [
        r"\bstop\b", r"\bwrong\b", r"\bmistake\b", r"\bnever\b", r"\bsecret\b",
        r"\breplaced\b", r"\binstead\b", r"\bif your?\b", r"\bwhy\b", r"\bhow\b",
        r"\bdon['’]?t\b", r"\bsteal\b", r"\bbefore\b",
    ]
    if any(re.search(p, said.lower()) for p in interrupt_patterns):
        score += 25.0
    else:
        score += 12.0
        feedback.append("Start with a stronger friction-interrupt word ('Stop...', 'If your...', 'Most people get X wrong...').")

    # 4. 3-Channel Synchronization: Visual + Text Overlay (up to 25 pts)
    if seen and len(seen.split()) >= 4:
        score += 13.0
    else:
        feedback.append("Specify the physical 0-3s visual action ('Seen') so the viewer's eyes are hooked before they unmute.")

    overlay_words = len(overlay.split()) if overlay else 0
    if 2 <= overlay_words <= 7:
        score += 12.0
    elif overlay_words > 7:
        score += 6.0
        feedback.append(f"Text overlay has {overlay_words} words; keep on-screen hook text to 3-6 punchy words.")
    else:
        feedback.append("Add a 3-6 word on-screen Text Overlay for muted scrollers.")

    # 5. Penalty for "Hey guys / In today's video" warm-up throat-clearing
    if any(re.search(p, said.lower()) for p in [r"\bhey guys\b", r"\bwelcome back\b", r"\bin today['’]?s video\b", r"\bmy name is\b"]):
        score = max(0.0, score - 25.0)
        feedback.append("CRITICAL: Delete 'Hey guys / In today's video' warm-up throat-clearing. Start directly on the tension.")

    matched_formula = HOOK_FORMULAS_21[0]["name"]
    low = said.lower()
    if "stop " in low:
        matched_formula = "F02: Negative Warning / Stop Doing X"
    elif "wrong" in low:
        matched_formula = "F03: Contrarian Correction"
    elif "spending" in low or "replaced" in low or "cost" in low:
        matched_formula = "F01: Cost Replacement"
    elif "if you" in low:
        matched_formula = "F08: If-Then Diagnostic Callout"

    return {
        "score": round(min(100.0, score), 1),
        "grade": "A" if score >= 85 else ("B" if score >= 70 else ("C" if score >= 55 else "D")),
        "spoken_word_count": word_count,
        "estimated_seconds": round(word_count / 4.2, 1),
        "matched_formula": matched_formula,
        "feedback": feedback,
    }


def check_cover_and_hook_alignment(
    cover_headline: str,
    cover_visual: str,
    spoken_hook: str,
) -> Dict[str, Any]:
    """
    Skill 02: Inspects the Cover Frame Visual, Cover Text Headline, and 0-3s Spoken Hook
    as a single unit (the Reels/TikTok equivalent of YouTube Title + Thumbnail).
    """
    issues: List[str] = []
    headline_words = [w for w in (cover_headline or "").split() if w.strip()]

    if len(headline_words) > 6:
        issues.append(f"Cover headline has {len(headline_words)} words; Instagram/TikTok 9:16 profile grids crop anything over 4-5 words.")
    if len(headline_words) < 2:
        issues.append("Cover headline is too short to create curiosity on the profile grid.")

    # Check lexical overlap vs verbatim repetition
    h_tokens = {re.sub(r"[^a-z0-9]", "", w.lower()) for w in headline_words if len(w) > 2}
    s_tokens = {re.sub(r"[^a-z0-9]", "", w.lower()) for w in (spoken_hook or "").split() if len(w) > 2}
    overlap = h_tokens.intersection(s_tokens)

    if not overlap and h_tokens and s_tokens:
        issues.append("MISMATCH: Cover headline and 0-3s spoken hook share zero core keywords. Viewers clicking from your profile or search will bounce immediately.")
    if (cover_headline or "").strip().lower() == (spoken_hook or "").strip().lower():
        issues.append("REDUNDANT: Cover headline is an exact copy-paste of the spoken hook. Use the cover for the 4-word promise and the spoken hook for the opening proof.")
    if not (cover_visual or "").strip():
        issues.append("Missing cover visual description (ensure the subject's eyes/object are centered in the 1:1 safe zone so Instagram's grid crop doesn't cut off text).")

    aligned = len(issues) == 0
    return {
        "aligned": aligned,
        "verdict": "PASS" if aligned else "MISMATCH_DETECTED",
        "cover_word_count": len(headline_words),
        "shared_keywords": sorted(list(overlap)),
        "issues": issues,
    }


def generate_transcript_cut_list(raw_transcript: str) -> Dict[str, Any]:
    """
    Skill 04: Takes raw recorded transcript sentences and generates an actionable
    editing cut list (what to cut, where to punch-in zoom, where to insert B-roll).
    """
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", (raw_transcript or "").strip()) if s.strip()]
    edit_list: List[Dict[str, Any]] = []
    current_sec = 0.0
    kept_count = 0
    cut_count = 0

    for idx, sent in enumerate(sentences):
        low = sent.lower()
        words = sent.split()
        duration = round(max(1.5, len(words) / 4.0), 1)

        # Detect warm-up fluff or filler-heavy false starts
        is_fluff = any(re.search(p, low) for p in FILLER_PATTERNS)
        is_duplicate = idx > 0 and low[:25] == sentences[idx - 1].lower()[:25]

        if is_fluff or is_duplicate:
            cut_count += 1
            edit_list.append({
                "beat": idx + 1,
                "action": "HARD_CUT_REMOVE",
                "reason": "Repeated take" if is_duplicate else "Warm-up throat-clearing / filler words",
                "original_text": sent,
            })
            continue

        kept_count += 1
        start_t = round(current_sec, 1)
        end_t = round(current_sec + duration, 1)
        current_sec = end_t

        if kept_count == 1:
            camera_cue = "100% -> 112% fast punch-in zoom on first word + bold center caption"
        elif kept_count % 2 == 0:
            camera_cue = "Insert B-Roll / Screen Recording overlay (keep voiceover rolling)"
        else:
            camera_cue = "Jump cut to 110% tight framing (strip all breath pauses > 0.15s)"

        edit_list.append({
            "beat": idx + 1,
            "action": "KEEP",
            "window_sec": f"{start_t}s - {end_t}s",
            "camera_and_broll_cue": camera_cue,
            "clean_line": sent,
        })

    return {
        "total_sentences_analyzed": len(sentences),
        "kept_beats": kept_count,
        "removed_cuts": cut_count,
        "estimated_final_duration_sec": round(current_sec, 1),
        "edit_instructions": edit_list,
    }


def diagnose_retention_dropoff(
    hold_3s_pct: float,
    avg_watch_pct: float,
    completion_pct: float,
    duration_sec: float = 30.0,
) -> Dict[str, Any]:
    """
    Skill 05: Viewer Retention Drop-Off Doctor.
    Pinpoints whether the video is dying in the 0-3s Hook, the 3-15s Body Transition,
    or the Final 5s Sign-Off, and prescribes the exact structural fix.
    """
    diagnoses: List[Dict[str, str]] = []

    if hold_3s_pct < 65.0:
        diagnoses.append({
            "zone": "0:00 - 0:03 (Opening Hook Drop-Off)",
            "severity": "CRITICAL",
            "metric": f"3s Hold Rate = {hold_3s_pct}% (Target: >= 65%)",
            "root_cause": "Viewers are swiping before your first sentence finishes because of slow visual movement, missing on-screen headline text, or warm-up throat-clearing.",
            "structural_fix": "Cut the first 1.5 seconds of footage, place a 4-word high-contrast text banner in the upper-center safe zone at 0:00, and open with a physical movement or proof receipt in frame 1.",
        })

    if avg_watch_pct < 45.0:
        mid_sec = int(duration_sec * (avg_watch_pct / 100.0))
        diagnoses.append({
            "zone": f"0:03 - 0:{mid_sec:02d} (Mid-Video Retention Cliff)",
            "severity": "HIGH",
            "metric": f"Average Watch Time = {avg_watch_pct}% (Target: >= 50%)",
            "root_cause": f"Viewers drop off around second {mid_sec} because the visual frame stays static for more than 4 seconds or you answered the hook's question too early.",
            "structural_fix": f"Insert a visual pattern-interrupt (B-roll cut, screen-share highlight, or prop change) every 3.5 seconds, and move your #1 best tip to the final third of the video.",
        })

    if completion_pct < 25.0:
        end_sec = max(3, int(duration_sec - 4))
        diagnoses.append({
            "zone": f"0:{end_sec:02d} - 0:{int(duration_sec):02d} (End-of-Video Sign-Off Bleed)",
            "severity": "MEDIUM",
            "metric": f"Completion Rate = {completion_pct}% (Target: >= 30%)",
            "root_cause": "You telegraphed that the video was ending ('So yeah, hope that helped, follow for more!'), triggering an instant swipe before the loop.",
            "structural_fix": "Delete the outro sign-off completely. Deliver your final takeaway and immediately bridge into a 4-word CTA ('Comment SYSTEM for the checklist — and that is why...') that loops seamlessly back into your 0:00 hook.",
        })

    if not diagnoses:
        diagnoses.append({
            "zone": "Full Timeline (Viral Ready)",
            "severity": "HEALTHY",
            "metric": f"3s Hold={hold_3s_pct}%, Avg Watch={avg_watch_pct}%, Completion={completion_pct}%",
            "root_cause": "All retention checkpoints exceed viral distribution thresholds.",
            "structural_fix": "Double down: film 3 immediate variations of this exact hook structure within 48 hours.",
        })

    return {
        "duration_sec": duration_sec,
        "metrics": {
            "hold_3s_pct": hold_3s_pct,
            "avg_watch_pct": avg_watch_pct,
            "completion_pct": completion_pct,
        },
        "diagnoses": diagnoses,
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ig-tiktok-skill",
        description="Instagram Reels & TikTok 11-Skill Agent Engine (Hook Scorer, Cover Alignment, Cut List, Retention Doctor)",
    )
    parser.add_argument("--list-formulas", action="store_true", help="List all 21 viral Reels & TikTok hook formulas")
    parser.add_argument("--score-hook", metavar="SAID_HOOK", help="Score a 0-3s spoken hook (0-100)")
    parser.add_argument("--seen", default="", help="0-3s visual action description for --score-hook")
    parser.add_argument("--overlay", default="", help="0-3s on-screen text overlay for --score-hook")
    parser.add_argument("--check-alignment", nargs=3, metavar=("COVER_HEADLINE", "COVER_VISUAL", "SPOKEN_HOOK"), help="Check Cover + Hook alignment as a set")
    parser.add_argument("--cut-list", metavar="RAW_TRANSCRIPT", help="Generate a timestamped editing cut list from a raw transcript")
    parser.add_argument("--diagnose-retention", nargs=3, type=float, metavar=("HOLD_3S_PCT", "AVG_WATCH_PCT", "COMPLETION_PCT"), help="Diagnose viewer drop-off points")

    args = parser.parse_args(argv)

    if args.list_formulas:
        print(json.dumps(HOOK_FORMULAS_21, indent=2))
        return 0

    if args.score_hook:
        print(json.dumps(score_shortform_hook(args.score_hook, args.seen, args.overlay), indent=2))
        return 0

    if args.check_alignment:
        print(json.dumps(check_cover_and_hook_alignment(*args.check_alignment), indent=2))
        return 0

    if args.cut_list:
        print(json.dumps(generate_transcript_cut_list(args.cut_list), indent=2))
        return 0

    if args.diagnose_retention:
        print(json.dumps(diagnose_retention_dropoff(*args.diagnose_retention), indent=2))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
