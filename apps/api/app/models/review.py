import uuid
from sqlalchemy import (
    Text, SmallInteger, Boolean, ForeignKey, Index, UniqueConstraint, CheckConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.base import UUIDv7PKMixin, TimestampMixin


class Review(Base, UUIDv7PKMixin, TimestampMixin):
    __tablename__ = "reviews"

    application_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    from_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    to_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    stars: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    application = relationship("Application", back_populates="reviews")

    __table_args__ = (
        UniqueConstraint("application_id", "from_user_id", name="uq_one_review_per_side_per_deal"),
        CheckConstraint("stars >= 1 AND stars <= 5", name="check_stars_range"),
        CheckConstraint("from_user_id <> to_user_id", name="check_self_review_prevented"),
    )
