from schemas.buildings_base import BuildingIDBaseSchema

from .rooms_base import RoomBaseSchema


class BuildingSchema(BuildingIDBaseSchema):
    rooms: list[RoomBaseSchema] = []
