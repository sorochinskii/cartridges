from fastapi import APIRouter
from schemas.rooms_base import RoomIDBaseSchema

rooms_router = APIRouter(prefix='/rooms', tags=['rooms'])


@rooms_router.get('/', response_model=list[RoomIDBaseSchema])
def get_rooms():
    pass


@rooms_router.post('/', response_model=RoomIDBaseSchema)
def create_room(item: RoomIDBaseSchema):
    pass
