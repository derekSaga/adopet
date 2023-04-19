from api.enums.animal_species import AnimalSpecieEnum
from api.models.base_model import StandardModelMixin
from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy.orm import declarative_base

BASE = declarative_base(cls=StandardModelMixin)


class AnimalSpecieModel(BASE):
    __tablename__ = "animal_specie"

    name = Column(
        types.Enum(
            AnimalSpecieEnum, values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
    )
