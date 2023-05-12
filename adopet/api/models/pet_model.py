from uuid import UUID

from api.models.animal_specie_model import AnimalSpecieModel
from api.models.base_model import StandardModelMixin
from api.models.city_model import CityModel
from api.models.size_model import SizeModel
from api.models.state_model import StateModel
from api.models.status_model import StatusModel
from api.models.user_model import UserModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

BASE = declarative_base(cls=StandardModelMixin)


class PetModel(BASE):
    name: Mapped[str]
    photo_url: Mapped[str] = mapped_column(URLType, nullable=False, unique=True)
    personality: Mapped[str]

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey(UserModel.id, ondelete="CASCADE"), nullable=False
    )
    specie_id: Mapped[UUID] = mapped_column(
        ForeignKey(AnimalSpecieModel.id, ondelete="CASCADE"), nullable=False
    )
    status_id: Mapped[UUID] = mapped_column(
        ForeignKey(StatusModel.id, ondelete="CASCADE"), nullable=False
    )
    size_id: Mapped[UUID] = mapped_column(
        ForeignKey(SizeModel.id, ondelete="CASCADE"), nullable=False
    )
    state_id: Mapped[UUID] = mapped_column(
        ForeignKey(StateModel.id, ondelete="CASCADE"), nullable=False
    )
    city_id: Mapped[UUID] = mapped_column(
        ForeignKey(CityModel.id, ondelete="CASCADE"), nullable=False
    )

    owner: Mapped["UserModel"] = relationship(
        back_populates="pets", foreign_keys=[owner_id]
    )
