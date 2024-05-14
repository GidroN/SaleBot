from enum import StrEnum


class ButtonText(StrEnum):
    MAIN_MENU = '🏠 Главное меню'
    PREVIOUS = '◀ Предыдущее'
    NEXT = '▶ Следующее'

    READY = '✔ Готово'
    CONFIRM = '✔ Принять'
    CATALOG = '🛒 Каталог'
    CANCEL = '❌ Отменить'
    CONTACTS = '☎ Контакты'
    BUY = '💵 Купить'
    MY_REQUESTS = '📖 Мои заявки'
    DELAY = '🕰 Отложить'
    HELP = '❓ Помощь'

    ADMIN_PANEL = '🕵️‍♂️ Админ. панель'
    REQUESTS = '📚 Заявки'
    ADD_SUBSCRIPTION = '➕ Добавить подписку'
    ADD_PRODUCT = '➕ Добавить товар'
    DELETE = '🗑 Удалить'
    DELETE_PRODUCT = '🗑 Удалить товар'
    CHANGE_PRODUCT = '✏ Изменить товар'
    CHANGE_PRODUCT_NAME = '✏ Изменить имя'
    CHANGE_PRODUCT_DECSRIPTION = '✏ Изменить описание'
    CHANGE_PRODUCT_PRICE = '✏ Изменить цену'
