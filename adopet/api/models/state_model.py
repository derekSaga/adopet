from api.enums.state_enum import StateEnum
from api.models.base_model import StandardModelMixin
from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

BASE = declarative_base(cls=StandardModelMixin)


class StateModel(BASE):
    __tablename__ = "state"

    name = Column(
        types.Enum(
            StateEnum,
            values_callable=lambda obj: [e.value for e in obj],
            create_constraint=True,
        ),
        nullable=False,
    )

    cities = relationship(
        "CityModel",
        back_populates="state",
        cascade="all, delete-orphan",
    )
