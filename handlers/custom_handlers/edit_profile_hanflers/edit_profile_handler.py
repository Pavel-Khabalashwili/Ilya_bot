from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import EditProfileStates
from aiogram.enums import ParseMode

from keyboards import edit_profile_keyboard, telephone_keyboard
from utils.validators import (validate_email,
                              validate_name,
                              validate_last_name,
                              validate_phone,
                              validate_request_comprehensive)

edit_router = Router()


async def return_to_edit_menu(message: Message, state: FSMContext, success_message: str = None):
    """
    Общая функция для возврата в меню редактирования после успешного изменения
    """
    if success_message:
        await message.answer(success_message, parse_mode="HTML")

    await state.set_state(EditProfileStates.choose_field)
    await message.answer(
        "📋 <b>Выберите поле для редактирования:</b>",
        reply_markup=edit_profile_keyboard,
        parse_mode="HTML"
    )


@edit_router.message(Command("edit_profile"))
async def edit_profile_start(message: Message, state: FSMContext):
    """Начало редактирования профиля"""
    await state.set_state(EditProfileStates.choose_field)
    await message.answer(
        "📋 <b>Выберите поле для редактирования:</b>",
        reply_markup=edit_profile_keyboard,
        parse_mode="HTML"
    )


@edit_router.message(Command("make_request"))
async def make_request_command(message: Message, state: FSMContext):
    """Обработка команды /make_request"""
    await state.set_state(EditProfileStates.editing_request)
    await message.answer(
        f"<b>🎯 ЗАПРОС</b>\n\n"
        f"Запрос в психологии — это то, с чем вы приходите к психологу, "
        f"основная тема или проблема, которую вы хотите обсудить.\n\n"
        f"✏️ Введите новый запрос:",
        parse_mode=ParseMode.HTML
    )


@edit_router.callback_query(EditProfileStates.choose_field, F.data == "edit_name")
async def edit_name_start(callback: CallbackQuery, state: FSMContext):
    """Начинаем редактирование имени"""
    await state.set_state(EditProfileStates.editing_name)
    await callback.message.answer("✏️ Введите новое имя:")
    await callback.answer()


@edit_router.message(EditProfileStates.editing_name)
async def edit_name_process(message: Message, state: FSMContext):
    """Обрабатываем новое имя"""
    validation = validate_name(message.text)
    if validation["is_valid"]:
        # Сохраняем в состояние FSM
        await state.update_data(name=validation['name'])
        # Сохраняем в БД: await update_user_name(message.from_user.id, validation["name"])
        await return_to_edit_menu(
            message,
            state,
            f"✅ Имя изменено на: <b>{validation['name']}</b>"
        )
    else:
        # Остаемся в том же состоянии для повторного ввода
        await message.answer(f"❌ {validation['message']}\n\n✏️ Пожалуйста, введите имя еще раз:")


@edit_router.callback_query(EditProfileStates.choose_field, F.data == "edit_last_name")
async def edit_last_name_start(callback: CallbackQuery, state: FSMContext):
    """Начинаем редактирование фамилии"""
    await state.set_state(EditProfileStates.editing_last_name)
    await callback.message.answer("✏️ Введите новую фамилию:")
    await callback.answer()


@edit_router.message(EditProfileStates.editing_last_name)
async def edit_last_name_process(message: Message, state: FSMContext):
    """Обрабатываем новую фамилию"""
    validation = validate_last_name(message.text)
    if validation["is_valid"]:
        # Сохраняем в состояние FSM
        await state.update_data(last_name=validation['last_name'])
        # Сохраняем в БД
        await return_to_edit_menu(
            message,
            state,
            f"✅ Фамилия изменена на: <b>{validation['last_name']}</b>"
        )
    else:
        # Остаемся в том же состоянии для повторного ввода
        await message.answer(f"❌ {validation['message']}\n\n✏️ Пожалуйста, введите фамилию еще раз:")


@edit_router.callback_query(EditProfileStates.choose_field, F.data == "edit_email")
async def edit_email_start(callback: CallbackQuery, state: FSMContext):
    """Начинаем редактирование email"""
    await state.set_state(EditProfileStates.editing_email)
    await callback.message.answer("✏️ Введите новый email:")
    await callback.answer()


@edit_router.message(EditProfileStates.editing_email)
async def edit_email_process(message: Message, state: FSMContext):
    """Обрабатываем новый email"""
    validation = validate_email(message.text)
    if validation["is_valid"]:
        # Сохраняем в состояние FSM
        await state.update_data(email=validation['email'])
        # Сохраняем в БД
        await return_to_edit_menu(
            message,
            state,
            f"✅ Email изменен на: <b>{validation['email']}</b>"
        )
    else:
        # Остаемся в том же состоянии для повторного ввода
        await message.answer(f"❌ {validation['message']}\n\n✏️ Пожалуйста, введите email еще раз:\n"
                             f"Пример: example@mail.ru")


