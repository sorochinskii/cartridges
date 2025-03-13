from typing import TYPE_CHECKING

from db.models.base import BaseCommonID
from sqlalchemy.orm import Mapped, mapped_column


class Employee(BaseCommonID):
    name: Mapped[str] = mapped_column(nullable=False)
    personnel_number: Mapped[str] = mapped_column(unique=True)
