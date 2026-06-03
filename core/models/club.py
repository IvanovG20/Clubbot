from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base


class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    bot_token: Mapped[str] = mapped_column(String(100), unique=True)
    admin_chat_id: Mapped[int] = mapped_column(BigInteger)
    timezone: Mapped[str] = mapped_column(String(50), default="Europe/Moscow")

    users: Mapped[list["User"]] = relationship(back_populates="club")
    slots: Mapped[list["Slot"]] = relationship(back_populates="club")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="club")
