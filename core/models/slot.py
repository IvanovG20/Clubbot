from datetime import date, time

from sqlalchemy import Boolean, Date, ForeignKey, Index, SmallInteger, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base


class Slot(Base):
    __tablename__ = "slots"
    __table_args__ = (Index("ix_slots_club_date", "club_id", "date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id", ondelete="CASCADE"))
    date: Mapped[date] = mapped_column(Date)
    time_from: Mapped[time] = mapped_column(Time)
    time_to: Mapped[time] = mapped_column(Time)
    seat_number: Mapped[int] = mapped_column(SmallInteger)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    club: Mapped["Club"] = relationship(back_populates="slots")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="slot")
