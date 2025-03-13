from typing import TYPE_CHECKING

from db.models.base import BaseCommonID
from db.models.devices import Device
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from types_custom import IDType

if TYPE_CHECKING:
    from db.models.vendors import Vendor


class Cartridge(BaseCommonID):
    name: Mapped[str] = mapped_column()
    serial: Mapped[str] = mapped_column()
    device_id: Mapped[IDType | None] = mapped_column(
        ForeignKey('device.id'))
    device: Mapped['Device'] = relationship(
        back_populates='cartridges',
        foreign_keys=[device_id])
    vendor_id: Mapped[IDType | None] = mapped_column(
        ForeignKey('vendor.id'))
    vendor: Mapped['Vendor'] = relationship(
        back_populates='cartridges',
        foreign_keys=[vendor_id])
