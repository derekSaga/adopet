from typing import Any
from typing import Dict
from typing import Union

import pytest
from api.schemas.v1.token_schema import UserOut
from pydantic import ValidationError


class TestUserOut:
    def test_should_validate_serialized_values(
        self, fxt_valid_user_out: Dict[str, Any]
    ):
        serialized = UserOut(**fxt_valid_user_out)

        assert serialized.email == fxt_valid_user_out.get("email")
        assert serialized.id == fxt_valid_user_out.get("id")

    @pytest.mark.parametrize(
        argnames="dict_key,invalid_value",
        argvalues=[("email", "invalid_email"), ("id", None)],
    )
    def test_should_raise_exception_when_receive_invalid_data(
        self,
        dict_key: str,
        invalid_value: Union[str, None],
        fxt_valid_user_out: Dict[str, Any],
    ):
        fxt_valid_user_out.update({dict_key: invalid_value})
        with pytest.raises(ValidationError) as error:
            UserOut(**fxt_valid_user_out)

        assert "validation error for UserOut" in error.value.__str__()
