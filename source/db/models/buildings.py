from typing import TYPE_CHECKING

from db.models.base import BaseCommonID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models.rooms import Rooms


class Buildings(BaseCommonID):
    name: Mapped[str] = mapped_column(nullable=False)
    rooms: Mapped[list['Rooms']] = relationship(back_populates='building')
