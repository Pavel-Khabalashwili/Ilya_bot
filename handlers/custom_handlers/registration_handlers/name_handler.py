from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from database import create_user
from keyboards import yes_no_keyboard, telephone_keyboard
from states import RegistartionStates
from utils.validators import (validate_email,
                              validate_name,
                              validate_last_name,
                              validate_phone,
                              validate_request_comprehensive)

router = Router()


async def ask_user_request(message: Message, state: FSMContext) -> None:
    """Запрашивает психологический запрос у пользователя."""
    await state.set_state(RegistartionStates.define_request)

    await message.answer(
        text=f"<b>🎯 ОПРЕДЕЛЕНИЕ ЗАПРОСА</b>\n\n"
             f"Чтобы наша встреча была максимально полезной для вас, я предлагаю заранее обозначить тему разговора.\n\n"
             f"<b>Что вас беспокоит или что хотели бы обсудить?</b>\n"
             f"Это может быть конкретная ситуация, вопрос или просто то, что сейчас на душе.\n\n"
             f"<b>Желаете описать запрос сейчас?</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=yes_no_keyboard
    )


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
             f"• Телефон: <i>{phone}</i>\n\n\n\n"
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


@router.message(F.text == "РЕГИСТРАЦИЯ")
async def reg_name_handler(message: Message, state: FSMContext) -> None:
    """Начинает процесс регистрации."""
    await state.set_state(RegistartionStates.name_state)

    user = message.from_user
    telegram_id: int = user.id
    username_link: str = f"https://t.me/{user.username}" if user.username else "неопределенно"

    await state.update_data(telegram_id=telegram_id, username_link=username_link)

    question: str = (f"<b>ЭТАП - 1: ПОДТВЕРЖДЕНИЕ ИМЕНИ</b>\n\n"
                     f"Использовать текущее ФИО: <i>{message.from_user.full_name}</i> ?")

    await message.answer(text=question, parse_mode=ParseMode.HTML, reply_markup=yes_no_keyboard)


@router.callback_query(F.data == "yes_button", RegistartionStates.name_state)
async def reg_name_get_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Подтверждает использование имени из Telegram."""
    user_data: list = callback.from_user.full_name.split()
    name: str = user_data[0]
    last_name: str = user_data[1]

    await state.update_data(name=name, last_name=last_name)
    await state.set_state(RegistartionStates.email_state)

    await callback.message.answer(
        text=f"<b>ЭТАП - 2: EM@IL</b>\n\nВведите email:",
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


@router.callback_query(F.data == "no_button", RegistartionStates.name_state)
async def reg_name_input_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Запрашивает ручной ввод имени."""
    await state.set_state(RegistartionStates.name_input_state)
    await callback.message.answer("Введите ваше имя:")
    await callback.answer()


@router.message(RegistartionStates.name_input_state)
async def reg_name_validation_handler(message: Message, state: FSMContext) -> None:
    """Валидирует и сохраняет имя."""
    name_validation: dict = validate_name(message.text)

    if name_validation["is_valid"]:
        await state.update_data(name=name_validation["name"])
        await state.set_state(RegistartionStates.lastname_input_state)
        await message.answer("✅ Имя сохранено!\nТеперь введите фамилию:")
    else:
        await message.answer(f"❌ {name_validation['message']}\n\nПожалуйста, введите имя еще раз:")


@router.message(RegistartionStates.lastname_input_state)
async def reg_lastname_input_handler(message: Message, state: FSMContext) -> None:
    """Валидирует и сохраняет фамилию."""
    lastname_validation: dict = validate_last_name(message.text)

    if lastname_validation["is_valid"]:
        await state.update_data(last_name=lastname_validation["last_name"])
        await state.set_state(RegistartionStates.email_state)

        await message.answer(
            text=f"<b>ЭТАП - 2: EM@IL</b>\n\n"
                 f"✅ Фамилия сохранена!\n"
                 f"Теперь введите email:",
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer(f"❌ {lastname_validation['message']}\n\nПожалуйста, введите фамилию еще раз:")


@router.message(RegistartionStates.email_state)
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


@router.message(RegistartionStates.tel_number_state, F.text == "Ввести номер")
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


@router.message(RegistartionStates.tel_number_state, F.text)
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


@router.message(RegistartionStates.tel_number_state, F.contact)
async def reg_tel_get_handler(message: Message, state: FSMContext) -> None:
    """Сохраняет номер из контакта Telegram."""
    phone: str = message.contact.phone_number
    await state.update_data(phone=phone)
    await ask_user_request(message, state)


@router.callback_query(RegistartionStates.define_request, F.data == "no_button")
async def user_request_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Завершает регистрацию без запроса."""
    await complete_user_request(callback.message, state)
    await callback.answer()


@router.callback_query(RegistartionStates.define_request, F.data == "yes_button")
async def user_request_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """Запрашивает ввод психологического запроса."""
    task: str = f"<b>🎯ЗАПРОС</b>\n\nВведите запрос:"

    await state.set_state(RegistartionStates.input_request)
    await callback.message.answer(task, parse_mode=ParseMode.HTML)
    await callback.answer()


@router.message(RegistartionStates.input_request)
async def process_user_request(message: Message, state: FSMContext) -> None:
    """Валидирует и сохраняет психологический запрос."""
    user_input: str = message.text
    request_validation: dict = validate_request_comprehensive(user_input)

    if request_validation["is_valid"]:
        await complete_user_request(message, state, request_validation["request"])
    else:
        await message.answer(
            text=f"❌ {request_validation['message']}\n\n"
                 f"<b>Пожалуйста, опишите запрос еще раз:</b>\n"
                 f"<i>Пример: 'Хотел бы обсудить проблемы с тревожностью и стрессом на работе'</i>",
            parse_mode=ParseMode.HTML
        )