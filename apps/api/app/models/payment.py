import enum
import uuid
from datetime import datetime
from typing import Optional, Any
from sqlalchemy import (
    String, Integer, DateTime, Enum, ForeignKey, Index, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import UUIDv7PKMixin, TimestampMixin


class PaymentKind(str, enum.Enum):
    MEMBERSHIP = "MEMBERSHIP"
    BOOST_PROFILE = "BOOST_PROFILE"
    BOOST_CAMPAIGN = "BOOST_CAMPAIGN"
    SPONSORED_BANNER = "SPONSORED_BANNER"
    VERIFIED_BADGE = "VERIFIED_BADGE"
    LEAD_FEE = "LEAD_FEE"
    DEAL_COMMISSION = "DEAL_COMMISSION"


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"
    REFUNDED = "REFUNDED"


class Payment(Base, UUIDv7PKMixin, TimestampMixin):
    __tablename__ = "payments"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    kind: Mapped[PaymentKind] = mapped_column(Enum(PaymentKind, native_enum=False), nullable=False)
    item_target_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    amount_bdt: Mapped[int] = mapped_column(Integer, nullable=False)
    gateway_provider: Mapped[str] = mapped_column(String(40), nullable=False)
    gateway_trx_id: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    idempotency_key: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    raw_webhook_payload: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, native_enum=False),
        default=PaymentStatus.PENDING,
        nullable=False
    )
    reviewed_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("gateway_provider", "gateway_trx_id", name="uq_gateway_provider_trx_id"),
        Index("idx_payments_user_status", "user_id", "status", "created_at"),
    )

