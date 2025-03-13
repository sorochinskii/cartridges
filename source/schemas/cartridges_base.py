from schemas.base import BaseSchema
from types_custom import IDType


class CartridgeBaseSchema(BaseSchema):
    name: str
    serial: str


class CartridgeIDBaseSchema(CartridgeBaseSchema):
    id: IDType


class CartridgeUpdateBaseSchema(CartridgeBaseSchema):
    ...
