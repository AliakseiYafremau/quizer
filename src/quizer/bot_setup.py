import psycopg
from contextlib import asynccontextmanager, AsyncExitStack
from typing import AsyncGenerator

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

from quizer.application.factories.survey import SurveyFactory, QuestionFactory, AnswerFactory
from quizer.application.factories.user import UserFactory

from quizer.adapters.repositories.postgres.answer import SQLAnswerRepository
from quizer.adapters.repositories.postgres.question import SQLQuestionRepository
from quizer.adapters.repositories.postgres.survey import SQLSurveyRepository
from quizer.adapters.repositories.postgres.user import SQLUserRepository


class BotIoC(IoC):
    def __init__(self, db_connection: psycopg.AsyncConnection):
        self.db_connection = db_connection
        self.survey_factory = SurveyFactory(uuid_generator=self.uuid_generator())
        self.question_factory = QuestionFactory(uuid_generator=self.uuid_generator())
        self.answer_factory = AnswerFactory(uuid_generator=self.uuid_generator())
        self.user_factory = UserFactory()

    @staticmethod
    def uuid_generator() -> UUIDGenerator:
        return uuid4

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[psycopg.AsyncCursor, None]:
        async with self.db_connection.cursor() as cursor:
            yield cursor

    @asynccontextmanager
    async def user_repo(self) -> AsyncGenerator[UserRepository, None]:
        async with self.get_session() as session:
            yield SQLUserRepository(session=session, user_factory=self.user_factory)

    @asynccontextmanager
    async def answer_repo(self) -> AsyncGenerator[AnswerRepository, None]:
        async with self.get_session() as session:
            yield SQLAnswerRepository(session=session, answer_factory=self.answer_factory)

    @asynccontextmanager
    async def question_repo(self) -> AsyncGenerator[QuestionRepository, None]:
        async with self.get_session() as session:
            yield SQLQuestionRepository(
                session=session, question_factory=self.question_factory
            )

    @asynccontextmanager
    async def survey_repo(self) -> AsyncGenerator[SurveyRepository, None]:
        async with self.get_session() as session:
            yield SQLSurveyRepository(session=session)

    @asynccontextmanager
    async def get_user(
        self, id_provider: IdProvider
    ) -> AsyncGenerator[GetUserInteractor, None]:
        async with self.user_repo() as user_repo:
            yield GetUserInteractor(
                id_provider=id_provider,
                user_repo=user_repo,
            )

    @asynccontextmanager
    async def register(self) -> AsyncGenerator[RegisterInteractor, None]:
        async with self.user_repo() as user_repo:
            yield RegisterInteractor(user_repo=user_repo)

    @asynccontextmanager
    async def get_user_surveys(
        self, id_provider: IdProvider
    ) -> AsyncGenerator[GetUserSurveysInteractor, None]:
        async with self.survey_repo() as survey_repo:
            yield GetUserSurveysInteractor(
                id_provider=id_provider, surver_repo=survey_repo
            )

    @asynccontextmanager
    async def get_surveys_questions(
        self,
    ) -> AsyncGenerator[GetSurveyQuestionsInteractor, None]:
        async with self.question_repo() as question_repo:
            yield GetSurveyQuestionsInteractor(question_repo=question_repo)

    @asynccontextmanager
    async def create_survey(
        self, id_provider: IdProvider
    ) -> AsyncGenerator[CreateSurveryInteractor, None]:
        async with self.survey_repo() as survey_repo:
            yield CreateSurveryInteractor(
                id_provider=id_provider,
                survey_repo=survey_repo,
                survey_factory=self.survey_factory,
            )

    @asynccontextmanager
    async def save_survey(self, id_provider: IdProvider):
        async with self.survey_repo() as survey_repo:
            yield SaveSurveyInteractor(id_provider=id_provider, survey_repo=survey_repo)

    @asynccontextmanager
    async def delete_survey(
        self, id_provider: IdProvider
    ) -> AsyncGenerator[DeleteSurveyInteractor, None]:
        async with self.survey_repo() as survey_repo:
            yield DeleteSurveyInteractor(
                survey_repo=survey_repo,
                id_provider=id_provider,
            )

    @asynccontextmanager
    async def add_question(
        self, id_provider: IdProvider
    ) -> AsyncGenerator[AddSurveyQuestionInteractor, None]:
        async with AsyncExitStack() as stack:
            question_repo = await stack.enter_async_context(self.question_repo())
            survey_repo = await stack.enter_async_context(self.survey_repo())
            user_repo = await stack.enter_async_context(self.user_repo())
            yield AddSurveyQuestionInteractor(
                id_provider=id_provider,
                question_repo=question_repo,
                survey_repo=survey_repo,
                user_repo=user_repo,
                question_factory=self.question_factory,
            )

    @asynccontextmanager
    async def answer_question(
        self, id_provider: IdProvider
    ) -> AsyncGenerator[AnswerQuestionInteractor, None]:
        async with AsyncExitStack() as stack:
            question_repo = await stack.enter_async_context(self.question_repo())
            answer_repo = await stack.enter_async_context(self.answer_repo())
            yield AnswerQuestionInteractor(
                id_provider=id_provider,
                question_repo=question_repo,
                answer_repo=answer_repo,
                answer_factory=self.answer_factory,
            )

    @asynccontextmanager
    async def get_all_surveys(self) -> AsyncGenerator[GetAllSurveysInteractor, None]:
        async with self.survey_repo() as survey_repo:
            yield GetAllSurveysInteractor(
                survey_repo=survey_repo,
            )

    @asynccontextmanager
    async def get_survey_report(
        self, id_provider: IdProvider
    ) -> AsyncGenerator[GetSurveyReportInteractor, None]:
        async with AsyncExitStack() as stack:
            survey_repo = await stack.enter_async_context(self.survey_repo())
            question_repo = await stack.enter_async_context(self.question_repo())
            answer_repo = await stack.enter_async_context(self.answer_repo())
            yield GetSurveyReportInteractor(
                id_provider=id_provider,
                survey_repo=survey_repo,
                question_repo=question_repo,
                answer_repo=answer_repo,
            )

    @asynccontextmanager
    async def update_survey(
        self, id_provider: IdProvider
    ) -> AsyncGenerator[UpdateSurveyInteractor, None]:
        async with self.survey_repo() as survey_repo:
            yield UpdateSurveyInteractor(
                id_provider=id_provider,
                survey_repo=survey_repo,
            )
