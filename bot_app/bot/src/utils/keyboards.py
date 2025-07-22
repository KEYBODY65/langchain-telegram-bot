from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='/choose_rate')],
        [KeyboardButton(text='/choose_model')],
        [KeyboardButton(text='/start_chat')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)