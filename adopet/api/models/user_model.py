from sqlalchemy import Column, types
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import EmailType, PasswordType, URLType

from api.models.base_model import StandardModelMixin

BASE = declarative_base(cls=StandardModelMixin)


class UserModel(BASE):
    __tablename__ = 'user'
    name = Column(types.String(155), nullable=False)
    email = Column(EmailType, nullable=False, index=True, unique=True)
    phone_number = Column(types.String, nullable=False)
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt'],
        max_length=8
    ))
    role = Column(types.String, nullable=False)
    about = Column(types.String, nullable=False)
    phot_url = Column(URLType, nullable=True)
