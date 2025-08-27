from faker import Faker

from unittest.mock import create_autospec

from factories import make_survey

from quizer.application.interactors.survey.create_survey import CreateSurveryInteractor
from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.survey import SurveyRepository
from quizer.application.interfaces.factories.survey import SurveyFactory


async def test_survery_creation(faker: Faker):
    survey_name = faker.sentence()
    id_provider = create_autospec(IdProvider)
    survey_repo_mock = create_autospec(SurveyRepository)
    survey_factory_mock = create_autospec(SurveyFactory)
    survey_factory_mock.create_survey.return_value = make_survey(name=survey_name)
    interactor = CreateSurveryInteractor(
        id_provider, survey_repo_mock, survey_factory_mock
    )

    await interactor(survey_name)

    survey_repo_mock.add.assert_called_once()
    new_survey = survey_repo_mock.add.call_args.args[0]
    assert new_survey.name == survey_name
