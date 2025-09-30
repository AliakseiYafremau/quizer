from uuid import UUID

from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.interfaces.repositories.question import QuestionRepository
from quizer.application.interfaces.repositories.answer import AnswerRepository
from quizer.application.dto.survey import SurveyReportDTO
from quizer.application.exceptions import TargetNotFoundError


class GetSurveyReportInteractor:
    def __init__(
        self,
        id_provider: IdProvider,
        survey_repo: SurveyRepository,
        question_repo: QuestionRepository,
        answer_repo: AnswerRepository,
    ):
        self._id_provider = id_provider
        self._survey_repo = survey_repo
        self._question_repo = question_repo
        self._answer_repo = answer_repo

    async def __call__(self, survey_id: UUID) -> SurveyReportDTO:
        user_id = self._id_provider.get_current_user_id()
        survey = await self._survey_repo.get_by_id(survey_id)
        if survey is None:
            raise TargetNotFoundError("Survey was not found")

        survey.can_manage(user_id)
        answers = await self._answer_repo.get_by_survey_id(survey_id)

        selections = tuple((answer.user, answer.selections) for answer in answers)
        report_dto = SurveyReportDTO(
            name=survey.name,
            author=survey.author,
            survey=survey.id,
            selections=selections,
        )
        return report_dto
