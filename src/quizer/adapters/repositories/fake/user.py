from quizer.entities.user import User
from quizer.application.interfaces.repositories.user import UserRepository


class FakeUserRepository(UserRepository):
    async def get_by_id(self, id: str):
        return User(
            id=id,
            name="name",
        )

    async def add(self, user: User):
        return user.id
