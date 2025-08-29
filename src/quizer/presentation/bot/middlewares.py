from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import Message

from quizer.presentation.bot.id_provider import TelegramIdProvider


class IdProviderMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,  # type: ignore
        data: dict[str, Any],
    ) -> Any:
        data["id_provider"] = TelegramIdProvider(str(data["event_from_user"].id))
        return await handler(event, data)
