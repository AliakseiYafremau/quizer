from quizer.entities.survey import Survey
from quizer.application.dto.survey import ReadSurveyDTO


def to_survey_dto(survey: Survey):
    return ReadSurveyDTO(
        id=survey.id,
        name=survey.name,
        author=survey.author,
    )
