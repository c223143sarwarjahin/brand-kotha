import enum
import uuid
from typing import Optional, Any
from sqlalchemy import (
    String, Integer, SmallInteger, Text, Enum, ForeignKey, Index, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import UUIDv7PKMixin, TimestampMixin


class ApplicationStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    WITHDRAWN = "WITHDRAWN"


class Application(Base, UUIDv7PKMixin, TimestampMixin):
    __tablename__ = "applications"

    campaign_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    creator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    proposed_rate_bdt: Mapped[int] = mapped_column(Integer, nullable=False)
    pitch_message: Mapped[str] = mapped_column(Text, nullable=False)
    match_score: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    match_breakdown: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, native_enum=False),
        default=ApplicationStatus.PENDING,
        nullable=False
    )
    deliverable_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    revision_count: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)

    # Relationships
    campaign = relationship("Campaign", back_populates="applications")
    creator = relationship("User", back_populates="applications")
    reviews = relationship("Review", back_populates="application", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("campaign_id", "creator_id", name="uq_campaign_creator_single_pitch"),
        Index("idx_apps_campaign_status", "campaign_id", "status"),
        Index("idx_apps_creator", "creator_id", "created_at"),
    )

