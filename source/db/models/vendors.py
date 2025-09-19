from db.models.base import BaseCommonID
from db.models.cartridges import Cartridge
from db.models.devices import Device
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Vendor(BaseCommonID):
    name: Mapped[str] = mapped_column()
    devices: Mapped[list["Device"]] = relationship(back_populates="vendor")
    cartridges: Mapped[list["Cartridge"]] = relationship(
        back_populates="vendor")
