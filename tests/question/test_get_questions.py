from unittest.mock import create_autospec

from tests.factories import make_question, make_survey

from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.dto.mappers.question import to_question_dto
from quizer.application.interactors.question.get_survey_questions import (
    GetSurveyQuestionsInteractor,
)


async def test_recieving_all_questions(uuid_generator):
    # Arrange
    question_ids = [uuid_generator() for _ in range(3)]
    questions = [make_question(id=question_id) for question_id in question_ids]
    survey = make_survey(questions=question_ids)
    questions_dto = list(map(to_question_dto, questions))

    question_repo_stub = create_autospec(QuestionRepository)
    question_repo_stub.get_by_survey_id.return_value = questions

    interactor = GetSurveyQuestionsInteractor(question_repo_stub)

    # Act
    result = await interactor(survey.id)

    # Assert
    assert result == questions_dto
