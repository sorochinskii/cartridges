from datetime import datetime
from typing import Annotated, Any
from uuid import uuid4

from sqlalchemy import func, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from types_custom import IDType
from utils import split_and_concatenate


class Base(DeclarativeBase):
    ...


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        try:
            if (not cls.__mapper_args__.get('polymorphic_abstract')
                    and (cls.__mapper_args__.get('polymorphic_identity')
                         and cls.__mapper_args__.get('polymorphic_on'))):
                return split_and_concatenate(cls.__name__)
        except AttributeError:
            return split_and_concatenate(cls.__name__)


class IDMixin:
    __abstract__ = True

    id: Mapped[IDType] = mapped_column(primary_key=True, unique=True)


class BaseCommon(Base, TableNameMixin, IDMixin):
    __abstract__ = True

    @classmethod
    def tablename(cls):
        return cls.__tablename__


class BaseCommonID(BaseCommon, IDMixin):
    __abstract__ = True


created_at = Annotated[
    datetime,
    mapped_column(nullable=False, server_default=func.now())
]


updated_at = Annotated[
    datetime,
    mapped_column(nullable=False, server_default=func.now(),
                  onupdate=func.now())
]
