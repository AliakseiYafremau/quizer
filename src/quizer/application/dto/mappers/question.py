from quizer.entities.survey import Question
from quizer.application.dto.question import ReadQuestionDTO


def to_question_dto(question: Question):
    return ReadQuestionDTO(
        id=question.id,
        name=question.name,
        options=question.options,
    )
