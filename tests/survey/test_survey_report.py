import pytest
from faker import Faker
from unittest.mock import create_autospec

from tests.factories import make_user, make_survey, make_question, make_answer

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.answer import AnswerRepository
from quizer.application.dto.survey import SurveyReportDTO
from quizer.entities.exceptions import AccessDeniedError
from quizer.application.interactors.survey.get_survey_report import (
    GetSurveyReportInteractor,
)


@pytest.fixture
def make_interactor():
    def factory(current_user_id, survey, answers):
        id_provider = create_autospec(IdProvider)
        survey_repo_stub = create_autospec(SurveyRepository)
        question_repo_stub = create_autospec(QuestionRepository)
        answer_repo_stub = create_autospec(AnswerRepository)

        id_provider.get_current_user_id.return_value = current_user_id
        survey_repo_stub.get_by_id.return_value = survey
        answer_repo_stub.get_by_survey_id.return_value = answers

        return GetSurveyReportInteractor(
            id_provider,
            survey_repo_stub,
            question_repo_stub,
            answer_repo_stub,
        )

    return factory


async def test_get_survey_report_with_owner(
    make_interactor, uuid_generator, faker: Faker
):
    # Arrange
    owner_id = faker.telegram_id()
    survey_id = uuid_generator()
    first_user = make_user()
    second_user = make_user()
    first_question = make_question()
    second_question = make_question()

    first_answer = make_answer(
        user=first_user.id,
        survey=survey_id,
        selections={first_question.id: 0, second_question.id: 1},
    )
    second_answer = make_answer(
        user=second_user.id, survey=survey_id, selections={first_question.id: 1}
    )

    survey = make_survey(
        id=survey_id, author=owner_id, questions=[first_question.id, second_question.id]
    )

    report_dto = SurveyReportDTO(
        name=survey.name,
        author=survey.author,
        survey=survey.id,
        selections={
            first_user.id: first_answer.selections,
            second_user.id: second_answer.selections,
        },
    )

    interactor = make_interactor(owner_id, survey, [first_answer, second_answer])

    # Act
    result = await interactor(survey_id)

    # Assert
    assert result == report_dto


async def test_get_survey_report_with_stranger(
    make_interactor, uuid_generator, faker: Faker
):
    # Arrange
    owner_id = faker.unique.telegram_id()
    stranger_id = faker.unique.telegram_id()
    survey_id = uuid_generator()
    first_user = make_user()
    second_user = make_user()
    first_question = make_question()
    second_question = make_question()

    first_answer = make_answer(
        user=first_user.id,
        survey=survey_id,
        selections={first_question.id: 0, second_question.id: 1},
    )
    second_answer = make_answer(
        user=second_user.id, survey=survey_id, selections={first_question.id: 1}
    )

    survey = make_survey(
        id=survey_id, author=owner_id, questions=[first_question.id, second_question.id]
    )
    interactor = make_interactor(stranger_id, survey, [first_answer, second_answer])

    # Act
    with pytest.raises(AccessDeniedError):
        await interactor(survey_id)
