from aiogram import F, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.models import Product, Subscription
from filters import AdminFilter
from keyboards import ready_mk
from states import AddProductForm, AddSubscriptionForm, ChangeProductForm, DeleteProductForm
from utils import parse_multiline_input, get_main_kb
from keyboards.button_text import ButtonText as BT

router = Router()


@router.message(AdminFilter(), AddProductForm.product, F.photo & F.caption)
async def process_productform(message: Message, state: FSMContext, bot: Bot):
    text = message.html_text
    title, description, price = await parse_multiline_input(text)
    photo_id = message.photo[-1].file_id
    path = f'database/img/products/{photo_id}.png'
    await bot.download(photo_id, path)
    await Product.create(title=title, description=description, price=price, img=path, img_file_id=photo_id)
    await message.answer('Новый товар успешно добавлен!', reply_markup=get_main_kb(str(message.from_user.id)))
    await state.clear()


@router.message(AdminFilter(), AddProductForm.product, ~F.photo)
@router.message(AdminFilter(), AddProductForm.product, F.photo & ~F.caption)
async def process_invalid_productform(message: Message, state: FSMContext, bot: Bot):
    if message.text == BT.CANCEL:
        await state.clear()
        await message.answer('Отменено.', reply_markup=get_main_kb(str(message.from_user.id)))
        return

    await message.answer("Пришлите вместе с фото и описанием!")


@router.message(AdminFilter(), AddSubscriptionForm.image, F.photo)
async def process_subscriptionform_image(message: Message, state: FSMContext, bot: Bot):
    photo_id = message.photo[-1].file_id
    path = f'database/img/subscriptions/{photo_id}.png'
    await bot.download(photo_id, path)
    product_type = (await state.get_data())['product_type']
    await Subscription.create(product_type=product_type,
                              img=path,
                              img_file_id=photo_id)
    await message.answer('Подписка успешно добавлена!', reply_markup=ready_mk)
    await state.set_state(ChangeProductForm.product)
    await state.update_data(product=product_type)


@router.message(AdminFilter(), AddSubscriptionForm.image, ~F.photo)
async def process_subscriptionform_image(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        product = (await state.get_data())['product_type']
        await state.set_state(ChangeProductForm.product)
        await state.update_data(product=product)
        await message.answer('Отменено.', reply_markup=ready_mk)
        return
    await message.answer('Принимаются только картинки!')


@router.message(AdminFilter(), ChangeProductForm.change_field, F.text)
async def process_changeproductform_title(message: Message, state: FSMContext):
    if message.text == BT.CANCEL:
        await message.answer('Отменено.', reply_markup=ready_mk)
        return

    data = await state.get_data()
    product = data['product']
    field = data['change_field']

    if field == 'title':
        product.title = message.text
    elif field == 'description':
        product.description = message.text
    else:
        try:
            product.price = float(message.text)
        except TypeError:
            await message.answer('Для цены введите числовое значение!')
            return

    await product.save()
    await state.set_state(ChangeProductForm.product)
    await message.answer('Информация обновлена!', reply_markup=ready_mk)


@router.message(AdminFilter(), DeleteProductForm.delete, F.text == BT.DELETE)
async def process_delete_product(message: Message, state: FSMContext):
    product = (await state.get_data())['product']
    await product.delete()
    await message.answer('Товар успешно удален!', reply_markup=get_main_kb(str(message.from_user.id)))
    await state.clear()


@router.message(AdminFilter(), DeleteProductForm.delete, F.text == BT.CANCEL)
async def cancel_delete_product(message: Message, state: FSMContext):
    product = (await state.get_data())['product']
    await message.answer('Операция отменена.', reply_markup=ready_mk)
    await state.set_state(ChangeProductForm.product)
    await state.update_data(product=product)
