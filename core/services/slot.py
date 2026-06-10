from datetime import date, time, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Slot


async def get_available_dates(session: AsyncSession, club_id: int) -> list[date]:
    """Метод для получения дат, возможных для брони"""

    today = date.today()
    max_date = today + timedelta(days=6)

    result = await session.execute(
        select(Slot.date).distinct().where(
            Slot.is_available == True,
            Slot.club_id == club_id,
            Slot.date >= today,
            Slot.date <= max_date
        ).order_by(Slot.date.asc())
    )
    dates = result.scalars().all()
    return dates


async def get_available_times(session: AsyncSession, club_id: int, book_date: date) -> list[tuple]:

    result = await session.execute(
        select(Slot.time_from, Slot.time_to).distinct().
        where(
            Slot.club_id == club_id,
            Slot.date == book_date,
            Slot.is_available == True,
        ).order_by(Slot.time_from.asc())
    )
    return result.all()


async def get_available_seats(session: AsyncSession, club_id: int, book_date: date, time_from: time, time_to: time) -> list[int]:

    result = await session.execute(
        select(Slot.seat_number).distinct().
        where(
            Slot.club_id == club_id,
            Slot.date == book_date,
            Slot.is_available == True,
            Slot.time_from == time_from,
            Slot.time_to == time_to
        ).order_by(Slot.seat_number)
    )
    return result.scalars().all()