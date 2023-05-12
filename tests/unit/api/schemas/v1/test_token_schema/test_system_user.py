from typing import Any
from typing import Dict

import pytest
from api.schemas.v1.token_schema import SystemUser
from pydantic import ValidationError


class TestSystemUser:
    def test_should_validate_serialized_values(self, fxt_system_user: Dict[str, Any]):
        serialized = SystemUser(**fxt_system_user)

        assert serialized.email == fxt_system_user.get("email")
        assert serialized.id == fxt_system_user.get("id")
        assert serialized.password == fxt_system_user.get("password")

    @pytest.mark.parametrize(
        argnames="dict_key,invalid_value",
        argvalues=[("email", "invalid_email"), ("id", None), ("password", None)],
    )
    def test_should_raise_exception_when_receive_invalid_data(
        self, dict_key: str, invalid_value: None, fxt_system_user: Dict[str, Any]
    ):
        fxt_system_user.update({dict_key: invalid_value})
        with pytest.raises(ValidationError) as error:
            SystemUser(**fxt_system_user)

        assert "validation error for SystemUser" in error.value.__str__()
        assert dict_key in error.value.__str__()
