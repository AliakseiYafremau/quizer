from faker import Faker

from unittest.mock import create_autospec

from quizer.application.dto.user import UserDTO
from quizer.application.dto.mappers.user import to_user_entity

from quizer.application.interfaces.repositories.user import UserRepository
from quizer.application.interactors.user.register import RegisterInteractor


async def test_user_registration(faker: Faker):
    # Arrange
    user_dto = UserDTO(faker.telegram_id(), faker.name())
    user = to_user_entity(user_dto)

    user_repo_mock = create_autospec(UserRepository)

    interactor = RegisterInteractor(user_repo_mock)

    # Act
    await interactor(user_dto)

    # Assert
    user_repo_mock.add.assert_called_once_with(user)
