from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def catalog_keyboard(page: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️", callback_data=f"page_{page-1}"),
                InlineKeyboardButton(text=f"{page}", callback_data="noop"),
                InlineKeyboardButton(text="➡️", callback_data=f"page_{page+1}"),
            ]
        ]
    )