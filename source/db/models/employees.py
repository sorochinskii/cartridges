from db.models.base import BaseCommonID
from db.models.rooms import Room
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from types_custom import IDType


class Employee(BaseCommonID):
    name: Mapped[str] = mapped_column(nullable=False)
    personnel_number: Mapped[str] = mapped_column(nullable=False, unique=True)
    room_id: Mapped[IDType | None] = mapped_column(
        ForeignKey('room.id'))
    room: Mapped['Room'] = relationship(back_populates='rooms')
