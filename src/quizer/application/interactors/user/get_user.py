from quizer.application.dto.user import UserDTO
from quizer.application.dto.mappers.user import to_user_dto
from quizer.application.interfaces.repositories.user import UserRepository
from quizer.application.interfaces.common.id_provider import IdProvider


class GetUserInteractor:
    def __init__(self, id_provider: IdProvider, user_repo: UserRepository):
        self._user_repo = user_repo
        self._id_provider = id_provider

    async def __call__(self) -> UserDTO:
        user_id = self._id_provider.get_current_user_id()
        user = await self._user_repo.get_by_id(user_id)
        return to_user_dto(user)
