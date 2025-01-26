from fastapi import APIRouter, Depends
from repositories.repositories import building_repository
from schemas import buildings
from schemas.buildings_base import BuildingIDBaseSchema
from types_custom import IDType

buildings_router = APIRouter(prefix='/buildings', tags=['buildings'])


@buildings_router.get('', response_model=list[BuildingIDBaseSchema])
async def get_buildings(repository=Depends(building_repository)):
    buildings = await repository.all()
    return buildings


@buildings_router.post('/', response_model=BuildingIDBaseSchema)
async def create_building(building: BuildingIDBaseSchema,
                          repository=Depends(building_repository)):
    await repository.create(building)
    return building


@buildings_router.get('/{building_id}',
                      response_model=BuildingIDBaseSchema | None)
async def get_building(building_id: IDType,
                       repository=Depends(building_repository)):
    result = await repository.get_single(id=building_id)
    return result


@buildings_router.put('/{building_id}', response_model=BuildingIDBaseSchema)
async def update_building(building_id: IDType,
                          building: BuildingIDBaseSchema,
                          repository=Depends(building_repository)):
    ...


@buildings_router.delete('/{building_id}', response_model=IDType)
async def delete_building(building_id: IDType,
                          repository=Depends(building_repository)):
    result = await repository.delete(id=building_id)
    return building_id
