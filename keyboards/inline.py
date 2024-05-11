from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Product
from keyboards.button_text import ButtonText as BT


# Builder
async def products(prefix: str):
    all_products = await Product.all()
    keyboard = InlineKeyboardBuilder()
    for item in all_products:
        keyboard.add(InlineKeyboardButton(text=item.title, callback_data=f'{prefix}{item.id}'))
    return keyboard.adjust(2).as_markup()


async def change_product_panel():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text=BT.CHANGE_PRODUCT_NAME, callback_data=f'change_product_info_title'),
        InlineKeyboardButton(text=BT.CHANGE_PRODUCT_DECSRIPTION, callback_data=f'change_product_info_description'),
        InlineKeyboardButton(text=BT.CHANGE_PRODUCT_PRICE, callback_data=f'change_product_info_price'),
        InlineKeyboardButton(text=BT.ADD_SUBSCRIPTION, callback_data=f'add_sub'),
        InlineKeyboardButton(text=BT.DELETE_PRODUCT, callback_data=f'delete_product')
    )
    keyboard.adjust(2, 2, 1).as_markup()

    return keyboard.as_markup()


async def buy_panel(product_id: int | str):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text=BT.BUY, callback_data=f'buy_product_{product_id}')
    )
    return keyboard.as_markup()


async def confirm_buy_panel(product_id: int | str):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text=BT.READY, callback_data=f'user_confirm_payment_{product_id}'),
        InlineKeyboardButton(text=BT.CANCEL, callback_data=f'user_cancel_payment_{product_id}')
    )
    return keyboard.as_markup()


admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BT.ADD_PRODUCT, callback_data='add_product'),
        ],
        [
            InlineKeyboardButton(text=BT.CHANGE_PRODUCT, callback_data='change_product'),
        ],
    ]
)


async def admin_confirm_panel(req_id: int | str, with_delay=True):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text=BT.CONFIRM, callback_data=f'admin_confirm_request_{req_id}'),
        InlineKeyboardButton(text=BT.CANCEL, callback_data=f'admin_cancel_request_{req_id}'),
    )
    if with_delay:
        keyboard.add(InlineKeyboardButton(text=BT.DELAY, callback_data=f'admin_delay_request_{req_id}'))

    return keyboard.adjust(2, 1).as_markup()
