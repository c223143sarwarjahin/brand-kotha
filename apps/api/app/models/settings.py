import uuid
from typing import Optional, Any
from decimal import Decimal
from sqlalchemy import (
    String, Integer, Numeric, Boolean, Index, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import UUIDv7PKMixin, TimestampMixin


class PlatformSettings(Base):
    __tablename__ = "platform_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    charge_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    commission_pct: Mapped[Decimal] = mapped_column(Numeric(4, 2), default=Decimal("10.00"), nullable=False)
    lead_fee_bdt: Mapped[int] = mapped_column(Integer, default=199, nullable=False)
    creator_membership_bdt: Mapped[int] = mapped_column(Integer, default=299, nullable=False)
    brand_membership_bdt: Mapped[int] = mapped_column(Integer, default=999, nullable=False)
    brand_premium_bdt: Mapped[int] = mapped_column(Integer, default=2499, nullable=False)
    payment_instructions: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        CheckConstraint("id = 1", name="check_singleton_platform_settings"),
    )


class AuditLog(Base, UUIDv7PKMixin, TimestampMixin):
    __tablename__ = "audit_logs"

    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(60), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(60), nullable=False)
    entity_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    diff_json: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)

    __table_args__ = (
        Index("idx_audit_logs_created_actor", "created_at", "actor_id"),
    )

