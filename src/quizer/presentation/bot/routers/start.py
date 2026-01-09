from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiogram_dialog import DialogManager, StartMode

from quizer.application.dto.user import UserDTO
from quizer.presentation.ioc import IoC
from quizer.logger import get_logger
from quizer.presentation.bot.routers.menu import Menu


logger = get_logger(__name__)

start_router = Router()


@start_router.message(CommandStart())
async def register(message: Message, ioc: IoC, dialog_manager: DialogManager):
    logger.info(
        'User %s register with "%s" name',
        message.from_user.id,  # type: ignore
        message.from_user.username,  # type: ignore
    )
    async with ioc.register() as interactor:
        try:
            await interactor(
                UserDTO(
                    id=message.from_user.id,  # type: ignore
                    name=message.from_user.username,  # type: ignore
                )
            )
        except Exception as e:
            pass
    await dialog_manager.start(
        state=Menu.main,
        mode=StartMode.RESET_STACK,
    )