@edit_router.callback_query(EditProfileStates.choose_field, F.data == "edit_phone")
async def edit_phone_start(callback: CallbackQuery, state: FSMContext):
    """Начинаем редактирование телефона"""
    await state.set_state(EditProfileStates.editing_phone)
    await callback.message.answer(
        "📱 Выберите способ ввода номера телефона:",
        reply_markup=telephone_keyboard
    )
    await callback.answer()


@edit_router.message(EditProfileStates.editing_phone, F.contact)
async def edit_phone_from_contact(message: Message, state: FSMContext):
    """Обрабатываем номер телефона из контакта"""
    phone_number = message.contact.phone_number
    validation = validate_phone(phone_number)

    if validation["is_valid"]:
        # Сохраняем в состояние FSM
        await state.update_data(phone=validation['phone'])
        # Сохраняем в БД
        await return_to_edit_menu(
            message,
            state,
            f"✅ Телефон изменен на: <b>{validation['phone']}</b>"
        )
    else:
        # Остаемся в том же состоянии для повторного ввода
        await message.answer(
            f"❌ {validation['message']}\n\n"
            "📱 Пожалуйста, попробуйте еще раз:",
            reply_markup=telephone_keyboard
        )


@edit_router.message(EditProfileStates.editing_phone)
async def edit_phone_process(message: Message, state: FSMContext):
    """Обрабатываем номер телефона из ручного ввода"""
    # Проверяем, что это не команда и не другой тип сообщения
    if message.text.startswith('/'):
        return

    phone_number = message.text
    validation = validate_phone(phone_number)

    if validation["is_valid"]:
        # Сохраняем в состояние FSM
        await state.update_data(phone=validation['phone'])
        # Сохраняем в БД
        await return_to_edit_menu(
            message,
            state,
            f"✅ Телефон изменен на: <b>{validation['phone']}</b>"
        )
    else:
        # Остаемся в том же состоянии для повторного ввода
        await message.answer(
            f"❌ {validation['message']}\n\n"
            "📱 Пожалуйста, введите номер телефона еще раз:",
            reply_markup=telephone_keyboard
        )


@edit_router.callback_query(EditProfileStates.choose_field, F.data == "edit_request")
async def edit_request_start(callback: CallbackQuery, state: FSMContext):
    """Начинаем редактирование запроса"""
    await state.set_state(EditProfileStates.editing_request)
    await callback.message.answer(
        f"<b>🎯 ЗАПРОС</b>\n\n"
        f"Запрос в психологии — это то, с чем вы приходите к психологу, "
        f"основная тема или проблема, которую вы хотите обсудить.\n\n"
        f"✏️ Введите новый запрос:",
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


@edit_router.message(EditProfileStates.editing_request)
async def edit_request_process(message: Message, state: FSMContext):
    """Обрабатываем новый запрос"""
    validation = validate_request_comprehensive(message.text)
    if validation["is_valid"]:
        # Сохраняем в состояние FSM
        await state.update_data(request=message.text)
        # Сохраняем в БД
        await return_to_edit_menu(
            message,
            state,
            "✅ Запрос обновлен!"
        )
    else:
        # Остаемся в том же состоянии для повторного ввода
        await message.answer(f"❌ {validation['message']}\n\n✏️ Пожалуйста, введите запрос еще раз:")


@edit_router.callback_query(EditProfileStates.choose_field, F.data == "show_data")
async def show_all_data(callback: CallbackQuery, state: FSMContext):
    """Показываем все данные пользователя"""
    user_data = await state.get_data()

    # В будущем данные будут браться из БД, а не из состояния
    # user_data = await get_user_data_from_db(callback.from_user.id)

    # Формируем сообщение с данными
    data_message = (
        f"<b>📊 ВАШИ ДАННЫЕ:</b>\n\n"
        f"👤 <b>Имя:</b> {user_data.get('name', 'Не указано')}\n"
        f"👥 <b>Фамилия:</b> {user_data.get('last_name', 'Не указана')}\n"
        f"📧 <b>Email:</b> {user_data.get('email', 'Не указан')}\n"
        f"📱 <b>Телефон:</b> {user_data.get('phone', 'Не указан')}\n"
        f"🎯 <b>Запрос:</b> {user_data.get('request', 'Не указан')}\n\n"
        f"<i>💡 В будущем данные будут загружаться из базы данных</i>"
    )

    await callback.message.answer(data_message, parse_mode=ParseMode.HTML)
    await callback.answer()


@edit_router.callback_query(EditProfileStates.choose_field, F.data == "cancel_edit")
async def cancel_edit(callback: CallbackQuery, state: FSMContext):
    """Отмена редактирования"""
    # TODO: сравнить данные с базой данных и залить новые обновления в БД
    # user_data = await state.get_data()
    # await save_user_data_to_db(callback.from_user.id, user_data)

    await callback.message.answer("❌ Редактирование отменено.")
    await state.clear()
    await callback.answer()

