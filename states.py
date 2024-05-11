from aiogram.fsm.state import StatesGroup, State


class AddProductForm(StatesGroup):
    product = State()
    subscription = State()


class ChangeProductForm(StatesGroup):
    product = State()
    change_field = State()


class DeleteProductForm(StatesGroup):
    product = State()
    delete = State()


class AddSubscriptionForm(StatesGroup):
    image = State()
