from schemas.base import BaseSchema
from types_custom import IDType


class RoomBaseSchema(BaseSchema):
    name: str
    building_id: IDType | None = None


class RoomIDBaseSchema(RoomBaseSchema):
    id: IDType


class RoomUpdateBaseSchema(RoomBaseSchema):
    ...
