from uuid import UUID

from quizer.entities.survey import Survey
from quizer.application.interfaces.repositories.survey import SurveyRepository


class FakeSurveyRepository(SurveyRepository):
    async def get_by_id(self, id: UUID):
        return Survey(
            id=id,
            name="name",
            author="author",
            questions=[],
        )

    async def get_all(self):
        return []

    async def add(self, survey: Survey):
        return survey.id

    async def update(self, survey):
        pass

    async def delete(self, id):
        pass
