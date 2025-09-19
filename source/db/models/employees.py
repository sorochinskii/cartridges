from typing import TYPE_CHECKING

from db.models.base import BaseCommonID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models.cartridges import Cartridge
class Employee(BaseCommonID):
    name: Mapped[str] = mapped_column(nullable=False)
    personnel_number: Mapped[str | None] = mapped_column(unique=True)
    cartridges: Mapped[list["Cartridge"]] = relationship(
        back_populates="employee")