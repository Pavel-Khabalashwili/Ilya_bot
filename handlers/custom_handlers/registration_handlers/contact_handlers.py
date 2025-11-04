from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardRemove

from states import RegistartionStates
from utils.validators import validate_email, validate_phone
from keyboards import telephone_keyboard
from .router import reg_router, ask_user_request


@reg_router.message(RegistartionStates.email_state)
async def reg_email_answer_handler(message: Message, state: FSMContext) -> None:
    """Валидирует и сохраняет email."""
    user_input: str = message.text
    email: dict = validate_email(email=user_input)

    if email["is_valid"]:
        await state.update_data(email=email['email'])
        await state.set_state(RegistartionStates.tel_number_state)

        await message.answer(
            text=f"<b>ЭТАП - 3: НОМЕР ТЕЛЕФОНА</b>\n\nНажмите на отправить номер или ручной ввод",
            reply_markup=telephone_keyboard,
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer(
            text=f"❌ {email['message']}\n\n"
                 f"<b>Пожалуйста, введите корректный email:</b>\n"
                 f"<i>Пример: example@mail.ru</i>",
            parse_mode=ParseMode.HTML
        )


@reg_router.message(RegistartionStates.tel_number_state, F.text == "Ввести номер")
async def reg_tel_manual_request_handler(message: Message) -> None:
    """Запрашивает ручной ввод номера телефона."""
    await message.answer(
        text=f"<b>ВВОД НОМЕРА ТЕЛЕФОНА</b>\n\n"
             f"📞 <b>Введите ваш номер телефона:</b>\n"
             f"<i>Пример: +79123456789 или 89123456789</i>\n\n"
             f"Формат: с кодом страны или без",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove()
    )


@reg_router.message(RegistartionStates.tel_number_state, F.text)
async def reg_tel_manual_handler(message: Message, state: FSMContext) -> None:
    """Валидирует и сохраняет номер телефона."""
    user_input: str = message.text
    phone_validation: dict = validate_phone(user_input)

    if phone_validation["is_valid"]:
        await state.update_data(phone=phone_validation["phone"])
        await ask_user_request(message, state)
    else:
        await message.answer(
            text=f"❌ {phone_validation['message']}\n\n"
                 f"<b>Пожалуйста, введите корректный номер телефона:</b>\n"
                 f"<i>Пример: +79123456789 или 89123456789</i>",
            parse_mode=ParseMode.HTML
        )


@reg_router.message(RegistartionStates.tel_number_state, F.contact)
async def reg_tel_get_handler(message: Message, state: FSMContext) -> None:
    """Сохраняет номер из контакта Telegram."""
    phone: str = message.contact.phone_number
    await state.update_data(phone=phone)
    await ask_user_request(message, state)
