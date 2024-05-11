import os
import json

from aiogram import Bot
from dotenv import load_dotenv

from database.models import Queue, Subscription
from keyboards import admin_confirm_panel
from keyboards.reply import admin_mk, user_mk

load_dotenv(dotenv_path='.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
PAYMENT_TOKEN = os.getenv('PAYMENT_TOKEN')
ADMINS = json.loads(os.getenv('ADMINS'))
BANK_CARD_NUMBER = os.getenv('BANK_CARD_NUMBER')


def is_admin(tg_id: str) -> bool:
    return tg_id in ADMINS


def get_main_kb(tg_id: str):
    return admin_mk if is_admin(tg_id) else user_mk


async def notify_admins(text: str, req_id: int | str, bot: Bot):
    for admin_id in ADMINS:
        await bot.send_message(text=text, chat_id=admin_id, reply_markup=await admin_confirm_panel(req_id))


async def get_user_and_buy_info_using_req_id(req_id: str):
    q = await Queue.get(req_id=req_id).select_related('product_type', 'user')
    product = q.product_type
    sub = await Subscription.filter(product_type=product).first()
    user_id = q.user.tg_id
    return q, sub, user_id


async def parse_multiline_input(user_input):
    lines = user_input.strip().split('\n')

    title = ''
    description = ''
    price = 0.0

    current_field = None

    for line in lines:
        line = line.strip()
        if line.startswith('1) '):
            current_field = 'title'
            title = line[2:].strip()
        elif line.startswith('2) '):
            current_field = 'description'
            description = line[2:].strip()
        elif line.startswith('3) '):
            current_field = 'price'
            try:
                price = float(line[2:].strip())
            except ValueError:
                return '', '', 0
        else:
            if current_field == 'description':
                description += ' ' + line

    return title, description, price
