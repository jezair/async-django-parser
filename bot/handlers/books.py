from aiogram import Router
from aiogram.types import Message

from services.api_client import get_books

router = Router()


@router.message(lambda message: message.text == "📚 Каталог книг")
async def show_books(message: Message):
    books = await get_books()

    if not books:
        await message.answer("Книги не знайдені.")
        return

    text = "📚 Перші 5 книг:\n\n"

    for book in books[:5]:
        text += (
            f"{book['title']}\n"
            f"💰 {book['price']}\n"
            f"⭐ {book['rating']}\n\n"
        )

    await message.answer(text)