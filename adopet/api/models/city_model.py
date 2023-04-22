from api.models.base_model import StandardModelMixin
from api.models.state_model import StateModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import types
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

BASE = declarative_base(cls=StandardModelMixin)


class CityModel(BASE):
    __tablename__ = "city"

    name = Column(types.String, nullable=False)
    state_id = Column(types.UUID, ForeignKey(StateModel.id), nullable=False)
    state = relationship("StateModel", back_populates="cities")
