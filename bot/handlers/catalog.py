from aiogram import Router, types
from services.api_client import get_books
from states.cart import user_carts
from states.pagination import user_pages
from keyboards.catalog_kb import catalog_keyboard

router = Router()

@router.message(lambda m: m.text == "📚 Каталог книг")
async def catalog_handler(message: types.Message):
    user_id = message.from_user.id

    page = user_pages.get(user_id, 1)
    data = await get_books(page=page)

    for book in data["results"]:
        kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="➕ Додати до кошика",
                        callback_data=f"add_{book['id']}"
                    )
                ]
            ]
        )

        await message.answer(
            f"📖 {book['title']}\n"
            f"💰 {book['price']}$\n"
            f"⭐ {book['rating']}\n"
            f"📦 {'Є в наявності' if book['availability'] else 'Немає'}",
            reply_markup=kb
        )

    await message.answer(
        f"📄 Сторінка {page}",
        reply_markup=catalog_keyboard(page)
    )



@router.callback_query(lambda c: c.data.startswith("add_"))
async def add_to_cart(callback: types.CallbackQuery):
    book_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    if user_id not in user_carts:
        user_carts[user_id] = []

    user_carts[user_id].append(book_id)

    await callback.answer("Додано до кошика ✅")


@router.message(lambda message: message.text == "🛒 Кошик")
async def cart_handler(message: types.Message):
    cart = user_carts.get(message.from_user.id, [])

    if not cart:
        await message.answer("🛒 Ваш кошик порожній")
        return

    text = "🛒 Ваш кошик:\n\n"

    for book_id in cart:
        text += f"📘 ID книги: {book_id}\n"

    await message.answer(text)

@router.message(lambda message: message.text == "📦 Замовлення")
async def order_handler(message: types.Message):
    user_carts[message.from_user.id] = []
    await message.answer("📦 Замовлення оформлено! 🎉")

@router.callback_query(lambda c: c.data.startswith("page_"))
async def change_page(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    page = int(callback.data.split("_")[1])

    if page < 1:
        await callback.answer("Це перша сторінка")
        return

    user_pages[user_id] = page

    await callback.message.delete()
    await callback.answer()

    data = await get_books(page=page)

    for book in data["results"]:
        kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="➕ Додати до кошика",
                        callback_data=f"add_{book['id']}"
                    )
                ]
            ]
        )

        await callback.message.answer(
            f"📖 {book['title']}\n"
            f"💰 {book['price']}$\n"
            f"⭐ {book['rating']}\n"
            f"📦 {'Є в наявності' if book['availability'] else 'Немає'}",
            reply_markup=kb
        )

    await callback.message.answer(
        f"📄 Сторінка {page}",
        reply_markup=catalog_keyboard(page)
    )