from quizer.application.dto.user import UserDTO
from quizer.application.dto.mappers.user import to_user_entity
from quizer.application.interfaces.repositories.user import UserRepository


class RegisterInteractor:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def __call__(self, user_data: UserDTO) -> str:
        return await self._user_repo.add(to_user_entity(user_data))
