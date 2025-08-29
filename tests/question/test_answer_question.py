from faker import Faker
from unittest.mock import create_autospec


from tests.factories import make_answer

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.answer import AnswerRepository
from quizer.application.dto.answer import AnswerDTO
from quizer.application.interactors.survey.finish_survey import (
    AnswerQuestionInteractor,
)


async def test_answer_question(answer_factory, faker: Faker):
    # Arrange
    answer = make_answer()
    answer_dto = AnswerDTO(
        survey=answer.survey,
        selections=answer.selections,
    )

    id_provider_stub = create_autospec(IdProvider)
    question_repo = create_autospec(QuestionRepository)
    answer_repo = create_autospec(AnswerRepository)

    answer_repo.get_by_user_and_survey_id.return_value = None

    interactor = AnswerQuestionInteractor(
        id_provider_stub, question_repo, answer_repo, answer_factory
    )

    # Act
    await interactor(answer_dto)

    # Assert
    answer_repo.add.assert_called_once()


async def test_answer_already_answered_question(answer_factory, faker: Faker):
    # Arrange
    answer = make_answer()
    answer_dto = AnswerDTO(
        survey=answer.survey,
        selections=answer.selections,
    )

    id_provider_stub = create_autospec(IdProvider)
    question_repo = create_autospec(QuestionRepository)
    answer_repo = create_autospec(AnswerRepository)

    answer_repo.get_by_user_and_survey_id.return_value = answer

    interactor = AnswerQuestionInteractor(
        id_provider_stub, question_repo, answer_repo, answer_factory
    )

    # Act
    await interactor(answer_dto)

    # Assert
    answer_repo.update.assert_called_once()
