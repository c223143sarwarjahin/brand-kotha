import enum
import uuid
from datetime import datetime
from typing import Optional, Any
from sqlalchemy import (
    String, Integer, DateTime, Enum, ForeignKey, Index, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import UUIDv7PKMixin, TimestampMixin
from app.models.profile import PlatformEnum


class CampaignType(str, enum.Enum):
    PAID_PROMO = "PAID_PROMO"
    PR_BARTER = "PR_BARTER"
    UGC = "UGC"


class CampaignStatus(str, enum.Enum):
    OPEN = "OPEN"
    PAUSED = "PAUSED"
    CLOSED = "CLOSED"
    COMPLETED = "COMPLETED"


class Campaign(Base, UUIDv7PKMixin, TimestampMixin):
    __tablename__ = "campaigns"

    brand_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    category: Mapped[str] = mapped_column(String(60), nullable=False)
    platform: Mapped[PlatformEnum] = mapped_column(Enum(PlatformEnum, native_enum=False), nullable=False)
    budget_bdt: Mapped[int] = mapped_column(Integer, nullable=False)
    deliverables: Mapped[Any] = mapped_column(JSONB, nullable=False, default=list)
    campaign_type: Mapped[CampaignType] = mapped_column(
        Enum(CampaignType, native_enum=False),
        default=CampaignType.PAID_PROMO,
        nullable=False
    )
    status: Mapped[CampaignStatus] = mapped_column(
        Enum(CampaignStatus, native_enum=False),
        default=CampaignStatus.OPEN,
        nullable=False
    )
    featured_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    brand = relationship("User", back_populates="campaigns")
    applications = relationship("Application", back_populates="campaign", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("budget_bdt >= 0", name="check_positive_budget"),
        Index("idx_campaigns_search", "status", "category", "platform", budget_bdt.desc()),
    )

