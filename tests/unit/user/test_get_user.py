from faker import Faker

from unittest.mock import create_autospec

from tests.factories import make_user

from quizer.application.dto.mappers.user import to_user_dto

from quizer.application.interfaces.repositories.user import UserRepository
from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interactors.user.get_user import GetUserInteractor


async def test_user_recieving(faker: Faker):
    # Arrange
    user = make_user()
    user_dto = to_user_dto(user)

    id_provider_stub = create_autospec(IdProvider)
    user_repo_stub = create_autospec(UserRepository)

    user_repo_stub.get_by_id.return_value = user

    interactor = GetUserInteractor(id_provider_stub, user_repo_stub)

    # Act
    result = await interactor()

    # Assert
    assert result == user_dto
