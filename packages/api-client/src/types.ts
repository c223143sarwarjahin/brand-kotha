/**
 * Core Type Definitions for BrandKotha API
 * Derived from BrandKotha PRD & TRD v2.0
 */

export type UserRole = "CREATOR" | "BRAND" | "ADMIN";
export type UserStatus = "ACTIVE" | "SUSPENDED" | "PENDING_VERIFICATION";

export type SocialPlatform = "INSTAGRAM" | "FACEBOOK" | "YOUTUBE" | "TIKTOK";
export type MembershipTier = "FREE" | "CREATOR_MONTHLY" | "BRAND_MONTHLY" | "BRAND_PREMIUM";

export type CampaignType = "PAID_PROMO" | "PR_BARTER" | "UGC";
export type CampaignStatus = "OPEN" | "PAUSED" | "CLOSED" | "COMPLETED";

export type ApplicationStatus = "PENDING" | "ACCEPTED" | "DECLINED" | "WITHDRAWN";

export interface UserProfile {
  id: string;
  display_name: string;
  handle: string;
  niche: string;
  platform: SocialPlatform;
  followers_count: number;
  rate_or_budget_bdt: number;
  bio?: string;
  portfolio_url?: string;
  past_work?: string;
  is_verified: boolean;
  membership_tier: MembershipTier;
  avg_rating: number;
  review_count: number;
}

export interface CampaignBrief {
  id: string;
  brand_id: string;
  title: string;
  category: string;
  platform: SocialPlatform;
  budget_bdt: number;
  deliverables: Array<{ title: string; format: string }>;
  campaign_type: CampaignType;
  status: CampaignStatus;
  match_score?: number;
  created_at: string;
}

export interface MatchScoreResult {
  score: number;
  reasons: {
    niche_match: boolean;
    platform_match: boolean;
    budget_fit: "exact" | "near" | "over_budget";
    breakdown: {
      niche_pts: number;
      platform_pts: number;
      budget_pts: number;
    };
  };
}

