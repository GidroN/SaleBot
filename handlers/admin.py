from aiogram import Router, F, Bot
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from database.models import Queue
from keyboards.inline import admin_panel, admin_confirm_panel
from keyboards.button_text import ButtonText as BT
from filters import AdminFilter

router = Router()


@router.message(AdminFilter(), Command(commands=['admin_panel']))
@router.message(AdminFilter(), F.text == BT.ADMIN_PANEL)
async def display_admin_panel(message: Message):
    await message.answer('Вы перешли в административную панель.', reply_markup=admin_panel)


@router.message(AdminFilter(), Command(commands=['requests']))
@router.message(AdminFilter(), F.text == BT.REQUESTS)
async def get_queue(message: Message):
    q = await Queue.filter(is_active=True).order_by('-date').select_related('user', 'product_type')
    if not q:
        await message.answer('Пока что активных заявок нет.')
        return

    for r in q:
        user = r.user
        product = r.product_type
        await message.answer(f'Заявка №<b>{r.req_id}</b>\n'
                             f'user_id: {user.tg_id}\n'
                             f'Имя: {user.name}\n'
                             f'Товар: {product.title}\n'
                             f'Сумма: {product.price}₽\n'
                             f'Дата: {r.date.strftime("%Y-%m-%d %H:%M")}',
                             reply_markup=await admin_confirm_panel(r.req_id, with_delay=False))


@router.message(AdminFilter(), Command(commands=['get_db']))
async def get_db(message: Message, bot: Bot):
    await bot.send_chat_action(chat_id=message.chat.id,
                               action=ChatAction.UPLOAD_DOCUMENT)
    file_path = 'database/db.sqlite3'
    await message.answer_document(
        document=FSInputFile(
            path=file_path
        )
    )
