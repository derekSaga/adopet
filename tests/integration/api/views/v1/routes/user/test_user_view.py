import pytest
import json
from api.models.user_model import UserModel
from core.config import settings
from fastapi import status
from httpx import AsyncClient

from tests.support.utils import user_data_with_password


class TestUserView:
    @pytest.mark.asyncio
    async def test_return_201_when_create_user_success(self, client_test: AsyncClient):
        data = user_data_with_password()
        response = await client_test.post(f"{settings.API_V1_STR}/tutor", data=json.dumps(data))
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == data.get("email")

    @pytest.mark.asyncio
    async def test_returns_409_when_the_email_used_for_registration_already_exists_in_the_base(
        self, client_test: AsyncClient, fxt_user_context: UserModel
    ):
        data = user_data_with_password()

        data["email"] = fxt_user_context.email

        response = await client_test.post(f"{settings.API_V1_STR}/tutor", data=json.dumps(data))

        expected_msg = f"Key (Email)=({fxt_user_context.email.title()}) Already Exists."

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json().get("detail") == expected_msg

    @pytest.mark.asyncio
    async def test_returns_409_when_phone_number_used_for_registration_already_exists_in_the_base(
        self, client_test: AsyncClient, fxt_user_context: UserModel
    ):
        data = user_data_with_password()

        data["phone_number"] = fxt_user_context.phone_number

        response = await client_test.post(f"{settings.API_V1_STR}/tutor", data=json.dumps(data))

        expected_msg = (
            f"Key (Phone_Number)=({fxt_user_context.phone_number}) Already Exists."
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json().get("detail") == expected_msg
