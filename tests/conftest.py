import asyncio

import pytest
from dotenv import load_dotenv

load_dotenv("test.env")

from core.config import Settings


@pytest.fixture(scope="module")
def fxt_settings() -> Settings:
    return Settings()


@pytest.fixture(scope="class")
def event_loop_instance(request):
    """ Add the event_loop as an attribute to the unittest style test class. """
    request.cls.event_loop = asyncio.get_event_loop_policy().new_event_loop()
    yield
    request.cls.event_loop.close()
