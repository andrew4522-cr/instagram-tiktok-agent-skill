import unittest

from instagram_tiktok_skill import (
    HOOK_FORMULAS_21,
    check_cover_and_hook_alignment,
    diagnose_retention_dropoff,
    generate_transcript_cut_list,
    score_shortform_hook,
)


class TestInstagramTiktokAgentSkill(unittest.TestCase):
    def test_21_hook_formulas_present(self):
        self.assertEqual(len(HOOK_FORMULAS_21), 21)

    def test_hook_scorer_grades_strong_vs_weak_hooks(self):
        strong = score_shortform_hook(
            said_hook="Stop spending four thousand euro a month on manual reporting when you can automate it in 15 minutes.",
            seen_visual="Cursor circles €4,000 spreadsheet row then cuts to live automated dashboard",
            text_overlay="€4,000/mo -> €200/mo",
        )
        self.assertGreaterEqual(strong["score"], 85.0)
        self.assertEqual(strong["grade"], "A")

        weak = score_shortform_hook(
            said_hook="Hey guys welcome back to my channel, in today's video I wanted to talk about productivity.",
            seen_visual="",
            text_overlay="",
        )
        self.assertLess(weak["score"], 40.0)
        self.assertEqual(weak["grade"], "D")

    def test_cover_and_hook_alignment_check(self):
        good = check_cover_and_hook_alignment(
            cover_headline="€4,000/mo Manual Reporting Fix",
            cover_visual="Founder pointing at highlighted spreadsheet cell in center 1:1 grid safe zone",
            spoken_hook="A client was spending €4,000 a month on manual reporting until we automated it.",
        )
        self.assertTrue(good["aligned"])

        mismatch = check_cover_and_hook_alignment(
            cover_headline="This cover headline has way too many words and talks about dogs",
            cover_visual="",
            spoken_hook="Here is how to bake sourdough bread at home.",
        )
        self.assertFalse(mismatch["aligned"])
        self.assertGreaterEqual(len(mismatch["issues"]), 2)

    def test_transcript_cut_list_removes_fluff(self):
        raw = (
            "Hey guys welcome back. "
            "A client was spending €4,000 a month on manual reporting. "
            "We replaced the entire process in 15 minutes. "
            "Comment SYSTEM for the free blueprint."
        )
        res = generate_transcript_cut_list(raw)
        self.assertEqual(res["removed_cuts"], 1)
        self.assertEqual(res["kept_beats"], 3)
        self.assertEqual(res["edit_instructions"][0]["action"], "HARD_CUT_REMOVE")

    def test_retention_dropoff_doctor(self):
        diag = diagnose_retention_dropoff(hold_3s_pct=48.0, avg_watch_pct=35.0, completion_pct=15.0)
        self.assertEqual(len(diag["diagnoses"]), 3)
        self.assertEqual(diag["diagnoses"][0]["severity"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()
