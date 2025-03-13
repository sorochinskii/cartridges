from typing import TYPE_CHECKING

from db.models.base import BaseCommonID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from types_custom import IDType

if TYPE_CHECKING:
    from db.models.cartridges import Cartridge
    from db.models.rooms import Room
    from db.models.vendors import Vendor


class Device(BaseCommonID):
    name: Mapped[str] = mapped_column(nullable=False)
    serial: Mapped[str] = mapped_column(nullable=False)
    room_id: Mapped[IDType | None] = mapped_column(
        ForeignKey('room.id'))
    room: Mapped['Room'] = relationship(back_populates='devices',
                                        foreign_keys=[room_id])
    vendor_id: Mapped[IDType | None] = mapped_column(
        ForeignKey('vendor.id'))
    vendor: Mapped['Vendor'] = relationship(
        back_populates='devices',
        foreign_keys=[vendor_id])
    cartridges: Mapped['Cartridge'] = relationship(back_populates='device')
