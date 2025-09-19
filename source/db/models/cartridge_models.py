from typing import TYPE_CHECKING

from db.models.base import BaseCommonID
from db.models.cartridges import Cartridge
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from types_custom import IDType


class CartridgeModel(BaseCommonID):
    name: Mapped[str] = mapped_column()
    cartridges: Mapped[list["Cartridge"]] = relationship(
        back_populates="cartridge_model"
    )
    original_id: Mapped[IDType | None] = mapped_column(
        ForeignKey("cartridge_model.id")
    )
    original: Mapped["CartridgeModel"] = relationship(
        foreign_keys=[original_id],
        remote_side="CartridgeModel.id",
        lazy="joined",
    )
