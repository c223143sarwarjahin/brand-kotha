import unittest
from app.modules.matching.engine import calculate_match_score


class TestMatchingEngine(unittest.TestCase):
    def test_calculate_match_score_exact_match(self):
        # 50 (niche) + 25 (platform) + 25 (exact budget) = 100
        score, reasons = calculate_match_score(
            creator_niche="Beauty",
            creator_platform="INSTAGRAM",
            creator_rate_bdt=10000,
            campaign_category="Beauty",
            campaign_platform="INSTAGRAM",
            campaign_budget_bdt=12000,
        )
        self.assertEqual(score, 100)
        self.assertTrue(reasons["niche_match"])
        self.assertTrue(reasons["platform_match"])
        self.assertEqual(reasons["budget_fit"], "exact")

    def test_calculate_match_score_negotiable_budget(self):
        # 50 (niche) + 25 (platform) + 12 (near budget <= 120%) = 87
        score, reasons = calculate_match_score(
            creator_niche="Tech",
            creator_platform="YOUTUBE",
            creator_rate_bdt=11000,  # exceeds 10,000 by 10% (within 20%)
            campaign_category="Tech",
            campaign_platform="YOUTUBE",
            campaign_budget_bdt=10000,
        )
        self.assertEqual(score, 87)
        self.assertTrue(reasons["niche_match"])
        self.assertTrue(reasons["platform_match"])
        self.assertEqual(reasons["budget_fit"], "near")

    def test_calculate_match_score_mismatched_niche(self):
        # 0 (mismatched niche) + 25 (platform) + 25 (exact budget) = 50
        score, reasons = calculate_match_score(
            creator_niche="Fashion",
            creator_platform="FACEBOOK",
            creator_rate_bdt=5000,
            campaign_category="Fitness",
            campaign_platform="FACEBOOK",
            campaign_budget_bdt=5000,
        )
        self.assertEqual(score, 50)
        self.assertFalse(reasons["niche_match"])
        self.assertTrue(reasons["platform_match"])
        self.assertEqual(reasons["budget_fit"], "exact")

    def test_calculate_match_score_over_budget(self):
        # 50 (niche) + 25 (platform) + 0 (over budget > 120%) = 75
        score, reasons = calculate_match_score(
            creator_niche="Food",
            creator_platform="TIKTOK",
            creator_rate_bdt=20000,  # exceeds 10,000 by 100%
            campaign_category="Food",
            campaign_platform="TIKTOK",
            campaign_budget_bdt=10000,
        )
        self.assertEqual(score, 75)
        self.assertEqual(reasons["budget_fit"], "over_budget")


if __name__ == "__main__":
    unittest.main()
