from schemas.base import BaseSchema
from types_custom import IDType


class VendorBaseSchema(BaseSchema):
    name: str


class VendorIDBaseSchema(VendorBaseSchema):
    id: IDType


class VendorUpdateBaseSchema(VendorBaseSchema):
    ...
