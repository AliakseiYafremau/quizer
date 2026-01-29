import pytest
from faker import Faker
from unittest.mock import create_autospec

from tests.factories import make_question, make_survey

from quizer.application.dto.question import UpdateQuestionDTO
from quizer.application.exceptions import TargetNotFoundError
from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.interactors.question.update_question import (
    UpdateQuestionInteractor,
)
from quizer.entities.exceptions import AccessDeniedError


async def test_update_question_with_owner(uuid_generator, faker: Faker):
    # Arrange
    user_id = faker.telegram_id()
    new_name = faker.sentence()
    new_options = [faker.word() for _ in range(3)]

    survey = make_survey(author=user_id)
    question = make_question(survey=survey.id)
    question_dto = UpdateQuestionDTO(question.id, new_name=new_name, options=new_options)

    question_repo_mock = create_autospec(QuestionRepository)
    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)

    id_provider_stub.get_current_user_id.return_value = user_id
    question_repo_mock.get_by_id.return_value = question
    survey_repo_mock.get_by_id.return_value = survey

    interactor = UpdateQuestionInteractor(
        id_provider_stub, question_repo_mock, survey_repo_mock
    )

    # Act
    await interactor(question_dto)

    # Assert
    question_repo_mock.update.assert_called_once()
    updated_question = question_repo_mock.update.call_args.args[0]
    assert updated_question.name == new_name
    assert updated_question.options == new_options


async def test_update_question_when_question_not_found(uuid_generator):
    # Arrange
    question_dto = UpdateQuestionDTO(uuid_generator(), new_name="name")
    question_repo_mock = create_autospec(QuestionRepository)
    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)

    question_repo_mock.get_by_id.return_value = None

    interactor = UpdateQuestionInteractor(
        id_provider_stub, question_repo_mock, survey_repo_mock
    )

    # Act
    with pytest.raises(TargetNotFoundError):
        await interactor(question_dto)

    # Assert
    question_repo_mock.update.assert_not_called()


async def test_update_question_when_survey_not_found(faker: Faker):
    # Arrange
    question = make_question()
    question_dto = UpdateQuestionDTO(question.id, new_name=faker.sentence())

    question_repo_mock = create_autospec(QuestionRepository)
    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)

    question_repo_mock.get_by_id.return_value = question
    survey_repo_mock.get_by_id.return_value = None

    interactor = UpdateQuestionInteractor(
        id_provider_stub, question_repo_mock, survey_repo_mock
    )

    # Act
    with pytest.raises(TargetNotFoundError):
        await interactor(question_dto)

    # Assert
    question_repo_mock.update.assert_not_called()


async def test_update_question_with_stranger(faker: Faker):
    # Arrange
    author_id = faker.unique.telegram_id()
    user_id = faker.unique.telegram_id()
    survey = make_survey(author=author_id)
    question = make_question(survey=survey.id)
    question_dto = UpdateQuestionDTO(question.id, new_name=faker.sentence())

    question_repo_mock = create_autospec(QuestionRepository)
    survey_repo_mock = create_autospec(SurveyRepository)
    id_provider_stub = create_autospec(IdProvider)

    id_provider_stub.get_current_user_id.return_value = user_id
    question_repo_mock.get_by_id.return_value = question
    survey_repo_mock.get_by_id.return_value = survey

    interactor = UpdateQuestionInteractor(
        id_provider_stub, question_repo_mock, survey_repo_mock
    )

    # Act
    with pytest.raises(AccessDeniedError):
        await interactor(question_dto)

    # Assert
    question_repo_mock.update.assert_not_called()
