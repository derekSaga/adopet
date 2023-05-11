from typing import Dict
from unittest.mock import MagicMock

import pytest
from api.schemas.v1.user_schema import UserSchemaBase
from phonenumbers import PhoneNumberFormat
from phonenumbers import parse as parse_phone_number
from phonenumbers.phonenumberutil import format_number
from pydantic import ValidationError


class TestUserSchemaBase:
    def test_should_validate_serialized_values(
        self, fxt_user_data_with_password: Dict[str, str]
    ):
        phone_number = parse_phone_number(
            fxt_user_data_with_password.get("phone_number"), "BR"
        )

        final_number = format_number(
            phone_number,
            PhoneNumberFormat.NATIONAL
            if phone_number.country_code == 55
            else PhoneNumberFormat.INTERNATIONAL,
        )

        serialized = UserSchemaBase(**fxt_user_data_with_password)

        assert serialized.name == fxt_user_data_with_password.get("name")
        assert serialized.email == fxt_user_data_with_password.get("email")
        assert serialized.phone_number == final_number
        assert serialized.role == fxt_user_data_with_password.get("role")
        assert serialized.about == fxt_user_data_with_password.get("about")
        assert serialized.photo_url == fxt_user_data_with_password.get("photo_url")

    def test_should_raise_exception_when_receive_invalid_phone_number(
        self, fxt_user_data_with_password: Dict[str, str]
    ):
        fxt_user_data_with_password.update({"phone_number": "wrong"})
        with pytest.raises(ValidationError) as error:
            UserSchemaBase(**fxt_user_data_with_password)

        assert "Please provide a valid mobile phone number" in error.value.__str__()

    def test_should_raise_exception_when_receive_invalid_phone_type(
        self, fxt_user_data_with_password: Dict[str, str], fxt_number_type: MagicMock
    ):
        with pytest.raises(ValidationError) as error:
            UserSchemaBase(**fxt_user_data_with_password)

        assert "Please provide a valid mobile phone number" in error.value.__str__()

    def test_should_raise_exception_when_receive_not_is_valid_number(
        self,
        fxt_user_data_with_password: Dict[str, str],
        fxt_is_valid_number: MagicMock,
    ):
        with pytest.raises(ValidationError) as error:
            UserSchemaBase(**fxt_user_data_with_password)

        assert "Please provide a valid mobile phone number" in error.value.__str__()
