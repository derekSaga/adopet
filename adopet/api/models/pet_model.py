from api.models.animal_specie_model import AnimalSpecieModel
from api.models.base_model import StandardModelMixin
from api.models.city_model import CityModel
from api.models.size_model import SizeModel
from api.models.state_model import StateModel
from api.models.status_model import StatusModel
from api.models.user_model import UserModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import types
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

BASE = declarative_base(cls=StandardModelMixin)


class PetModel(BASE):
    __tablename__ = "pet"
    photo_url = Column(URLType, nullable=True)
    name = Column(types.String(155), nullable=False)
    personality = Column(types.String, nullable=False)

    owner_id = mapped_column(types.UUID, ForeignKey(UserModel.id, ondelete="CASCADE"))
    specie_id = mapped_column(
        types.UUID, ForeignKey(AnimalSpecieModel.id, ondelete="CASCADE")
    )
    status_id = mapped_column(
        types.UUID, ForeignKey(StatusModel.id, ondelete="CASCADE")
    )
    size_id = mapped_column(types.UUID, ForeignKey(SizeModel.id, ondelete="CASCADE"))
    state_id = mapped_column(types.UUID, ForeignKey(StateModel.id, ondelete="CASCADE"))
    city_id = mapped_column(types.UUID, ForeignKey(CityModel.id, ondelete="CASCADE"))

    owner = relationship("UserModel", back_populates="pets")
