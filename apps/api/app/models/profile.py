import enum
import uuid
from datetime import datetime
from typing import Optional
from decimal import Decimal
from sqlalchemy import (
    String, Text, Integer, Numeric, Boolean, DateTime,
    Enum, ForeignKey, Index, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class PlatformEnum(str, enum.Enum):
    INSTAGRAM = "INSTAGRAM"
    FACEBOOK = "FACEBOOK"
    YOUTUBE = "YOUTUBE"
    TIKTOK = "TIKTOK"


class MembershipTier(str, enum.Enum):
    FREE = "FREE"
    CREATOR_MONTHLY = "CREATOR_MONTHLY"
    BRAND_MONTHLY = "BRAND_MONTHLY"
    BRAND_PREMIUM = "BRAND_PREMIUM"


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    handle: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    niche: Mapped[str] = mapped_column(String(60), nullable=False)
    platform: Mapped[PlatformEnum] = mapped_column(Enum(PlatformEnum, native_enum=False), nullable=False)
    followers_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rate_or_budget_bdt: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    portfolio_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    past_work: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Monetization fields
    membership_tier: Mapped[MembershipTier] = mapped_column(
        Enum(MembershipTier, native_enum=False),
        default=MembershipTier.FREE,
        nullable=False
    )
    membership_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    featured_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Review Aggregates
    avg_rating: Mapped[Decimal] = mapped_column(Numeric(3, 2), default=Decimal("0.00"), nullable=False)
    review_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    user = relationship("User", back_populates="profile")

    __table_args__ = (
        CheckConstraint("followers_count >= 0", name="check_positive_followers"),
        CheckConstraint("rate_or_budget_bdt >= 0", name="check_positive_rate"),
        Index("idx_profiles_discovery", "niche", "platform", "rate_or_budget_bdt", followers_count.desc()),
    )

