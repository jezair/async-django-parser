from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📚 Каталог книг"),
            KeyboardButton(text="🛒 Кошик"),
        ],
        [
            KeyboardButton(text="📦 Мої замовлення"),
            KeyboardButton(text="❓ Допомога"),
        ]
    ],
    resize_keyboard=True,
)