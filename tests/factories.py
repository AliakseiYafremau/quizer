from uuid import UUID, uuid4

from tests.provider import generate_telegram_id, get_faker, TelegramIdProvider

from quizer.entities.user import User
from quizer.entities.survey import Survey, Question, Answer

faker = get_faker(TelegramIdProvider)


def make_user(id: str | None = None, name: str | None = None) -> User:
    return User(
        id=id or generate_telegram_id(faker),
        name=name or faker.name(),
    )


def make_question(
    id: UUID | None = None,
    name: str | None = None,
    survey: UUID | None = None,
    options: list[str] | None = None,
) -> Question:
    return Question(
        id=id or uuid4(),
        name=name or faker.sentence(),
        survey=survey or uuid4(),
        options=options or [faker.sentence() for _ in range(3)],
    )


def make_survey(
    id: UUID | None = None,
    name: str | None = None,
    author: str | None = None,
    questions: list[UUID] | None = None,
) -> Survey:
    return Survey(
        id=id or uuid4(),
        name=name or faker.sentence(),
        author=author or faker.telegram_id(),
        questions=questions or [uuid4() for _ in range(5)],
        is_available=False,
    )


def make_answer(
    id: UUID | None = None,
    user: str | None = None,
    survey: UUID | None = None,
    selections: tuple[tuple[UUID, int], ...] | None = None,
) -> Answer:
    return Answer(
        id=id or uuid4(),
        user=user or generate_telegram_id(faker),
        survey=survey or uuid4(),
        selections=selections or (),
    )
