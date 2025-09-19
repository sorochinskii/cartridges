from apps.user_manager import fastapi_users
from fastapi import APIRouter, Depends
from repositories.repositories import building_repository
from schemas.buildings_base import BuildingBaseSchema, BuildingIDBaseSchema
from types_custom import IDType

buildings_router = APIRouter(
    prefix="/buildings",
    tags=["buildings"],
    dependencies=[
        Depends(
            fastapi_users.authenticator.current_user(active=True, verified=True)
        )
    ],
)


@buildings_router.get("", response_model=list[BuildingIDBaseSchema])
async def get_buildings(
    offset: int = 0, limit: int = 10, repository=Depends(building_repository)
):
    buildings = await repository.get_all(offset, limit)
    return buildings


@buildings_router.post("/batch", response_model=list[BuildingIDBaseSchema])
async def get_buildings_batch(
    ids: list[IDType], repository=Depends(building_repository)
):
    str_ids = [str(x) for x in ids]
    buildings = await repository.get_batch(str_ids)
    return buildings


@buildings_router.post(
    "/batch/create", response_model=list[BuildingIDBaseSchema]
)
async def create_rooms_batch(
    rooms: list[BuildingIDBaseSchema], repository=Depends(building_repository)
):
    await repository.batch_create(rooms)
    return rooms


@buildings_router.post("", response_model=BuildingIDBaseSchema)
async def create_building(
    building: BuildingIDBaseSchema, repository=Depends(building_repository)
):
    await repository.create(building)
    return building


@buildings_router.get(
    "/{building_id}", response_model=BuildingIDBaseSchema | None
)
async def get_building(
    building_id: IDType, repository=Depends(building_repository)
):
    result = await repository.get_single(id=building_id)
    return result


@buildings_router.put("/{building_id}", response_model=BuildingIDBaseSchema)
async def update_building(
    building_id: IDType,
    building: BuildingIDBaseSchema,
    repository=Depends(building_repository),
): ...


@buildings_router.delete("/{building_id}", response_model=IDType)
async def delete_building(
    building_id: IDType, repository=Depends(building_repository)
):
    result = await repository.delete(id=building_id)
    return building_id


@buildings_router.patch("/{building_id}", response_model=BuildingIDBaseSchema)
async def patch_building(
    building_id: IDType,
    building: BuildingBaseSchema,
    repository=Depends(building_repository),
):
    result = await repository.update(
        building, id=building_id, exclude_unset=True
    )
    return result


@buildings_router.get("/name/{name}", response_model=list[BuildingIDBaseSchema])
async def get_buildings_by_name(
    name: str, repository=Depends(building_repository)
):
    result = await repository.get_name_filtered(name)
    return result
