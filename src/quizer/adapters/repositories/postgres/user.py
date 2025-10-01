import psycopg

from quizer.entities.user import User
from quizer.application.interfaces.repositories.user import UserRepository
from quizer.application.factories.user import UserFactory


class SQLUserRepository(UserRepository):
    def __init__(self, session: psycopg.AsyncCursor):
        self.session = session

    async def get_by_id(self, id: str) -> User | None:
        await self.session.execute("SELECT id, name FROM users WHERE id = &s", (id,))
        row = await self.session.fetchone()
        if row is not None:
            return UserFactory().create_user(id=row[0], name=row[1])
        return None

    async def add(self, user: User) -> str:
        await self.session.execute(
            "INSERT INTO users (id, name) FROM (&s, &s)", (user.id, user.name)
        )
        return user.id
