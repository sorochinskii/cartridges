from typing import TYPE_CHECKING

from db.models.base import BaseCommonID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models.rooms import Room


class Building(BaseCommonID):
    name: Mapped[str] = mapped_column(nullable=False)
    rooms: Mapped[list['Room']] = relationship(back_populates='building')
