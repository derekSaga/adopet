from typing import Any
from typing import Dict

import pytest
from api.schemas.v1.token_schema import TokenSchema
from pydantic import ValidationError

invalid_values = [None, 1, {}, []]


class TestTokenSchema:
    def test_should_validate_serialized_values(
        self, fxt_valid_token_schema: Dict[str, str]
    ):
        serialized = TokenSchema(**fxt_valid_token_schema)

        assert serialized.refresh_token == fxt_valid_token_schema.get("refresh_token")
        assert serialized.access_token == fxt_valid_token_schema.get("access_token")

    @pytest.mark.parametrize(
        argnames="invalid_value",
        argvalues=invalid_values,
    )
    def test_should_raise_error_when_access_token_is_invalid_data(
        self, invalid_value: Any, fxt_valid_token_schema: Dict[str, str]
    ):
        fxt_valid_token_schema.update({"access_token": invalid_value})

        with pytest.raises(ValidationError) as error:
            TokenSchema(**fxt_valid_token_schema)

        assert "validation error for TokenSchema" in error.value.__str__()

    @pytest.mark.parametrize(
        argnames="invalid_value",
        argvalues=invalid_values,
    )
    def test_should_raise_error_when_refresh_token_is_invalid_data(
        self, invalid_value: Any, fxt_valid_token_schema: Dict[str, str]
    ):
        fxt_valid_token_schema.update({"refresh_token": invalid_value})

        with pytest.raises(ValidationError) as error:
            TokenSchema(**fxt_valid_token_schema)

        assert "validation error for TokenSchema" in error.value.__str__()
