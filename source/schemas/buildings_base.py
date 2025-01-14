from schemas.base import BaseSchema
from types_custom import IDType


class BuildingBaseSchema(BaseSchema):
    name: str


class BuildingIDBaseSchema(BuildingBaseSchema):
    id: IDType
