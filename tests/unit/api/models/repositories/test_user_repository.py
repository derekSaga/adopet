from typing import Any
from typing import Dict

import pytest
from api.models.repositories.user_repository import UserRepository
from api.models.user_model import UserModel
from faker import Faker
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
    async def test_c(
        self,
        fxt_user_repository: UserRepository,
        fxt_user_data_with_password: Dict[str, Any],
    ):
        new_user = UserModel(**user_data_with_password())

        new_user = await fxt_user_repository.create_user(new_user)

        await fxt_user_repository.delete_user_by_email(new_user.email)

        result = await fxt_user_repository.get_user_by_unique_constraint(new_user)
        assert result is None
