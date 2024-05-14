from aiogram import F, Router, Bot
from aiogram.enums import ChatAction
from aiogram.types import CallbackQuery

from database.models import Product, Queue, User, Subscription
from keyboards import buy_panel, confirm_buy_panel
from keyboards.button_text import ButtonText as BT
from utils import BANK_CARD_NUMBER, notify_admins

router = Router()


@router.callback_query(F.data.startswith('get_prod_info_'))
async def get_product_info(callback: CallbackQuery):
    await callback.answer('')
    product_id = callback.data.split('_')[-1]
    product = await Product.get(id=product_id)
    await callback.message.answer_photo(
        photo=product.img_file_id,
        caption=f'<b>{product.title}</b>\n'
                f'Описание: {product.description}\n'
                f'Цена: {product.price}₽',
        reply_markup=await buy_panel(product_id),
    )


@router.callback_query(F.data.startswith('buy_product_'))
async def process_buy(callback: CallbackQuery):
    product_id = callback.data.split('_')[-1]
    product = await Product.get(id=product_id)

    if not await Subscription.filter(product_type=product).exists():
        await callback.answer('Извините, такого товара сейчас нет в наличии.', show_alert=True)
        return

    await callback.answer('')
    await callback.message.answer(
        f'Для завершения покупки вам необходимо перевести деньги по номеру <b>{BANK_CARD_NUMBER}</b> сумму {product.price}₽.\n'
        f'После перевода, нажмите на кнопку {BT.READY}. Как только нажмете, отправится запрос админу на получение подписки.\n',
        reply_markup=await confirm_buy_panel(product_id))


@router.callback_query(F.data.startswith('user_confirm_payment_'))
async def confirm_payment(callback: CallbackQuery, bot: Bot):
    await callback.answer('')
    product_id = callback.data.split('_')[-1]
    product = await Product.get(id=product_id)
    user_id = callback.from_user.id
    await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
    user = await User.get(tg_id=user_id)
    q = await Queue.create(user=user, product_type=product)
    await notify_admins(f'<b>Новая заявка!</b>\n'
                        f'№ <b>{q.req_id}</b>\n'
                        f'user_id: {user_id}\n'
                        f'Имя: {user.name}\n'
                        f'Товар: {product.title}\n'
                        f'Сумма: {product.price}₽\n'
                        f'Дата: {q.date.strftime("%Y-%m-%d %H:%M")}', bot, q.req_id)

    await callback.message.delete()
    await callback.message.answer(
        f'Заявка № <b>{q.req_id}</b> отправлена.\n'
        f'Товар: {product.title}\n'
        f'Сумма: {product.price}₽\n'
        f'Дата: {q.date.strftime("%Y-%m-%d %H:%M")}\n'
        f'-----------------------------------------------\n'
        f'Ожидайте подтверждения. Статус заявки можно посмотреть здесь - /my_requests.\n'
        f'Для связи используйте - /contacts')


@router.callback_query(F.data.startswith('user_cancel_payment_'))
async def cancel_payment(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
