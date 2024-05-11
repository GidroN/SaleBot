from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from database.models import Queue, User
from keyboards import products
from keyboards.button_text import ButtonText as BT
from utils import get_main_kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    user = message.from_user

    tg_id = user.id
    full_name = user.first_name

    if user.last_name:
        full_name += " " + user.last_name

    username = user.username
    reply_mk = get_main_kb(str(tg_id))

    if username:
        await message.answer(f'Добро пожаловать, @{user.username}!', reply_markup=reply_mk)
    else:
        await message.answer(f'Добро пожаловать!', reply_markup=reply_mk)

    if not await User.filter(tg_id=tg_id).exists():
        await User.create(tg_id=tg_id, name=full_name.strip(), username=username)


@router.message(Command(commands=['catalog']))
@router.message(F.text == BT.CATALOG)
async def process_catalog(message: Message):
    await message.answer('Наш каталог', reply_markup=await products('get_prod_info_'))


@router.message(Command(commands=['contacts']))
@router.message(F.text == BT.CONTACTS)
async def process_contacts(message: Message):
    await message.answer("Если возникли вопросы, то можете писать сюда:\n"
                         "@afrikaman666 или @helmazy\n"
                         "<b>ОБЯЗАТЕЛЬНО ПРИ ОБРАЩЕНИИ УКАЗЫВАЙТЕ НОМЕР ЗАЯВКИ</b>")


@router.message(Command(commands=['my_requests']))
@router.message(F.text == BT.MY_REQUESTS)
async def process_my_requests(message: Message):
    user = await User.get(tg_id=message.from_user.id)
    q = await Queue.filter(user=user, is_active=True).select_related('product_type').order_by('-date')
    q_len = len(q)
    if q_len > 0:
        await message.answer(f'У вас сейчас имеются активные завяки в количестве - <b>{q_len}</b>\n'
                             f'Если хотите задать вопрос по заявке, вам сюда - /contacts')
        for r in q:
            await message.answer(f'Заявка № <b>{r.req_id}</b>\n'
                                 f'Дата: {r.date.strftime("%Y-%m-%d %H:%M")}\n'
                                 f'Товар: {r.product_type.title}\n'
                                 f'Сумма: {r.product_type.price}₽')

    else:
        await message.answer(f'У вас сейчас нет активных заявок.')


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(f"Наши комманды:"
                         f"/my_requests - для просмотра\n"
                         f"/contacts - для контактов\n"
                         f"/catalog - для просмотра каталога\n"
                         f"/help - для просмотра этого сообщения")


@router.message()
async def handle_buttons(message: Message):
    await message.reply('Извините я не знаю эту команду. Для просмотра всех команд наберите /help.')


