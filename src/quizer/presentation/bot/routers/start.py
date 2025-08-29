from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from quizer.application.dto.user import UserDTO
from quizer.presentation.ioc import IoC

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message, ioc: IoC):
    with ioc.register() as interactor:
        await interactor(UserDTO(
            id=message.from_user.id,
            name=message.from_user.username,
        ))
