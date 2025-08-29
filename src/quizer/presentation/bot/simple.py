from aiogram import Router
from aiogram.types import Message

from quizer.application.interfaces.common.id_provider import IdProvider

simple = Router()


@simple.message()
async def get_id(message: Message, id_provider: IdProvider):
    await message.answer(id_provider.get_current_user_id())