from typing import Any
from typing import Dict
from typing import List
from typing import Union

import pytest
from api.enums.user_role_enum import UserRoleEnum
from api.models.repositories.user_repository import UserRepository
from api.models.user_model import UserModel
from faker import Faker
from fastapi_pagination import Params
from sqlalchemy.exc import IntegrityError

from tests.support.utils import user_data_with_password

myFactory = Faker(locale="pt_BR")


class TestUserRepository:
    @pytest.mark.asyncio
    async def test_must_raise_exception_when_method_create_user_violate_unique_constraint(
        self,
        fxt_user_repository: UserRepository,
        test_user: UserModel,
        fxt_user_data_with_password: Dict[str, Any],
    ):
        with pytest.raises(Exception) as error:
            await fxt_user_repository.create_user(
                UserModel(**fxt_user_data_with_password)
            )

        assert isinstance(error.value, (IntegrityError,))

    @pytest.mark.asyncio
    async def test_must_validate_return_from_method_get_user_by_email_when_user_exists(
        self,
        fxt_user_repository: UserRepository,
        fxt_user_email: str,
    ):
        result = await fxt_user_repository.get_user_by_email(fxt_user_email)

        assert result is not None

    @pytest.mark.asyncio
    async def test_must_validate_return_from_method_get_user_by_email_when_user_dont_exists(
        self,
        fxt_user_repository: UserRepository,
        fxt_user_email: str,
    ):
        result = await fxt_user_repository.get_user_by_email("fxt_user_email")

        assert result is None

    @pytest.mark.asyncio
    async def test_should_validate_when_user_is_deleted(
        self,
        fxt_user_repository: UserRepository,
        fxt_user_data_with_password: Dict[str, Any],
    ):
        new_user = UserModel(**user_data_with_password())

        new_user = await fxt_user_repository.create_user(new_user)

        await fxt_user_repository.delete_user_by_email(new_user.email)

        result = await fxt_user_repository.get_user_by_unique_constraint(new_user)
        assert result is None

    @pytest.mark.asyncio
    async def test_must_validate_return_from_get_all_users_method(
        self,
        fxt_bulk_insert_users: List[Union[UserModel, List]],
        fxt_user_repository: UserRepository,
    ):
        repository_result = []

        for value in UserRoleEnum:
            result = await fxt_user_repository.get_all_users(
                value.value, params=Params(size=20)
            )
            repository_result.append(result)

        repository_result = [item.id for pg in repository_result for item in pg.items]

        for fxt_user in fxt_bulk_insert_users:
            assert fxt_user.id in repository_result
