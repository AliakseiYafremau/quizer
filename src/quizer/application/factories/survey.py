from uuid import UUID

from quizer.application.interfaces.common.uuid_generator import UUIDGenerator
from quizer.entities.survey import Survey, Question, Answer


class SurveyFactory:
    def __init__(self, uuid_generator: UUIDGenerator):
        self._uuid_generator = uuid_generator

    def create_survey(self, name: str, author: str, id: UUID | None = None) -> Survey:
        survey_id = id or self._uuid_generator()
        return Survey(
            id=survey_id,
            name=name,
            author=author,
            questions=[],
            is_available=False,
        )


class QuestionFactory:
    def __init__(self, uuid_generator: UUIDGenerator):
        self._uuid_generator = uuid_generator

    def create_question(
        self, name: str, survey: UUID, options: list[str], id: UUID | None = None
    ) -> Question:
        question_id = id or self._uuid_generator()
        return Question(id=question_id, name=name, survey=survey, options=options)


class AnswerFactory:
    def __init__(self, uuid_generator: UUIDGenerator):
        self._uuid_generator = uuid_generator

    def create_answer(
        self,
        user_id: str,
        survey_id: UUID,
        selections: tuple[tuple[UUID, int], ...],
        id: UUID | None = None,
    ) -> Answer:
        answer_id = id or self._uuid_generator()
        return Answer(
            id=answer_id,
            user=user_id,
            survey=survey_id,
            selections=selections,
        )
