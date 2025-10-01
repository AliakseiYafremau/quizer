from quizer.entities.user import User


class UserFactory:
    def create_user(self, id: str, name: str):
        return User(id=id, name=name)
