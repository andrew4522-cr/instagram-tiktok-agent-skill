import unittest

from instagram_tiktok_skill import (
    HOOK_FORMULAS_21,
    check_cover_and_hook_alignment,
    diagnose_retention_dropoff,
    generate_carousel_deck,
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

    def test_carousel_architect_generates_8_slides(self):
        deck = generate_carousel_deck(
            topic="Valencia Singles Retreat",
            hook_headline="24 Vetted Singles. 1 Spanish Estate. 72 Hours.",
            rehook_slide2="Why 75% of Applicants Are Rejected Before Getting the Villa Address",
            value_points=[
                "Strict Vetting: ID check + 12-minute Zoom vibe check locks 12 men & 12 women.",
                "Private Suites: Choose Solo En-Suite, Twin En-Suite, or Boutique Annex.",
                "Day 1 Phones Off: Phones go into a wooden lockbox at sunset tapas.",
                "Day 2 Thermal Springs: 25C Montanejos canyon waters trigger 2.4x attraction.",
                "Day 3 Real Chemistry: 38% rebook or refer a friend within 30 days.",
            ],
            cta_keyword="VILLA",
        )
        self.assertEqual(deck["slide_count"], 8)
        self.assertEqual(deck["save_ability_score"], 100.0)
        self.assertTrue(deck["instagram_second_impression_ready"])
        self.assertTrue(deck["tiktok_photo_mode_pacing_ok"])
        self.assertEqual(deck["cta_keyword"], "VILLA")


if __name__ == "__main__":
    unittest.main()
