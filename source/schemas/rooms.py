from schemas.buildings_base import BuildingIDBaseSchema


class RoomSchema(BuildingIDBaseSchema):
    building: BuildingIDBaseSchema | None
