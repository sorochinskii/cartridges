from fastapi import APIRouter, Depends
from repositories.repositories import room_repository
from schemas.rooms_base import RoomBaseSchema, RoomIDBaseSchema, RoomUpdateBaseSchema
from types_custom import IDType

rooms_router = APIRouter(prefix='/rooms', tags=['rooms'])


@rooms_router.get('', response_model=list[RoomIDBaseSchema])
async def get_rooms(repository=Depends(room_repository)):
    rooms = await repository.get_all()
    return rooms


@rooms_router.post('/', response_model=RoomIDBaseSchema)
async def create_room(room: RoomIDBaseSchema,
                      repository=Depends(room_repository)):
    await repository.create(room)
    return room


@rooms_router.get('/{room_id}', response_model=RoomIDBaseSchema | None)
async def get_room(room_id: IDType,
                   repository=Depends(room_repository)):
    result = await repository.get_single(id=room_id)
    return result


@rooms_router.put('/{room_id}', response_model=RoomIDBaseSchema)
async def update_room(room_id: IDType,
                      room: RoomUpdateBaseSchema,
                      repository=Depends(room_repository)):
    result = await repository.update(room, id=room_id, exclude_unset=False)
    return result


@rooms_router.patch('/{room_id}', response_model=RoomIDBaseSchema)
async def patch_room(room_id: IDType,
                     room: RoomUpdateBaseSchema,
                     repository=Depends(room_repository),
                     ):
    result = await repository.update(room, id=room_id, exclude_unset=True)
    return result


@rooms_router.delete('/{room_id}', response_model=IDType)
async def delete_room(room_id: IDType,
                      repository=Depends(room_repository)):
    result = await repository.delete(id=room_id)
    return room_id
