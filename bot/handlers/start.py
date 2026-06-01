from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.menu import main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Ласкаво просимо до книжкового магазину!\n\n"
        "Оберіть потрібний пункт меню:",
        reply_markup=main_menu,
    )