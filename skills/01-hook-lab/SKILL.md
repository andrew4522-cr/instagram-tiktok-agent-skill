---
name: 01-hook-lab
description: "Generate and score 0-3 second Instagram Reels and TikTok hooks using 21 proven short-form formulas and the 3-Channel Synchronization framework (Said + Seen + Text Overlay)."
metadata:
  version: 1.0.0
  source: "https://github.com/andrew4522-cr/instagram-tiktok-agent-skill"
---

# Skill 01: Hook Lab (21 Hook Formulas & 0-100 Scorer)

On Instagram Reels and TikTok, you do not have 15 seconds to warm up. You have **1.7 to 3.0 seconds** before the viewer's thumb swipes up.

Every hook must synchronize **three channels at the exact same millisecond (0:00)** and include **Proof**, **Promise**, and **Plan**:
1. **SAID (Spoken Audio):** 8 to 14 words max. Zero "Hey guys" or throat-clearing.
2. **SEEN (Physical / Visual Action):** High-contrast movement, side-by-side comparison, or proof receipt in Frame 1.
3. **TEXT OVERLAY (On-Screen Hook Banner):** 3 to 6 bold words in the upper-center safe zone for muted scrollers.

---

## The 21 Viral Short-Form Hook Formulas

1. **Cost Replacement:** *"A client was spending [High Cost] on [Process] until we replaced it with [Low Cost Solution]."*
2. **Negative Warning:** *"Stop [Common Habit] when you can [Better Outcome] in [Short Timeframe]."*
3. **Contrarian Correction:** *"Most people approach [Topic] completely wrong. Here is what actually works."*
4. **The Gatekept Playbook:** *"[Industry] charges [Price] for this, but here is the exact playbook in 30 seconds."*
5. **Time-Compressed Transformation:** *"How we went from [Painful Before] to [Quantified After] in [Timeframe]."*
6. **Hard Operational Scarcity:** *"If you want [Outcome], do this before [Deadline/Limit] or you miss out."*
7. **Sensory / Visual Proof First:** *"Look at the difference between [Bad Example] and [Good Example] in real time."*
8. **If-Then Diagnostic Callout:** *"If your [Thing] looks like [Symptom], you are losing [Quantified Loss] every week."*
9. **I Tested X So You Don't Have To:** *"I spent [Time/Money] testing [Number] ways to [Goal]. Only these 3 worked."*
10. **Unpopular Truth:** *"Unpopular opinion: [Common Advice] is the fastest way to kill your [Goal]."*
11. **The 3-Second Checklist:** *"3 signs your [System/Habit] is quietly costing you [Outcome]."*
12. **Amateur vs. Pro Split:** *"Here is why a beginner takes [Long Time] to [Task] and a pro takes [Short Time]."*
13. **Mistake Autopsy:** *"This one tiny mistake cost us [Specific Number], and 90% of people make it daily."*
14. **Steal My System:** *"Steal the exact 3-step workflow I use to [Desirable Result] in [Minutes] a day."*
15. **Myth vs. Reality:** *"Everyone tells you to [Myth], but the data shows [Reality] works 4x better."*
16. **Real Question Answered:** *"A client asked me yesterday: 'How do I fix [Pain Point] without [Cost]?' Here is the answer."*
17. **Do Not Buy X Until You See This:** *"Do not pay for [Popular Tool/Course] until you try this free [Alternative] first."*
18. **Before / After Receipt:** *"30 days ago our [Metric] was [Low]. Today it hit [High]. Here is the one change we made."*
19. **The Busy Person's Shortcut:** *"How to get [Big Outcome] after work in 20 minutes without [Hated Chore]."*
20. **Live Teardown / Audit:** *"Let's fix this broken [Page/Process/Habit] in under 45 seconds."*
21. **Curiosity Open Loop:** *"There is only one reason your [Effort] isn't turning into [Result], and nobody talks about it."*

---

## CLI Hook Scoring

```bash
ig-tiktok-skill --score-hook "Stop spending four thousand euro a month on manual reporting when you can automate it in 15 minutes." \
  --seen "Cursor circles €4,000 spreadsheet cell then cuts to live automated dashboard" \
  --overlay "€4,000/mo -> €200/mo"
```
