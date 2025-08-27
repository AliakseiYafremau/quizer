from faker import Faker

from unittest.mock import create_autospec

from factories import make_user

from quizer.application.interactors.user.update_user import UpdateUserInteractor
from quizer.application.interfaces.common.id_provider import IdProvider
from quizer.application.interfaces.repositories.user import UserRepository


async def test_user_update(faker: Faker):
    old_name = faker.unique.name()
    new_name = faker.unique.name()
    user = make_user(name=old_name)
    user_repo_mock = create_autospec(UserRepository)
    id_provider = create_autospec(IdProvider)
    user_repo_mock.get_by_id.return_value = user
    interactor = UpdateUserInteractor(id_provider, user_repo_mock)

    await interactor(new_name)

    user_repo_mock.update.assert_called_once()
    new_user = user_repo_mock.update.call_args.args[0]
    assert new_user.name == new_name
