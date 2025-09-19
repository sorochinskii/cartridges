from typing import TYPE_CHECKING

from db.models.base import BaseCommonID
from db.models.buildings import Building
from db.models.devices import Device
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from types_custom import IDType


class Room(BaseCommonID):
    name: Mapped[str] = mapped_column(nullable=False)
    building_id: Mapped[IDType | None] = mapped_column(
        ForeignKey('building.id'))
    building: Mapped['Building'] = relationship(back_populates='rooms')
    devices: Mapped[list['Device']] = relationship(back_populates='room')
