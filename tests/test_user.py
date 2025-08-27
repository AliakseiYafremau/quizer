from faker import Faker

from unittest.mock import create_autospec

from factories import make_user

from quizer.application.dto.user import UserDTO
from quizer.application.dto.mappers.user import to_user_entity
from quizer.application.dto.mappers.user import to_user_dto

from quizer.application.interfaces.repositories.user import UserRepository
from quizer.application.interfaces.common.id_provider import IdProvider

from quizer.application.interactors.user.register import RegisterInteractor
from quizer.application.interactors.user.get import GetUserInteractor


async def test_register_user(faker: Faker):
    user_dto = UserDTO(faker.telegram_id(), faker.name())
    user = to_user_entity(user_dto)
    user_repo_mock = create_autospec(UserRepository)
    user_repo_mock.add.return_value = user_dto.id
    interactor = RegisterInteractor(user_repo_mock)

    result = await interactor(user_dto)

    assert result == user_dto.id
    user_repo_mock.add.assert_called_once_with(user)


async def test_get_user(faker: Faker):
    user = make_user()
    user_dto = to_user_dto(user)
    id_provider_stub = create_autospec(IdProvider)
    user_repo_stub = create_autospec(UserRepository)
    user_repo_stub.get_by_id.return_value = user
    interactor = GetUserInteractor(id_provider_stub, user_repo_stub)

    result = await interactor()

    assert result == user_dto
