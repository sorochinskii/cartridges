from pydantic import BaseModel
from schemas.mixins import OptionalFieldsMixin
from types_custom import IDType


class BaseSchema(BaseModel, OptionalFieldsMixin):
    ...

class ItemIds(BaseModel):
    ids: list[IDType]