from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from database import create_user

async def complete_registration(message: Message, state: FSMContext) -> None:
    """Завершает регистрацию и сохраняет данные в БД."""
    data: dict = await state.get_data()

    name: str = data["name"]
    last_name: str = data["last_name"]
    email: str = data["email"]
    phone: str = data["phone"]
    user_request: str = data.get("user_request", "**неопределен**")

    await message.answer(
        text=f"<b>🎉 РЕГИСТРАЦИЯ ЗАВЕРШЕНА!</b>\n\n"
             f"<b>Ваши данные были сохранены:</b>\n"
             f"• Имя: <i>{name}</i>\n"
             f"• Фамилия: <i>{last_name}</i>\n"
             f"• Email: <i>{email}</i>\n"
             f"• Телефон: <i>{phone}</i>\n\n"
             f"• Запрос: <i>{user_request}</i>\n\n"
             f"Вы всегда можете вызвать команду /edit_profile и отредактировать любое поле!",
        parse_mode=ParseMode.HTML,
    )

    await state.clear()
    create_user(data=data)

async def complete_user_request(message: Message, state: FSMContext, user_request: str = None) -> None:
    """Завершает процесс ввода запроса и регистрации."""
    if user_request:
        await state.update_data(user_request=user_request)
        completion_text = (
            f"<b>✅ Запрос сохранен!</b>\n\n"
            f"Психолог ознакомится с вашим запросом перед сеансом.\n\n"
            f"<i>Ваш запрос:</i>\n"
            f"<code>{user_request}</code>\n\n"
            f"Вы всегда можете вызвать команду /make_request и отредактировать или обновить запрос!"
        )
    else:
        completion_text = (
            f"<b>📝 Запрос не добавлен</b>\n\n"
            f"Вы всегда можете добавить или изменить запрос по команде /make_request из меню.\n\n"
            f"Это поможет психологу лучше подготовиться к сеансу."
        )

    await message.answer(text=completion_text, parse_mode=ParseMode.HTML)
    await complete_registration(message, state)
