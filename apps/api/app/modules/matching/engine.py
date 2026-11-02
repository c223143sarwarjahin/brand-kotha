from typing import Dict, Any, Tuple


def calculate_match_score(
    creator_niche: str,
    creator_platform: str,
    creator_rate_bdt: int,
    campaign_category: str,
    campaign_platform: str,
    campaign_budget_bdt: int,
) -> Tuple[int, Dict[str, Any]]:
    """
    Deterministic 100-Point Match Score Formula (PRD Section 8.1 & TRD Section 10):
    - Niche Alignment (50 Points): Full +50 if lowercase niche matches lowercase campaign category; 0 otherwise.
    - Platform Alignment (25 Points): Full +25 if platforms match; 0 otherwise.
    - Budget & Rate Fit (25 Points):
        * Full +25 if creator.rate <= campaign.budget
        * Partial +12 if creator.rate <= campaign.budget * 1.20 (within 20% negotiable threshold)
        * 0 otherwise
    """
    # 1. Niche Alignment (50 Points)
    niche_pts = 50 if creator_niche.strip().lower() == campaign_category.strip().lower() else 0

    # 2. Platform Alignment (25 Points)
    platform_pts = 25 if creator_platform.strip().upper() == campaign_platform.strip().upper() else 0

    # 3. Budget & Rate Fit (25 Points)
    if creator_rate_bdt <= campaign_budget_bdt:
        budget_pts = 25
        budget_fit_label = "exact"
    elif creator_rate_bdt <= int(campaign_budget_bdt * 1.20):
        budget_pts = 12
        budget_fit_label = "near"
    else:
        budget_pts = 0
        budget_fit_label = "over_budget"

    total = niche_pts + platform_pts + budget_pts

    reasons = {
        "niche_match": niche_pts == 50,
        "platform_match": platform_pts == 25,
        "budget_fit": budget_fit_label,
        "breakdown": {
            "niche_pts": niche_pts,
            "platform_pts": platform_pts,
            "budget_pts": budget_pts,
        }
    }

    return total, reasons
