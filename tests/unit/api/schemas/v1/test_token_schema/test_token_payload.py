from typing import Any
from typing import Dict

from api.schemas.v1.token_schema import TokenPayload


class TestTokenSchema:
    def test_should_validate_serialized_values(
        self, fxt_valid_token_payload: Dict[str, Any]
    ):
        serialized = TokenPayload(**fxt_valid_token_payload)

        assert serialized.sub == fxt_valid_token_payload.get("sub")
        assert serialized.exp == fxt_valid_token_payload.get("exp")
