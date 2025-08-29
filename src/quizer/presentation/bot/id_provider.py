from quizer.application.interfaces.common.id_provider import IdProvider


class TelegramIdProvider(IdProvider):
    def __init__(self, telegram_id: str):
        self.telegram_id = telegram_id

    def get_current_user_id(self):
        return self.telegram_id
