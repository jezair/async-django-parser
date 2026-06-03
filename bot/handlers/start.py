from aiogram import Router, types
from keyboards.main_kb import main_keyboard

router = Router()

@router.message(lambda message: message.text == "/start")
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Вітаю! Я бот-магазин книг.\n\n"
        "Оберіть дію з меню нижче:",
        reply_markup=main_keyboard
    )