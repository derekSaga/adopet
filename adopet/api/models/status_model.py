from sqlalchemy import Column, types
from sqlalchemy.orm import declarative_base

from api.enums.status_enum import StatusEnum
from api.models.base_model import StandardModelMixin

BASE = declarative_base(cls=StandardModelMixin)


class StatusModel(BASE):
    __tablename__ = 'status'

    name = Column(
        types.Enum(
            StatusEnum,
            values_callable=lambda obj: [e.value for e in obj],
            create_constraint=True,
        ),
        nullable=False,
    )
