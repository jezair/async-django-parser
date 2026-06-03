from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Каталог книг")],
        [KeyboardButton(text="🛒 Кошик")],
        [KeyboardButton(text="❓ Допомога")],
    ],
    resize_keyboard=True
)