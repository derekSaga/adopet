from typing import Any
from typing import Dict

import pytest
from api.schemas.v1.token_schema import UserAuth
from pydantic import ValidationError


class TestUserAuth:
    def test_should_validate_serialized_values(
        self, fxt_valid_user_auth: Dict[str, Any]
    ):
        serialized = UserAuth(**fxt_valid_user_auth)

        assert serialized.email == fxt_valid_user_auth.get("email")
        assert serialized.password == fxt_valid_user_auth.get("password")

    @pytest.mark.parametrize(
        argnames="dict_key,invalid_value",
        argvalues=[("email", "invalid_email"), ("password", None)],
    )
    def test_should_raise_exception_when_receive_invalid_data(
        self, dict_key: str, invalid_value: None, fxt_valid_user_auth: Dict[str, Any]
    ):
        fxt_valid_user_auth.update({dict_key: invalid_value})
        with pytest.raises(ValidationError) as error:
            UserAuth(**fxt_valid_user_auth)

        assert "validation error for UserAuth" in error.value.__str__()
