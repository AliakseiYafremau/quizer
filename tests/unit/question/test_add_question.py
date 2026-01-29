import pytest
from faker import Faker
from unittest.mock import create_autospec

from tests.factories import make_survey

from quizer.application.dto.question import CreateQuestionDTO
from quizer.application.exceptions import TargetNotFoundError
from quizer.application.factories.survey import QuestionFactory
from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.interfaces.repositories.user import UserRepository
from quizer.application.interactors.question.add_question import (
    AddSurveyQuestionInteractor,
)


async def test_add_question_for_own_survey(uuid_generator, faker: Faker):
    # Arrange
    user_id = faker.telegram_id()
    survey = make_survey(author=user_id)
    question_id = uuid_generator()
    question_dto = CreateQuestionDTO(
        survey_id=survey.id,
        name=faker.sentence(),
        options=[faker.word() for _ in range(3)],
    )

    id_provider_stub = create_autospec(IdProvider)
    question_repo_mock = create_autospec(QuestionRepository)
    survey_repo_mock = create_autospec(SurveyRepository)
    user_repo_stub = create_autospec(UserRepository)
    question_factory = QuestionFactory(lambda: question_id)

    id_provider_stub.get_current_user_id.return_value = user_id
    survey_repo_mock.get_by_user_id.return_value = [survey]
    question_repo_mock.add.return_value = question_id

    interactor = AddSurveyQuestionInteractor(
        id_provider_stub,
        question_repo_mock,
        survey_repo_mock,
        user_repo_stub,
        question_factory,
    )

    # Act
    result = await interactor(question_dto)

    # Assert
    assert result == question_id
    question_repo_mock.add.assert_called_once()
    new_question = question_repo_mock.add.call_args.args[0]
    assert new_question.id == question_id
    assert new_question.name == question_dto.name
    assert new_question.options == question_dto.options
    assert new_question.survey == question_dto.survey_id


async def test_add_question_for_stranger_survey(uuid_generator, faker: Faker):
    # Arrange
    user_id = faker.telegram_id()
    survey = make_survey()
    question_dto = CreateQuestionDTO(
        survey_id=survey.id,
        name=faker.sentence(),
        options=[faker.word() for _ in range(2)],
    )

    id_provider_stub = create_autospec(IdProvider)
    question_repo_mock = create_autospec(QuestionRepository)
    survey_repo_mock = create_autospec(SurveyRepository)
    user_repo_stub = create_autospec(UserRepository)
    question_factory = QuestionFactory(uuid_generator)

    id_provider_stub.get_current_user_id.return_value = user_id
    survey_repo_mock.get_by_user_id.return_value = []

    interactor = AddSurveyQuestionInteractor(
        id_provider_stub,
        question_repo_mock,
        survey_repo_mock,
        user_repo_stub,
        question_factory,
    )

    # Act
    with pytest.raises(TargetNotFoundError):
        await interactor(question_dto)

    # Assert
    question_repo_mock.add.assert_not_called()
