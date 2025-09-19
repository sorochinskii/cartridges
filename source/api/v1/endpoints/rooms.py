from apps.user_manager import fastapi_users
from fastapi import APIRouter, Depends
from repositories.repositories import room_repository
from schemas.base import ItemIds
from schemas.rooms_base import RoomIDBaseSchema, RoomUpdateBaseSchema
from types_custom import IDType

rooms_router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
    dependencies=[
        Depends(
            fastapi_users.authenticator.current_user(active=True, verified=True)
        )
    ],
)


@rooms_router.get("", response_model=list[RoomIDBaseSchema])
async def get_rooms(
    limit: int = 10, offset: int = 0, repository=Depends(room_repository)
):
    rooms = await repository.get_all(offset=offset, limit=limit)
    return rooms


@rooms_router.post("/batch", response_model=list[RoomIDBaseSchema])
async def get_rooms_batch(
    item_ids: ItemIds, repository=Depends(room_repository)
):
    str_ids = [str(x) for x in item_ids.ids]
    rooms = await repository.get_batch(str_ids)
    return rooms


@rooms_router.post("/batch/create", response_model=list[RoomIDBaseSchema])
async def create_rooms_batch(
    rooms: list[RoomIDBaseSchema], repository=Depends(room_repository)
):
    await repository.batch_create(rooms)
    return rooms


@rooms_router.post("", response_model=RoomIDBaseSchema)
async def create_room(
    room: RoomIDBaseSchema, repository=Depends(room_repository)
):
    await repository.create(room)
    return room


@rooms_router.get("/{room_id}", response_model=RoomIDBaseSchema | None)
async def get_room(room_id: IDType, repository=Depends(room_repository)):
    result = await repository.get_single(id=room_id)
    return result


@rooms_router.put("/{room_id}", response_model=RoomIDBaseSchema)
async def update_room(
    room_id: IDType,
    room: RoomUpdateBaseSchema,
    repository=Depends(room_repository),
):
    result = await repository.update(room, id=room_id, exclude_unset=False)
    return result


@rooms_router.patch("/{room_id}", response_model=RoomIDBaseSchema)
async def patch_room(
    room_id: IDType,
    room: RoomUpdateBaseSchema,
    repository=Depends(room_repository),
):
    result = await repository.update(room, id=room_id, exclude_unset=True)
    return result


@rooms_router.delete("/{room_id}", response_model=IDType)
async def delete_room(room_id: IDType, repository=Depends(room_repository)):
    result = await repository.delete(id=room_id)
    return room_id


@rooms_router.get("/name/{name}", response_model=list[RoomIDBaseSchema])
async def get_rooms_by_name(name: str, repository=Depends(room_repository)):
    result = await repository.get_name_filtered(name)
    return result
