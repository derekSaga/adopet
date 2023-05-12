from unittest.mock import MagicMock

import pytest
from core.config import Settings
from pytest_mock import MockFixture


@pytest.fixture
def fxt_create_async_engine(fxt_settings: Settings, mocker: MockFixture) -> MagicMock:
    new_mock = MagicMock()
    mocked_build_publisher = mocker.patch(
        "core.deps.get_session_db.create_async_engine", autospec=True
    )
    mocked_build_publisher.return_value = new_mock
    return mocked_build_publisher


@pytest.fixture
def fxt_class_async_session(mocker: MockFixture) -> MagicMock:
    new_mock = MagicMock
    mocked = mocker.patch("core.deps.get_session_db.AsyncSession", autospec=True)
    mocked.return_value = new_mock
    return mocked
