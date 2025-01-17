from typing import TYPE_CHECKING

from db.models.base import BaseCommonID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from types_custom import IDType

if TYPE_CHECKING:
    from db.models.buildings import Building


class Room(BaseCommonID):
    name: Mapped[str] = mapped_column(nullable=False)
    building_id: Mapped[IDType]
    building: Mapped['Building'] = relationship(back_populates='rooms')
