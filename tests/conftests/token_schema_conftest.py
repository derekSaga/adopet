import uuid
from datetime import datetime
from typing import Any
from typing import Dict

import pytest
from faker import Faker

myFactory = Faker(locale="pt_BR")


@pytest.fixture
def fxt_valid_token_schema() -> Dict[str, str]:
    return {
        "access_token": uuid.uuid4().__str__(),
        "refresh_token": uuid.uuid4().__str__(),
    }


@pytest.fixture
def fxt_invalid_token_schema() -> Dict[str, str]:
    return {
        "access_token": None,
        "refresh_token": "",
    }


@pytest.fixture
def fxt_valid_token_payload() -> Dict[str, Any]:
    return {
        "sub": myFactory.email(),
        "exp": datetime.utcnow().timestamp(),
    }


@pytest.fixture
def fxt_valid_user_auth() -> Dict[str, Any]:
    return {
        "email": myFactory.email(),
        "password": myFactory.password(),
    }


@pytest.fixture
def fxt_valid_user_out() -> Dict[str, Any]:
    return {
        "email": myFactory.email(),
        "id": uuid.uuid4(),
    }


@pytest.fixture
def fxt_system_user(fxt_valid_user_out: Dict[str, Any]) -> Dict[str, Any]:
    fxt_valid_user_out.update({"password": uuid.uuid4().__str__()})
    return fxt_valid_user_out
