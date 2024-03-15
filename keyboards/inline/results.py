from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

answer = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Javoblarni yuborish", callback_data="send_answers")
        ]
    ]
)
