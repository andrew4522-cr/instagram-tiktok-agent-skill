---
name: 05-retention-dropoff-doctor
description: "Analyze viewer retention graphs (3-second hold rate, average watch time, completion rate) and transcripts to pinpoint exactly where viewers swipe away and rewrite the weak beat."
metadata:
  version: 1.0.0
  source: "https://github.com/andrew4522-cr/instagram-tiktok-agent-skill"
---

# Skill 05: Viewer Retention Drop-Off Doctor

Stop guessing why a Reel or TikTok stalled at 300 views. Every retention graph tells a mathematical story across three checkpoints:

---

## The 3 Retention Checkpoints & Fixes

| Checkpoint | Healthy Benchmark | If Below Benchmark, Here Is Why | The Exact Fix |
| :--- | :--- | :--- | :--- |
| **1. 3-Second Hold Rate (`0:00 - 0:03`)** | **`>= 65%`** | Viewers swiped before your first sentence finished due to a static opening frame, missing on-screen text, or slow intro. | Trim the first 1.2s of video, add a 4-word bold banner at `0:00`, and show the finished result in Frame 1. |
| **2. Average Watch Percentage (`0:03 - 0:20`)** | **`>= 50%`** (for 30s video) | Mid-video sag: you stayed on one camera angle for `> 5s` or gave away the answer too early with no open loop. | Add a B-roll / visual change every `3.5s` and hold your best insight until the final 25% of the video. |
| **3. Completion & Loop Rate (`Final 4s`)** | **`>= 30%`** | You telegraphed the ending (*"So yeah, thanks for watching!"*), giving viewers permission to swipe. | Cut the outro completely. End on your final punchline + a 4-word CTA that grammatically flows back into your first word at `0:00`. |

---

## CLI Retention Diagnostics

```bash
# Diagnose a 30s Reel with 52% 3s hold, 38% average watch time, and 18% completion
ig-tiktok-skill --diagnose-retention 52 38 18
```
