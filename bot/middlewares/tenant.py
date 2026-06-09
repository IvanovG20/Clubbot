from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from sqlalchemy import select

from core.database import async_session_factory
from core.models.club import Club


class TenantMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, dict], Awaitable[Any]],
        event: Any,
        data: dict,
    ) -> Any:

        bot = data.get("bot")

        if bot is None:
            return await handler(event, data)

        async with async_session_factory() as session:
            result = await session.execute(
                select(Club).where(
                    Club.bot_token == bot.token
                )
            )

            club = result.scalar_one_or_none()

        # Если клуб не найден — игнорируем сообщение
        if club is None:
            return

        data["club_id"] = club.id

        return await handler(event, data)
