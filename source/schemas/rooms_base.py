from schemas.base import BaseSchema
from types_custom import IDType


class RoomBaseSchema(BaseSchema):
    name: str
    building_id: int | None = None


class RoomIDBaseSchema(RoomBaseSchema):
    id: IDType
