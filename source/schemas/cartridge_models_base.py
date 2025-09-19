from schemas.base import BaseSchema
from types_custom import IDType


class CartridgeModelBaseSchema(BaseSchema):
    name: str


class CartridgeModelIDBaseSchema(CartridgeModelBaseSchema):
    id: IDType
