from aiogram import Router, types

router = Router()

@router.message(lambda message: message.text == "❓ Допомога")
async def help_handler(message: types.Message):
    await message.answer(
        "📌 Інструкція користування ботом:\n\n"
        "📚 Каталог книг — перегляд доступних книг\n"
        "🛒 Кошик — ваші обрані книги\n"
        "➕ Додавання — через кнопку біля книги\n\n"
        "📦 Оформлення замовлення — тестовий режим"
    )