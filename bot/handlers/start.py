from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router(name="start")


@start_router.message(CommandStart())
async def handle_start(message: Message) -> None:
    """Handle /start command."""
    await message.answer(
        f"Привет, <b>{message.from_user.full_name}</b>!\n\n"
        "Добро пожаловать в ClubBot."
    )
