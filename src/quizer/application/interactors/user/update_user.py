from quizer.application.interfaces.repositories.user import UserRepository
from quizer.application.interfaces.common.id_provider import IdProvider


class UpdateUserInteractor:
    def __init__(self, id_provider: IdProvider, user_repo: UserRepository):
        self._id_provider = id_provider
        self._user_repo = user_repo

    async def __call__(self, name: str) -> None:
        user_id = self._id_provider.get_current_user_id()
        user = await self._user_repo.get_by_id(user_id)
        user.update_name(name)
        await self._user_repo.update(user)
