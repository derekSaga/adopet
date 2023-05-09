import datetime
from datetime import timedelta
from unittest import mock
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

import pytest
from api.models.user_model import UserModel
from core.config import Settings
from core.deps.get_current_user import get_current_user_request
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.freeze_time("2017-05-21")
class TestGetCurrentUser:
    @pytest.mark.asyncio
    async def test_must_validate_return_from_token_validation_when_validation_succeeds(
        self,
        normal_user_token_headers: str,
        fxt_async_session: AsyncSession,
        test_user: UserModel,
    ):
        with mock.patch("core.deps.get_current_user.datetime") as mock_datetime:
            mock_datetime.utcnow.return_value = datetime.datetime.utcnow() - timedelta(
                hours=8
            )

            mock_datetime.fromtimestamp.return_value = (
                datetime.datetime.utcnow() + timedelta(hours=8)
            )

        result = await get_current_user_request(
            normal_user_token_headers, fxt_async_session
        )
        assert result.email == test_user.email

    @pytest.mark.asyncio
    async def test_must_raise_401_exception_when_token_date_expired(
        self,
        normal_user_token_headers: str,
        fxt_async_session: AsyncSession,
        test_user: UserModel,
    ):
        with mock.patch("core.deps.get_current_user.datetime") as mock_datetime:
            mock_datetime.utcnow.return_value = datetime.datetime.utcnow() + timedelta(
                hours=8
            )
            mock_datetime.fromtimestamp.return_value = (
                datetime.datetime.utcnow() - timedelta(hours=8)
            )
            with pytest.raises(HTTPException) as error:
                await get_current_user_request(
                    normal_user_token_headers, fxt_async_session
                )
        assert error.value.status_code == 401
        assert error.value.detail == "Token expired"
        assert error.value.headers == {"WWW-Authenticate": "Bearer"}

        mock_datetime.fromtimestamp.assert_called()
        mock_datetime.utcnow.assert_called()

    @mock.patch(
        "core.deps.get_current_user.jwt.decode",
    )
    @pytest.mark.asyncio
    async def test_must_raise_404_when_user_not_found(
        self,
        mock_jose_jwt: MagicMock,
        normal_user_token_headers: str,
        fxt_async_session: AsyncSession,
        test_user: UserModel,
        fxt_settings: Settings,
    ):
        mock_jose_jwt.return_value = {
            "sub": "invalid_email",
            "exp": (
                datetime.datetime.utcnow() + datetime.timedelta(hours=3)
            ).timestamp(),
        }

        mock_async = AsyncMock()
        normal_mock = MagicMock()
        normal_mock.scalars.return_value.unique.return_value.one_or_none.return_value = (
            None
        )
        mock_async.execute.return_value = normal_mock

        query = select(UserModel).where(UserModel.email == "invalid_email")

        with pytest.raises(HTTPException) as error:
            await get_current_user_request(normal_user_token_headers, mock_async)

        mock_jose_jwt.assert_called_with(
            token=normal_user_token_headers,
            key=fxt_settings.JWT_SECRET_KEY,
            algorithms=[fxt_settings.ALGORITHM],
        )

        assert mock_async.execute.call_args[0][0].__str__() == query.__str__()
        assert error.value.status_code == 404
        assert error.value.detail == "Could not find user"
