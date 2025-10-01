import asyncio
import psycopg
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram_dialog import setup_dialogs

from quizer.config import load_bot_token, load_db_url
from quizer.bot_setup import BotIoC
from quizer.logger import get_logger

from quizer.presentation.bot.middlewares import IdProviderMiddleware
from quizer.presentation.bot.routers.start import start_router
from quizer.presentation.bot.routers.menu import menu_dialog
from quizer.presentation.bot.routers.manage_survey import manager_survey


logger = get_logger(__name__)


async def get_dispatcher() -> Dispatcher:
    async with await psycopg.AsyncConnection.connect(load_db_url()) as connection:
        ioc = BotIoC(db_connection=connection)
    dp = Dispatcher(ioc=ioc)
    dp.update.middleware(IdProviderMiddleware())
    dp.include_router(start_router)
    dp.include_router(menu_dialog)
    dp.include_router(manager_survey)
    setup_dialogs(dp)
    return dp


async def bot_run():
    token = load_bot_token()
    bot = Bot(token, default=DefaultBotProperties(parse_mode="html"))

    logger.info("Start app")
    dispatcher = await get_dispatcher()
    await dispatcher.start_polling(bot)


def run():
    asyncio.run(bot_run())
