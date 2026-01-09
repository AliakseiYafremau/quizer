from typing import Protocol, AsyncContextManager
from abc import abstractmethod

from quizer.application.interfaces.common.id_provider import IdProvider

from quizer.application.interactors.user.get_user import GetUserInteractor
from quizer.application.interactors.user.register import RegisterInteractor
from quizer.application.interactors.user.get_user_surveys import (
    GetUserSurveysInteractor,
)
from quizer.application.interactors.question.get_survey_questions import (
    GetSurveyQuestionsInteractor,
)
from quizer.application.interactors.question.add_question import (
    AddSurveyQuestionInteractor,
)
from quizer.application.interactors.question.update_question import (
    UpdateQuestionInteractor,
)
from quizer.application.interactors.question.delete_question import (
    DeleteQuestionInteractor,
)
from quizer.application.interactors.survey.create_survey import CreateSurveryInteractor
from quizer.application.interactors.survey.delete_survey import DeleteSurveyInteractor
from quizer.application.interactors.survey.answer_question import (
    AnswerQuestionInteractor,
)
from quizer.application.interactors.survey.finish_survey import SaveSurveyInteractor
from quizer.application.interactors.survey.get_all_surveys import (
    GetAllSurveysInteractor,
)
from quizer.application.interactors.survey.get_survey_report import (
    GetSurveyReportInteractor,
)
from quizer.application.interactors.survey.update_survey import UpdateSurveyInteractor


class IoC(Protocol):
    @abstractmethod
    def get_user(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[GetUserInteractor]:
        raise NotImplementedError

    @abstractmethod
    def register(self) -> AsyncContextManager[RegisterInteractor]:
        raise NotImplementedError

    @abstractmethod
    def get_user_surveys(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[GetUserSurveysInteractor]:
        raise NotImplementedError

    @abstractmethod
    def get_surveys_questions(
        self,
    ) -> AsyncContextManager[GetSurveyQuestionsInteractor]:
        raise NotImplementedError

    @abstractmethod
    def create_survey(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[CreateSurveryInteractor]:
        raise NotImplementedError

    @abstractmethod
    def save_survey(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[SaveSurveyInteractor]:
        raise NotImplementedError

    @abstractmethod
    def delete_survey(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[DeleteSurveyInteractor]:
        raise NotImplementedError

    @abstractmethod
    def add_question(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[AddSurveyQuestionInteractor]:
        raise NotImplementedError

    @abstractmethod
    def update_question(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[UpdateQuestionInteractor]:
        raise NotImplementedError

    @abstractmethod
    def delete_question(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[DeleteQuestionInteractor]:
        raise NotImplementedError

    @abstractmethod
    def answer_question(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[AnswerQuestionInteractor]:
        raise NotImplementedError

    @abstractmethod
    def get_all_surveys(self) -> AsyncContextManager[GetAllSurveysInteractor]:
        raise NotImplementedError

    @abstractmethod
    def get_survey_report(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[GetSurveyReportInteractor]:
        raise NotImplementedError

    @abstractmethod
    def update_survey(
        self, id_provider: IdProvider
    ) -> AsyncContextManager[UpdateSurveyInteractor]:
        raise NotImplementedError
