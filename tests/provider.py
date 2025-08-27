from faker import Faker
from faker.providers import BaseProvider


def generate_telegram_id(faker: Faker):
    return faker.bothify(text="##########")


class TelegramIdProvider(BaseProvider):
    def __init__(self, generator):
        self.fake = Faker()
        super().__init__(generator)

    def telegram_id(self) -> str:
        return generate_telegram_id(self.fake)


def get_faker(*providers: type[BaseProvider]):
    faker = Faker()
    for provider in providers:
        faker.add_provider(provider)
    return faker
