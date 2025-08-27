from quizer.entities.user import User
from quizer.application.dto.user import UserDTO


def to_user_dto(user: User):
    return UserDTO(
        id=user.id,
        name=user.name,
    )


def to_user_entity(user_data: UserDTO):
    return User(
        id=user_data.id,
        name=user_data.name,
    )
