from aiogram.types import ReplyKeyboardMarkup

from buttons import tel_get_button, tel_input_button

telephone_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [tel_get_button],
        [tel_input_button],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

