from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from .button_text import ButtonText as BT


user_mk = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.CATALOG),
        ],
        [
            KeyboardButton(text=BT.CONTACTS),
            KeyboardButton(text=BT.MY_REQUESTS)
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Главное меню:',
)

admin_mk = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.CATALOG),
        ],
        [
            KeyboardButton(text=BT.ADMIN_PANEL),
            KeyboardButton(text=BT.REQUESTS),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Главное меню:',
)

cancel_mk = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.CANCEL)
        ],

    ],
    resize_keyboard=True,
    input_field_placeholder='Для отмены действия нажмите на кнопку.',
    one_time_keyboard=True,
)


ready_mk = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.READY)
        ]
    ],
    resize_keyboard=True
)

delete_product_mk = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=BT.CANCEL),
            KeyboardButton(text=BT.DELETE),
        ],

    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

remove_mk = ReplyKeyboardRemove()
