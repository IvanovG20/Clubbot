from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from core.models.slot import Slot
from core.models.booking import Booking, BookingStatus
from core.exceptions import SlotNotAvailableError, BookingNotFoundError


async def create_booking(
    session: AsyncSession,
    slot_id: int,
    club_id: int,
    user_id: int,
) -> Booking:
    result = await session.execute(
        select(Slot).where(
            Slot.id == slot_id,
            Slot.club_id == club_id,
        ).with_for_update()
    )
    slot = result.scalar_one_or_none()
    if slot is None or not slot.is_available:
        raise SlotNotAvailableError(f"Слот {slot_id} недоступен")

    booking = Booking(
        club_id=club_id,
        user_id=user_id,
        slot_id=slot_id,
        status=BookingStatus.pending,
    )
    slot.is_available = False

    session.add(booking)
    await session.commit()
    await session.refresh(booking)

    return booking


async def cancel_booking(
    session: AsyncSession,
    slot_id: int,
    club_id: int,
    user_id: int,
    book_id: int,
) -> Booking:
    result = await session.execute(
        select(Booking).options(joinedload(Booking.slot)).with_for_update().where(
            Booking.id == book_id,
            Booking.slot_id == slot_id,
            Booking.club_id == club_id,
            Booking.user_id == user_id,
        )
    )
    book = result.unique().scalar_one_or_none()
    if not book:
        raise BookingNotFoundError("Бронь не найдена")
    if book.status == BookingStatus.cancelled:
        raise BookingNotFoundError("Бронь уже отменена")

    book.status = BookingStatus.cancelled
    book.slot.is_available = True

    await session.commit()
    await session.refresh(book)

    return book


async def get_user_bookings(
    session: AsyncSession,
    user_id: int,
    club_id: int,
) -> list[Booking]:
    result = await session.execute(
        select(Booking).options(joinedload(Booking.slot)).where(
            Booking.club_id == club_id,
            Booking.user_id == user_id,
            Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed]),
        ).order_by(Booking.id.desc())
    )
    return result.unique().scalars().all()
