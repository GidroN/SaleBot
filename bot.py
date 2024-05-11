import logging
import asyncio

from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from tortoise import Tortoise

from database.connection import init
from routers import router as main_router
from utils import BOT_TOKEN


async def main():
    # set up logging config
    logging.basicConfig(level=logging.INFO)

    # setup bot
    default = DefaultBotProperties(parse_mode='HTML')
    bot = Bot(token=BOT_TOKEN, default=default)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(main_router)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        # setup db
        await init()

        # start polling
        await dp.start_polling(bot, close_bot_session=False)
    finally:
        # shutdown bot and db connection
        tasks = [dp.storage.close(), Tortoise.close_connections()]
        await asyncio.wait([asyncio.create_task(task) for task in tasks])
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info('Bot stopped successfully.')
