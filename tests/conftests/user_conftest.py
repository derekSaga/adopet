from typing import Any
from typing import Dict
from typing import List
from typing import Union
from unittest.mock import MagicMock

import pytest
from api.models.repositories.user_repository import UserRepository
from api.models.user_model import UserModel
from api.schemas.v1.user_schema import MOBILE_NUMBER_TYPES
from api.schemas.v1.user_schema import UserSchemaCreate
from api.views.v1.utils.auth import get_hashed_password
from core.config import Settings
from faker import Faker
from pytest_mock import MockFixture
from sqlalchemy.ext.asyncio import AsyncSession

from tests.support.utils import user_data_with_password

myFactory = Faker(locale="pt_BR")


@pytest.fixture
def fxt_is_valid_number(fxt_settings: Settings, mocker: MockFixture) -> MagicMock:
    mocked_build_publisher = mocker.patch(
        "api.schemas.v1.user_schema.is_valid_number", autospec=True, return_value=False
    )

    return mocked_build_publisher


@pytest.fixture
def fxt_number_type(fxt_settings: Settings, mocker: MockFixture) -> MagicMock:
    value = max(MOBILE_NUMBER_TYPES) + 1
    mocked_build_publisher = mocker.patch(
        "api.schemas.v1.user_schema.number_type", autospec=True, return_value=value
    )

    return mocked_build_publisher


@pytest.fixture(autouse=True)
def fxt_user_data_with_password() -> Dict[str, Any]:
    user_data = UserSchemaCreate(**user_data_with_password())
    return user_data.dict()


@pytest.fixture(autouse=True)
async def fxt_user_repository(fxt_async_session: AsyncSession) -> UserRepository:
    return UserRepository(fxt_async_session)


@pytest.fixture(autouse=True)
async def fxt_bulk_insert_users(
    fxt_user_repository: UserRepository,
) -> List[Union[UserModel, List]]:
    users_result: List[Union[UserModel, List]] = []
    for _ in range(10):
        user = await fxt_user_repository.create_user(
            UserModel(**user_data_with_password())
        )
        users_result += [user]

    yield users_result

    for user in users_result:
        await fxt_user_repository.delete_user_by_email(user.email)


@pytest.fixture(autouse=True)
async def fxt_user_context(
    fxt_async_session: AsyncSession,
    fxt_user_data_with_password: Dict[str, Any],
    fxt_user_repository: UserRepository,
) -> UserModel:
    new_user = UserModel(**fxt_user_data_with_password)
    await fxt_user_repository.create_user(new_user)
    yield new_user
    await fxt_user_repository.delete_user_by_email(email=new_user.email)


@pytest.fixture
def fxt_user_email(fxt_user_context: UserModel) -> str:
    return fxt_user_context.email


@pytest.fixture(autouse=True)
async def test_user(
    fxt_async_session: AsyncSession, fxt_settings: Settings
) -> UserModel:
    new_user = UserModel(**user_data_with_password())
    new_user.metadata.schema = fxt_settings.DATABASE_SCHEMA

    new_user.password = get_hashed_password(new_user.password)

    user_repo = UserRepository(fxt_async_session)

    existing_user = await user_repo.get_user_by_email(email=new_user.email)

    new_user.photo_url = "da.com"

    unique_url_photo = await user_repo.check_value_is_unique(
        "photo_url", new_user.photo_url
    )

    while unique_url_photo is not None:
        new_user.photo_url = myFactory.domain_name()

        unique_url_photo = await user_repo.check_value_is_unique(
            "photo_url", new_user.photo_url
        )
    if existing_user is None:
        existing_user = await user_repo.create_user(new_user)

    yield existing_user

    await user_repo.delete_user_by_email(email=new_user.email)
