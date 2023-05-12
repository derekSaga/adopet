from unittest.mock import MagicMock

import pytest
from core.config import Settings
from core.deps.get_session_db import get_session


class TestGetSession:
    @pytest.mark.asyncio
    async def test_must_validate_url_connection_db(
        self, fxt_settings: Settings, fxt_create_async_engine: MagicMock
    ):
        _ = [item async for item in get_session()]
        fxt_create_async_engine.assert_called_with(fxt_settings.DB_URL)

    @pytest.mark.asyncio
    async def test_must_raise_exception_when_connection_is_refused(
        self, fxt_create_async_engine: MagicMock, fxt_class_async_session: MagicMock
    ):
        fxt_create_async_engine.side_effect = ConnectionRefusedError()
        with pytest.raises(ConnectionRefusedError):
            _ = [item async for item in get_session()]
        fxt_class_async_session.assert_not_called()
