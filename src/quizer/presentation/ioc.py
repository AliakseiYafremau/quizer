from typing import Protocol, ContextManager
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
from quizer.application.interactors.survey.create_survey import CreateSurveryInteractor
from quizer.application.interactors.survey.delete_survey import DeleteSurveyInteractor
from quizer.application.interactors.survey.finish_survey import AnswerQuestionInteractor
from quizer.application.interactors.survey.get_all_surveys import (
    GetAllSurveysInteractor,
)
from quizer.application.interactors.survey.get_survey_report import (
    GetSurveyReportInteractor,
)
from quizer.application.interactors.survey.update_survey import UpdateSurveyInteractor


class IoC(Protocol):
    @abstractmethod
    def get_user(self, id_provider: IdProvider) -> ContextManager[GetUserInteractor]:
        raise NotImplementedError

    @abstractmethod
    def register(self) -> ContextManager[RegisterInteractor]:
        raise NotImplementedError

    @abstractmethod
    def get_user_surveys(
        self, id_provider: IdProvider
    ) -> ContextManager[GetUserSurveysInteractor]:
        raise NotImplementedError

    @abstractmethod
    def get_surveys_questions(self) -> ContextManager[GetSurveyQuestionsInteractor]:
        raise NotImplementedError

    @abstractmethod
    def create_survey(
        self, id_provider: IdProvider
    ) -> ContextManager[CreateSurveryInteractor]:
        raise NotImplementedError

    @abstractmethod
    def delete_survey(
        self, id_provider: IdProvider
    ) -> ContextManager[DeleteSurveyInteractor]:
        raise NotImplementedError

    @abstractmethod
    def add_question(
        self, id_provider: IdProvider
    ) -> ContextManager[AddSurveyQuestionInteractor]:
        raise NotImplementedError

    @abstractmethod
    def answer_question(
        self, id_provider: IdProvider
    ) -> ContextManager[AnswerQuestionInteractor]:
        raise NotImplementedError

    @abstractmethod
    def get_all_surveys(self) -> ContextManager[GetAllSurveysInteractor]:
        raise NotImplementedError

    @abstractmethod
    def get_survey_report(
        self, id_provider: IdProvider
    ) -> ContextManager[GetSurveyReportInteractor]:
        raise NotImplementedError

    @abstractmethod
    def update_survey(
        self, id_provider: IdProvider
    ) -> ContextManager[UpdateSurveyInteractor]:
        raise NotImplementedError
