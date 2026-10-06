from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="⚡ محاسبه سطح مقطع کابل")
            ],
            [
                KeyboardButton(text="ℹ️ راهنما")
            ]
        ],
        resize_keyboard=True
    )

    return keyboard