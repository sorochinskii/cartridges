from schemas.cartridge_models_base import CartridgeModelIDBaseSchema
from types_custom import IDType


class CartridgeModelSchemaCreate(CartridgeModelIDBaseSchema):
    original_id: IDType | None


class CartridgeModelSchema(CartridgeModelIDBaseSchema):
    original_id: IDType | None
    original: CartridgeModelIDBaseSchema | None = None
