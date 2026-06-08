from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from core.models.slot import Slot
from core.models.booking import Booking, BookingStatus
from core.exceptions import SlotNotAvailableError


async def create_booking(session: AsyncSession,
                         slot_id: int,
                         club_id: int,
                         user_id: int):
    result = await session.execute(
        select(Slot).where(Slot.id == slot_id,
                           Slot.club_id == club_id,
                           )
    )
    slot = result.scalar_one_or_none()
    if slot is None or not slot.is_available:
        raise SlotNotAvailableError(
            f"Слот {slot_id} недоступен"
        )
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


