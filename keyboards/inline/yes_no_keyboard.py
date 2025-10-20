from aiogram.types import InlineKeyboardMarkup

from buttons import yes_button, no_button


yes_no_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [yes_button],
        [no_button]
    ]
)