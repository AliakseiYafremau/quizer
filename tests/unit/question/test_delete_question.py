import pytest
from faker import Faker
from unittest.mock import create_autospec

from tests.factories import make_question, make_survey

from quizer.application.exceptions import TargetNotFoundError
from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.interactors.question.delete_question import (
    DeleteQuestionInteractor,
)
from quizer.entities.exceptions import AccessDeniedError


async def test_delete_question_with_owner(uuid_generator, faker: Faker):
    # Arrange
    user_id = faker.telegram_id()
    survey = make_survey(author=user_id)
    question = make_question(survey=survey.id)

    question_repo_mock = create_autospec(QuestionRepository)
    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)

    id_provider_stub.get_current_user_id.return_value = user_id
    question_repo_mock.get_by_id.return_value = question
    survey_repo_mock.get_by_id.return_value = survey

    interactor = DeleteQuestionInteractor(
        id_provider_stub, question_repo_mock, survey_repo_mock
    )

    # Act
    await interactor(question.id)

    # Assert
    question_repo_mock.delete.assert_called_once_with(question.id)


async def test_delete_question_when_question_not_found(uuid_generator):
    # Arrange
    question_id = uuid_generator()
    question_repo_mock = create_autospec(QuestionRepository)
    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)

    question_repo_mock.get_by_id.return_value = None

    interactor = DeleteQuestionInteractor(
        id_provider_stub, question_repo_mock, survey_repo_mock
    )

    # Act
    with pytest.raises(TargetNotFoundError):
        await interactor(question_id)

    # Assert
    question_repo_mock.delete.assert_not_called()


async def test_delete_question_when_survey_not_found(uuid_generator):
    # Arrange
    question = make_question()
    question_repo_mock = create_autospec(QuestionRepository)
    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)

    question_repo_mock.get_by_id.return_value = question
    survey_repo_mock.get_by_id.return_value = None

    interactor = DeleteQuestionInteractor(
        id_provider_stub, question_repo_mock, survey_repo_mock
    )

    # Act
    with pytest.raises(TargetNotFoundError):
        await interactor(question.id)

    # Assert
    question_repo_mock.delete.assert_not_called()


async def test_delete_question_with_stranger(uuid_generator, faker: Faker):
    # Arrange
    author_id = faker.unique.telegram_id()
    user_id = faker.unique.telegram_id()
    survey = make_survey(author=author_id)
    question = make_question(survey=survey.id)

    question_repo_mock = create_autospec(QuestionRepository)
    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)

    id_provider_stub.get_current_user_id.return_value = user_id
    question_repo_mock.get_by_id.return_value = question
    survey_repo_mock.get_by_id.return_value = survey

    interactor = DeleteQuestionInteractor(
        id_provider_stub, question_repo_mock, survey_repo_mock
    )

    # Act
    with pytest.raises(AccessDeniedError):
        await interactor(question.id)

    # Assert
    question_repo_mock.delete.assert_not_called()
