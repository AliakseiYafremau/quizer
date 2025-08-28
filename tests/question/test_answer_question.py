from faker import Faker
from unittest.mock import create_autospec

from uuid import UUID

from tests.factories import make_answer

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.answer import AnswerRepository
from quizer.application.interactors.question.answer_question import (
    AnswerQuestionInteractor,
)


async def test_answer_question(answer_factory, faker: Faker):
    answer = make_answer()
    id_provider_stub = create_autospec(IdProvider)
    question_repo = create_autospec(QuestionRepository)
    answer_repo = create_autospec(AnswerRepository)
    answer_repo.get_by_user_and_question_id.return_value = None
    interactor = AnswerQuestionInteractor(
        id_provider_stub, question_repo, answer_repo, answer_factory
    )

    await interactor(answer.question, answer.option)

    answer_repo.add.assert_called_once()


async def test_answer_already_answered_question(answer_factory, faker: Faker):
    answer = make_answer()
    id_provider_stub = create_autospec(IdProvider)
    question_repo = create_autospec(QuestionRepository)
    answer_repo = create_autospec(AnswerRepository)
    answer_repo.get_by_user_and_question_id.return_value = answer
    interactor = AnswerQuestionInteractor(
        id_provider_stub, question_repo, answer_repo, answer_factory
    )

    await interactor(answer.question, answer.option)

    answer_repo.update.assert_called_once()
