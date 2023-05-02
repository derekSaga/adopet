from unittest.mock import MagicMock

import pytest
from dotenv import load_dotenv
from pytest_mock import MockFixture

load_dotenv("test.env")

from core.config import Settings


@pytest.fixture(scope="module")
def fxt_settings() -> Settings:
    return Settings()


@pytest.fixture
def fxt_create_async_engine(fxt_settings: Settings, mocker: MockFixture) -> MagicMock:
    new_mock = MagicMock()
    mocked_build_publisher = mocker.patch("core.deps.create_async_engine", autospec=True)
    mocked_build_publisher.return_value = new_mock
    return mocked_build_publisher
