from enum import Enum

from api.exceptions.schema_validation_errors import PhoneNumberException
from api.models.user_model import UserModel
from phonenumbers import NumberParseException
from phonenumbers import PhoneNumberFormat
from phonenumbers import PhoneNumberType
from phonenumbers import format_number
from phonenumbers import is_valid_number
from phonenumbers import number_type
from phonenumbers import parse as parse_phone_number
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import HttpUrl
from pydantic import constr
from pydantic import validator

MOBILE_NUMBER_TYPES = (
    PhoneNumberType.MOBILE,
    PhoneNumberType.FIXED_LINE_OR_MOBILE,
    PhoneNumberType.FIXED_LINE,
)


class UserSchemaBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: constr(max_length=50, strip_whitespace=True)
    role: str
    about: str
    photo_url: HttpUrl
    # created_at: str
    # updated_at: str

    @validator("photo_url")
    def check_photo_url(cls, value):
        return value

    @validator("phone_number")
    def check_phone_number(cls, value):
        try:
            n = parse_phone_number(value, "BR")
        except NumberParseException as e:
            raise PhoneNumberException from e

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            raise PhoneNumberException

        return format_number(
            n,
            PhoneNumberFormat.NATIONAL
            if n.country_code == 55
            else PhoneNumberFormat.INTERNATIONAL,
        )

    class Config:
        orm_mode = UserModel


class UserTeste(UserSchemaBase):
    role: Enum

    class Config:
        orm_mode = True


class UserSchemaCreate(UserSchemaBase):
    password: str
