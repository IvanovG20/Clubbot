from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User


async def get_or_create_user(
    session: AsyncSession,
    tg_id: int,
    club_id: int,
    username: str | None = None,
) -> tuple[User, bool]:

    result = await session.execute(
        select(User).where(
            User.tg_id == tg_id,
            User.club_id == club_id,
        )
    )

    user = result.scalar_one_or_none()

    if user:
        return user, False

    user = User(
        tg_id=tg_id,
        club_id=club_id,
        username=username,
    )

    session.add(user)

    await session.commit()
    await session.refresh(user)

    return user, True
