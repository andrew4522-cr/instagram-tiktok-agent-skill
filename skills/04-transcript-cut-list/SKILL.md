---
name: 04-transcript-cut-list
description: "Feed the raw transcript of recorded footage to generate a frame-by-frame editing cut list: what sentences to cut, where to remove dead air, where to punch-in zoom, and where to overlay B-roll."
metadata:
  version: 1.0.0
  source: "https://github.com/andrew4522-cr/instagram-tiktok-agent-skill"
---

# Skill 04: Transcript-to-Cut-List Editor

Creators burn out because they stare at 10 minutes of raw footage in CapCut or Premiere trying to figure out what to keep.

Give this skill your raw spoken transcript (including fumbles, repeated sentences, and filler words) and it outputs a **ready-to-execute Editing Cut List**.

---

## Editing Rules Applied Automatically

1. **Zero Throat-Clearing:** Any opening sentence containing *"Hey guys"*, *"So today I wanted to talk about"*, or *"Testing one two"* is marked `[HARD_CUT_REMOVE]`.
2. **Duplicate Take Detection:** When a creator repeats a line 2–3 times to get the delivery right, only the cleanest final take is marked `[KEEP]`.
3. **Breath & Pause Stripping:** Instructs the editor to strip all gaps `> 0.15 seconds` between sentences.
4. **Alternating Visual Rhythm:**
   - Beat 1 (`0:00 - 0:03`): `100% -> 112%` fast punch-in zoom + bold hook caption.
   - Even Beats: Insert B-Roll or screen-recording overlay while voiceover continues.
   - Odd Beats: Jump-cut between `100%` medium framing and `110%` tight framing to hide cuts.

---

## CLI Usage

```bash
ig-tiktok-skill --cut-list "Hey guys welcome back. Um so today I want to show you this workflow. A client was spending €4,000 a month on manual reporting. We replaced the entire process in 15 minutes using an automated pipeline. Comment SYSTEM and I will send you the template."
```
