from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_club_tg", "club_id", "tg_id"),
        UniqueConstraint("club_id", "tg_id", name="uq_users_club_tg"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id", ondelete="CASCADE"))
    username: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    club: Mapped["Club"] = relationship(back_populates="users")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="user")
