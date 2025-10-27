from aiogram.types import InlineKeyboardButton


name_button = InlineKeyboardButton(text="👤 Имя", callback_data="edit_name")
last_name_button = InlineKeyboardButton(text="📝 Фамилия", callback_data="edit_last_name")
mail_button = InlineKeyboardButton(text="📧 Email", callback_data="edit_email")
telephone_button = InlineKeyboardButton(text="📞 Телефон", callback_data="edit_phone")
user_request_button = InlineKeyboardButton(text="🎯 Запрос", callback_data="edit_request")
full_info_button = InlineKeyboardButton(text="Показать все данные", callback_data="show_data")
cancel_button = InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_edit")
