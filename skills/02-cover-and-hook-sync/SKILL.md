---
name: 02-cover-and-hook-sync
description: "Inspect and align the Reels/TikTok Grid Cover Frame, 4-Word Cover Headline, and 0-3s Spoken Hook as a single set so viewers never bounce from cover-to-video mismatch."
metadata:
  version: 1.0.0
  source: "https://github.com/andrew4522-cr/instagram-tiktok-agent-skill"
---

# Skill 02: Cover & Hook Sync (The Short-Form "Title & Thumbnail" Check)

Videos where the **Grid Cover / Opening Frame** and the **Spoken Hook** don't match are the #1 silent killer of Instagram Reels and TikTok accounts. Never write or review them separately—always inspect them as a single unit.

---

## The 4 Alignment Rules

1. **The 4-Word Grid Crop Rule:**
   - Instagram profile grids crop 9:16 Reels into a centered `1:1` (or `4:5`) box. Any cover headline longer than 4 to 5 words or placed near the top/bottom edges gets cut off.
2. **Complement, Never Repeat:**
   - **Bad (Verbatim Repeat):** Cover says *"How To Save 4 Hours"* and Spoken Hook says *"How to save 4 hours."*
   - **Good (Promise + Immediate Proof):** Cover says *"€4,000/mo -> €200/mo"* while Spoken Hook says *"A client was spending four thousand euro a month on manual reporting until we replaced it with this 15-minute workflow."*
3. **Visual Promise Match:**
   - If the cover promises a tool, spreadsheet, recipe, or physical result, that exact object must be visible in Frame 1 (`0:00`)—not hidden at `0:18` after a 15-second talking-head intro.
4. **Safe-Zone Placement:**
   - Keep all on-screen hook text out of the bottom 25% (covered by caption/music ticker) and right 15% (covered by like/comment/share buttons).

---

## CLI Verification

```bash
ig-tiktok-skill --check-alignment \
  "€4,000/mo to €200/mo" \
  "Founder pointing at highlighted €4,000 spreadsheet row in center 1:1 safe zone" \
  "A client was spending four thousand euro a month on manual reporting until we automated it."
```
