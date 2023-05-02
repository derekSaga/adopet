import pytest
from dotenv import load_dotenv

load_dotenv("test.env")

from core.config import Settings


@pytest.fixture(scope="module")
def fxt_settings() -> Settings:
    return Settings()
