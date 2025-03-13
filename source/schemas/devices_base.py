from schemas.base import BaseSchema
from types_custom import IDType


class DeviceBaseSchema(BaseSchema):
    name: str
    serial: str


class DeviceIDBaseSchema(DeviceBaseSchema):
    id: IDType


class DeviceUpdateBaseSchema(DeviceBaseSchema):
    ...
