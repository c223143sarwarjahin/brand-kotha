"""001_initial_schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-11-03 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="ACTIVE"),
        sa.Column("email_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("phone", name="uq_users_phone"),
    )
    op.create_index("idx_users_role_status", "users", ["role", "status"])

    # 2. profiles
    op.create_table(
        "profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("display_name", sa.String(120), nullable=False),
        sa.Column("handle", sa.String(80), nullable=False),
        sa.Column("niche", sa.String(60), nullable=False),
        sa.Column("platform", sa.String(50), nullable=False),
        sa.Column("followers_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rate_or_budget_bdt", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("portfolio_url", sa.String(500), nullable=True),
        sa.Column("past_work", sa.Text(), nullable=True),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("membership_tier", sa.String(50), nullable=False, server_default="FREE"),
        sa.Column("membership_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("featured_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("avg_rating", sa.Numeric(3, 2), nullable=False, server_default="0.00"),
        sa.Column("review_count", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("handle", name="uq_profiles_handle"),
        sa.CheckConstraint("followers_count >= 0", name="check_positive_followers"),
        sa.CheckConstraint("rate_or_budget_bdt >= 0", name="check_positive_rate"),
    )
    op.create_index("idx_profiles_discovery", "profiles", ["niche", "platform", "rate_or_budget_bdt", sa.text("followers_count DESC")])

    # 3. campaigns
    op.create_table(
        "campaigns",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("brand_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(180), nullable=False),
        sa.Column("category", sa.String(60), nullable=False),
        sa.Column("platform", sa.String(50), nullable=False),
        sa.Column("budget_bdt", sa.Integer(), nullable=False),
        sa.Column("deliverables", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("campaign_type", sa.String(50), nullable=False, server_default="PAID_PROMO"),
        sa.Column("status", sa.String(50), nullable=False, server_default="OPEN"),
        sa.Column("featured_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("budget_bdt >= 0", name="check_positive_budget"),
    )
    op.create_index("idx_campaigns_brand_id", "campaigns", ["brand_id"])
    op.create_index("idx_campaigns_search", "campaigns", ["status", "category", "platform", sa.text("budget_bdt DESC")])

    # 4. applications (pitches)
    op.create_table(
        "applications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("campaign_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False),
        sa.Column("creator_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("proposed_rate_bdt", sa.Integer(), nullable=False),
        sa.Column("pitch_message", sa.Text(), nullable=False),
        sa.Column("match_score", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("match_breakdown", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="PENDING"),
        sa.Column("deliverable_url", sa.String(500), nullable=True),
        sa.Column("revision_count", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("campaign_id", "creator_id", name="uq_campaign_creator_single_pitch"),
    )
    op.create_index("idx_apps_campaign_status", "applications", ["campaign_id", "status"])
    op.create_index("idx_apps_creator", "applications", ["creator_id", sa.text("created_at DESC")])

    # 5. conversations & messages
    op.create_table(
        "conversations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_one_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_two_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("last_message_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("user_one_id < user_two_id", name="check_canonical_user_order"),
        sa.UniqueConstraint("user_one_id", "user_two_id", name="uq_canonical_user_pair"),
    )

    op.create_table(
        "messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sender_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("attachment_url", sa.String(500), nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_messages_conversation", "messages", ["conversation_id"])
    op.create_index("idx_messages_unread", "messages", ["conversation_id", "sender_id"], postgresql_where=sa.text("read_at IS NULL"))

    # 6. reviews
    op.create_table(
        "reviews",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("application_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("applications.id", ondelete="CASCADE"), nullable=False),
        sa.Column("from_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("to_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("stars", sa.SmallInteger(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.Column("is_hidden", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("application_id", "from_user_id", name="uq_one_review_per_side_per_deal"),
        sa.CheckConstraint("stars >= 1 AND stars <= 5", name="check_stars_range"),
        sa.CheckConstraint("from_user_id <> to_user_id", name="check_self_review_prevented"),
    )

    # 7. payments
    op.create_table(
        "payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("kind", sa.String(50), nullable=False),
        sa.Column("item_target_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("amount_bdt", sa.Integer(), nullable=False),
        sa.Column("gateway_provider", sa.String(40), nullable=False),
        sa.Column("gateway_trx_id", sa.String(120), nullable=True),
        sa.Column("idempotency_key", sa.String(120), nullable=False),
        sa.Column("raw_webhook_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="PENDING"),
        sa.Column("reviewed_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("gateway_provider", "gateway_trx_id", name="uq_gateway_provider_trx_id"),
        sa.UniqueConstraint("idempotency_key", name="uq_payment_idempotency_key"),
    )
    op.create_index("idx_payments_user_status", "payments", ["user_id", "status", "created_at"])

    # 8. platform_settings & audit_logs
    op.create_table(
        "platform_settings",
        sa.Column("id", sa.Integer(), primary_key=True, default=1),
        sa.Column("charge_enabled", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("commission_pct", sa.Numeric(4, 2), nullable=False, server_default="10.00"),
        sa.Column("lead_fee_bdt", sa.Integer(), nullable=False, server_default="199"),
        sa.Column("creator_membership_bdt", sa.Integer(), nullable=False, server_default="299"),
        sa.Column("brand_membership_bdt", sa.Integer(), nullable=False, server_default="999"),
        sa.Column("brand_premium_bdt", sa.Integer(), nullable=False, server_default="2499"),
        sa.Column("payment_instructions", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.CheckConstraint("id = 1", name="check_singleton_platform_settings"),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("action", sa.String(60), nullable=False),
        sa.Column("entity_type", sa.String(60), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("diff_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("idx_audit_logs_created_actor", "audit_logs", ["created_at", "actor_id"])


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("platform_settings")
    op.drop_table("payments")
    op.drop_table("reviews")
    op.drop_table("messages")
    op.drop_table("conversations")
    op.drop_table("applications")
    op.drop_table("campaigns")
    op.drop_table("profiles")
    op.drop_table("users")
