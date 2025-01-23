from polyfactory.factories.pydantic_factory import ModelFactory
from schemas.rooms_base import RoomIDBaseSchema


class RoomCreateFactory(ModelFactory[RoomIDBaseSchema]):
    __model__ = RoomIDBaseSchema
