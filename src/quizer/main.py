import asyncio
from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs

from quizer.config import load_bot_token
from quizer.bot_setup import BotIoC
from quizer.logger import get_logger

from quizer.presentation.bot.middlewares import IdProviderMiddleware
from quizer.presentation.bot.routers.start import start_router
from quizer.presentation.bot.routers.menu import menu_dialog
from quizer.presentation.bot.routers.create_survey import create_survey


logger = get_logger(__name__)


def get_dispatcher() -> Dispatcher:
    ioc = BotIoC()
    dp = Dispatcher(ioc=ioc)
    dp.update.middleware(IdProviderMiddleware())
    dp.include_router(start_router)
    dp.include_router(menu_dialog)
    dp.include_router(create_survey)
    setup_dialogs(dp)
    return dp


async def bot_run():
    token = load_bot_token()
    bot = Bot(token)

    logger.info("Start app")
    await get_dispatcher().start_polling(bot)


def run():
    asyncio.run(bot_run())
