from typing import TypeAlias, TypeVar
from uuid import UUID

# from db.models.base import Base
from pydantic import BaseModel

IDType: TypeAlias = UUID

# ORMModel: TypeAlias = Base
# ORMModel = TypeVar('ORMModel', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
GetSchemaType = TypeVar('GetSchemaType', bound=BaseModel)
