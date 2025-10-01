import psycopg
from contextlib import contextmanager, ExitStack, asynccontextmanager
from typing import Generator, Any, AsyncGenerator

from uuid import uuid4

from quizer.presentation.ioc import IoC

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.common.uuid_generator import UUIDGenerator
from quizer.application.interfaces.repositories.answer import AnswerRepository
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.interfaces.repositories.user import UserRepository

from quizer.application.interactors.user.get_user import GetUserInteractor
from quizer.application.interactors.user.register import RegisterInteractor
from quizer.application.interactors.user.get_user_surveys import (
    GetUserSurveysInteractor,
)
from quizer.application.interactors.question.get_survey_questions import (
    GetSurveyQuestionsInteractor,
)
from quizer.application.interactors.question.add_question import (
    AddSurveyQuestionInteractor,
)
from quizer.application.interactors.survey.create_survey import CreateSurveryInteractor
from quizer.application.interactors.survey.delete_survey import DeleteSurveyInteractor
from quizer.application.interactors.survey.answer_question import (
    AnswerQuestionInteractor,
)
from quizer.application.interactors.survey.get_all_surveys import (
    GetAllSurveysInteractor,
)
from quizer.application.interactors.survey.get_survey_report import (
    GetSurveyReportInteractor,
)
from quizer.application.interactors.survey.update_survey import UpdateSurveyInteractor
from quizer.application.interactors.survey.finish_survey import SaveSurveyInteractor

from quizer.application.factories.survey import (
    SurveyFactory,
    QuestionFactory,
    AnswerFactory,
)

from quizer.adapters.repositories.answer import FakeAnswerRepository
from quizer.adapters.repositories.question import FakeQuestionRepository
from quizer.adapters.repositories.survey import FakeSurveyRepository
from quizer.adapters.repositories.user import FakeUserRepository

from quizer.adapters.database import get_async_connection, get_async_session


class BotIoC(IoC):
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.survey_factory = SurveyFactory(uuid_generator=self.uuid_generator())
        self.question_factory = QuestionFactory(uuid_generator=self.uuid_generator())
        self.answer_factory = AnswerFactory(uuid_generator=self.uuid_generator())

    def uuid_generator(self) -> UUIDGenerator:
        return uuid4

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[psycopg.AsyncConnection]:
        yield await get_async_connection(self.db_url)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[psycopg.AsyncCursor]:
        async with self.get_connection() as connection:
            yield await get_async_session(connection=connection)

    @contextmanager
    def user_repo(self) -> Generator[UserRepository, None, None]:
        yield FakeUserRepository()

    @contextmanager
    def answer_repo(self) -> Generator[AnswerRepository, None, None]:
        yield FakeAnswerRepository()

    @contextmanager
    def question_repo(self) -> Generator[QuestionRepository, None, None]:
        yield FakeQuestionRepository()

    @contextmanager
    def survey_repo(self) -> Generator[SurveyRepository, None, None]:
        yield FakeSurveyRepository()

    @contextmanager
    def get_user(
        self, id_provider: IdProvider
    ) -> Generator[GetUserInteractor, None, None]:
        with self.user_repo() as user_repo:
            yield GetUserInteractor(
                id_provider=id_provider,
                user_repo=user_repo,
            )

    @contextmanager
    def register(self) -> Generator[RegisterInteractor, None, None]:
        with self.user_repo() as user_repo:
            yield RegisterInteractor(user_repo=user_repo)

    @contextmanager
    def get_user_surveys(
        self, id_provider: IdProvider
    ) -> Generator[GetUserSurveysInteractor, None, None]:
        with self.survey_repo() as survey_repo:
            yield GetUserSurveysInteractor(
                id_provider=id_provider, surver_repo=survey_repo
            )

    @contextmanager
    def get_surveys_questions(
        self,
    ) -> Generator[GetSurveyQuestionsInteractor, None, None]:
        with self.question_repo() as question_repo:
            yield GetSurveyQuestionsInteractor(question_repo=question_repo)

    @contextmanager
    def create_survey(
        self, id_provider: IdProvider
    ) -> Generator[CreateSurveryInteractor, None, None]:
        with self.survey_repo() as survey_repo:
            yield CreateSurveryInteractor(
                id_provider=id_provider,
                survey_repo=survey_repo,
                survey_factory=self.survey_factory,
            )

    @contextmanager
    def save_survey(self, id_provider: IdProvider):
        with self.survey_repo() as survey_repo:
            yield SaveSurveyInteractor(id_provider=id_provider, survey_repo=survey_repo)

    @contextmanager
    def delete_survey(
        self, id_provider: IdProvider
    ) -> Generator[DeleteSurveyInteractor, None, None]:
        with self.survey_repo() as survey_repo:
            yield DeleteSurveyInteractor(
                survey_repo=survey_repo,
                id_provider=id_provider,
            )

    @contextmanager
    def add_question(
        self, id_provider: IdProvider
    ) -> Generator[AddSurveyQuestionInteractor, None, None]:
        with ExitStack() as stack:
            question_repo = stack.enter_context(self.question_repo())
            survey_repo = stack.enter_context(self.survey_repo())
            user_repo = stack.enter_context(self.user_repo())
            yield AddSurveyQuestionInteractor(
                id_provider=id_provider,
                question_repo=question_repo,
                survey_repo=survey_repo,
                user_repo=user_repo,
                question_factory=self.question_factory,
            )

    @contextmanager
    def answer_question(
        self, id_provider: IdProvider
    ) -> Generator[AnswerQuestionInteractor, Any, Any]:
        with ExitStack() as stack:
            question_repo = stack.enter_context(self.question_repo())
            answer_repo = stack.enter_context(self.answer_repo())
            yield AnswerQuestionInteractor(
                id_provider=id_provider,
                question_repo=question_repo,
                answer_repo=answer_repo,
                answer_factory=self.answer_factory,
            )

    @contextmanager
    def get_all_surveys(self) -> Generator[GetAllSurveysInteractor, Any, Any]:
        with self.survey_repo() as survey_repo:
            yield GetAllSurveysInteractor(
                survey_repo=survey_repo,
            )

    @contextmanager
    def get_survey_report(
        self, id_provider: IdProvider
    ) -> Generator[GetSurveyReportInteractor, Any, Any]:
        with ExitStack() as stack:
            survey_repo = stack.enter_context(self.survey_repo())
            question_repo = stack.enter_context(self.question_repo())
            answer_repo = stack.enter_context(self.answer_repo())
            yield GetSurveyReportInteractor(
                id_provider=id_provider,
                survey_repo=survey_repo,
                question_repo=question_repo,
                answer_repo=answer_repo,
            )

    @contextmanager
    def update_survey(
        self, id_provider: IdProvider
    ) -> Generator[UpdateSurveyInteractor, Any, Any]:
        with self.survey_repo() as survey_repo:
            yield UpdateSurveyInteractor(
                id_provider=id_provider,
                survey_repo=survey_repo,
            )
