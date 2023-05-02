from unittest import mock

import pytest
from core.config import Settings
from core.deps import get_session


@pytest.mark.usefixtures("event_loop_instance")
class TestGetSession:
    @pytest.mark.asyncio
    async def test_a(self, fxt_settings: Settings):
        with mock.patch(
                "core.deps.create_async_engine", autospec=True
        ) as fxt_create_async_engine:
            await get_session().__anext__()
        fxt_create_async_engine.assert_called_with(fxt_settings.DB_URL)
