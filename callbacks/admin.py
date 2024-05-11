from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.models import Product, Subscription, Queue
from filters import AdminFilter
from keyboards import products, cancel_mk, change_product_panel, delete_product_mk, ready_mk
from keyboards.button_text import ButtonText as BT
from states import AddProductForm, AddSubscriptionForm, ChangeProductForm, DeleteProductForm
from utils import get_main_kb, get_user_and_buy_info_using_req_id

router = Router()


@router.message(AdminFilter(), ChangeProductForm.product, F.text == BT.READY)
async def process_ready_fields(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Информация сохранена!', reply_markup=get_main_kb(str(message.from_user.id)))


@router.callback_query(AdminFilter(), F.data == 'add_product')
async def add_product(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(AddProductForm.product)
    await callback.message.answer('Заполните информация о товаре в таком виде (пробелы после скобок соблюдать!):\n'
                                  '1) Название\n'
                                  '2) Описание (можно делать переход на след строку)\n'
                                  '3) Цена (для разделителя использовать точку)\n'
                                  '+ для фото просто как приложение.(обязательно)', reply_markup=cancel_mk)


@router.callback_query(AdminFilter(), F.data == 'change_product')
async def choose_product_for_change(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer('Выберите товар, который хотите изменить', reply_markup=await products('change_product_'))


@router.callback_query(AdminFilter(), ChangeProductForm.product, F.data.startswith('change_product_info_'))
async def process_change_product_title(callback: CallbackQuery,  state: FSMContext):
    await callback.answer('')
    data = callback.data
    product = (await state.get_data())['product']
    await state.update_data(product=product)

    if 'title' in data:
        await state.update_data(change_field='title')
    elif 'description' in data:
        await state.update_data(change_field='description')
    else:
        await state.update_data(change_field='price')

    await callback.message.answer('Теперь введите новое значения для выбранного поля.', reply_markup=cancel_mk)
    await state.set_state(ChangeProductForm.change_field)


@router.callback_query(AdminFilter(), F.data.startswith('change_product_'))
async def display_product_to_change(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    product_id = callback.data.split('_')[-1]
    product = await Product.get(id=product_id)
    await state.set_state(ChangeProductForm.product)
    await state.update_data(product=product)
    await callback.message.answer_photo(
        photo=product.img_file_id,
        caption=f'<b>{product.title}</b>\n'
                f'Описание: {product.description}\n'
                f'Цена: {product.price}₽',
        reply_markup=await change_product_panel()
    )
    await callback.message.answer(f'Выберите действия, и после завершения нажмите на кнопку {BT.READY}', reply_markup=ready_mk)


@router.callback_query(AdminFilter(), ChangeProductForm.product, F.data == 'delete_product')
async def display_msg_to_product_delete(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    product = (await state.get_data())['product']
    await state.set_state(DeleteProductForm.delete)
    subs = await Subscription.filter(product_type=product).count()
    if subs > 0:
        await callback.message.answer('Вы уверены, что хотите удалить этот товар?\n'
                                      f'<b>Вместе с этим товаром удаляться подписки в количестве - {subs}.</b>',
                                      reply_markup=delete_product_mk)
    else:
        await callback.message.answer('Вы уверены, что хотите удалить этот товар?', reply_markup=delete_product_mk)


@router.callback_query(AdminFilter(), ChangeProductForm.product, F.data.startswith('add_sub'))
async def choose_product_for_sub(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    product = (await state.get_data())['product']
    await state.set_state(AddSubscriptionForm.image)
    await state.update_data(product_type=product)
    await callback.message.answer('Теперь пришлите картинку для добавления.', reply_markup=cancel_mk)


@router.callback_query(AdminFilter(), F.data.startswith('admin_confirm_request_'))
async def admin_admin_confirm_request(callback: CallbackQuery, bot: Bot):
    req_id = callback.data.split('_')[-1]
    q, sub, user_id = await get_user_and_buy_info_using_req_id(req_id)

    if q.is_active is False:
        await callback.message.edit_text('Данная заявка уже была обработана.')
        return

    if sub is None:
        await callback.answer('Нельзя принять заявку. Товар закончился.', show_alert=True)
        return

    await callback.message.edit_text('Заявка одобрена!')
    await bot.send_message(chat_id=user_id, text=f'Ваша заявка № <b>{req_id}</b> была одобрена! Спасибо за покупку!')
    await bot.send_photo(chat_id=user_id,
                         photo=sub.img_file_id,
                         caption='Ваша покупка.')
    q.is_active = False
    await q.save()
    await sub.delete()


@router.callback_query(AdminFilter(), F.data.startswith('admin_cancel_request_'))
async def admin_cancel_request(callback: CallbackQuery, bot: Bot):
    req_id = callback.data.split('_')[-1]
    q, sub, user_id = await get_user_and_buy_info_using_req_id(req_id)

    if q.is_active is False:
        await callback.message.edit_text('Данная заявка уже была обработана.')
        return

    await callback.message.edit_text(f'Заявка № <b>{req_id}</b> отменена')
    await bot.send_message(chat_id=user_id, text=f'Ваша заявка № <b>{req_id}</b> была отменена! Если возникли вопросы, используйте - '
                                                 '/contacts')
    q.is_active = False
    await q.save()


@router.callback_query(AdminFilter(), F.data.startswith('admin_delay_request_'))
async def admin_delay_request(callback: CallbackQuery):
    req_id = callback.data.split('_')[-1]
    q, sub, user_id = await get_user_and_buy_info_using_req_id(req_id)

    if q.is_active is False:
        await callback.message.edit_text('Данная заявка уже была обработана.')
        return

    await callback.message.edit_text('Заявка отложена! Чтобы вернуться к ней, наберите команду /requests')
