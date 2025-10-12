import psycopg

from quizer.entities.user import User
from quizer.application.interfaces.repositories.user import UserRepository
from quizer.application.factories.user import UserFactory


class SQLUserRepository(UserRepository):
    def __init__(self, session: psycopg.AsyncCursor, user_factory: UserFactory):
        self.session = session
        self.user_factory = user_factory

    async def get_by_id(self, id: str) -> User | None:
        await self.session.execute("SELECT id, name FROM users WHERE id = %s", (id,))
        row = await self.session.fetchone()
        if row is None:
            return None
        return self.user_factory.create_user(id=row[0], name=row[1])

    async def add(self, user: User) -> str:
        await self.session.execute(
            "INSERT INTO users (id, name) VALUES (&s, &s)", (user.id, user.name)
        )
        return user.id
