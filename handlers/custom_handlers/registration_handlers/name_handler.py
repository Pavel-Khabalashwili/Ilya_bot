from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from states import RegistartionStates
from keyboards import yes_no_keyboard

router = Router()


@router.message(F.text == "РЕГИСТРАЦИЯ")
async def reg_name_handler(message: Message, state: FSMContext):
    await state.set_state(RegistartionStates.name_state)

    question = (f"<b>ЭТАП - 1: ПОДТВЕРЖДЕНИЕ ИМЕНИ</b>\n\n"
                f"Использовать текущее ФИО: <i>{message.from_user.full_name}</i> ?")

    # Убираем реплай-клавиатуру
    await message.answer(
        text=question,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML

    )
    await message.answer(
        text="Выберите действие:",
        reply_markup=yes_no_keyboard,
    )


@router.callback_query(F.data == "yes_button", RegistartionStates.name_state)
async def reg_email_handler(callback: CallbackQuery, state: FSMContext):
    user_data = callback.from_user.full_name.split()
    name = user_data[0]
    last_name = user_data[1]

    await state.update_data(name=name, last_name=last_name)
    await state.set_state(RegistartionStates.email_state)

    await callback.message.answer(
        text=f"<b>ЭТАП - 2: EM@IL</b>\n\n"
             f"Введите emai:",
            parse_mode=ParseMode.HTML)

    await callback.answer()

@router.message(RegistartionStates.email_state)
async def reg_email_answer_handler(callback: CallbackQuery, state: FSMContext):

    pass
