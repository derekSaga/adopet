from unittest import mock
from unittest.mock import MagicMock

import pytest
from core.config import Settings
from core.deps import get_session


class TestGetSession:
    @pytest.mark.asyncio
    async def test_b(self, fxt_settings: Settings, fxt_create_async_engine: MagicMock):
        _ = [item async for item in get_session()]
        fxt_create_async_engine.assert_called_with(fxt_settings.DB_URL)
