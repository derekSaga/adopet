from api.enums.size_enum import SizeEnum
from api.models.base_model import StandardModelMixin
from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy.orm import declarative_base

BASE = declarative_base(cls=StandardModelMixin)


class SizeModel(BASE):
    __tablename__ = "size"

    name = Column(
        types.Enum(
            SizeEnum,
            values_callable=lambda obj: [e.value for e in obj],
            create_constraint=True,
        ),
        nullable=False,
    )
