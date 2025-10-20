from aiogram.types import ReplyKeyboardMarkup

from buttons import registration_button


registration_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [registration_button]
    ],
    resize_keyboard=True,
    input_field_placeholder="Нажмите 'РЕГИСТРАЦИЯ', чтобы начать...",
    one_time_keyboard=True
)