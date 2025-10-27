from aiogram.types import InlineKeyboardMarkup

from buttons import (name_button,
                                   last_name_button,
                                   mail_button,
                                   cancel_button,
                                   telephone_button,
                                   full_info_button,
                                   user_request_button)

edit_profile_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [name_button],
        [last_name_button],
        [mail_button],
        [telephone_button],
        [user_request_button],
        [full_info_button],
        [cancel_button],
    ]
)
