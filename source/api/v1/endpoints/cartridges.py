from apps.user_manager import fastapi_users
from fastapi import APIRouter, Depends
from repositories.repositories import cartridge_repository
from schemas.cartridges_base import (
    CartridgeIDBaseSchema,
    CartridgeUpdateBaseSchema,
)
from types_custom import IDType

cartridges_router = APIRouter(
    prefix="/cartridges",
    tags=["cartridges"],
    dependencies=[
        Depends(
            fastapi_users.authenticator.current_user(active=True, verified=True)
        )
    ],
)


@cartridges_router.get("", response_model=list[CartridgeIDBaseSchema])
async def get_cartridge(repository=Depends(cartridge_repository)):
    cartridges = await repository.get_all()
    return cartridges


@cartridges_router.post("", response_model=CartridgeIDBaseSchema)
async def create_cartridge(
    cartridge: CartridgeIDBaseSchema, repository=Depends(cartridge_repository)
):
    await repository.create(cartridge)
    return cartridge


@cartridges_router.get(
    "/{cartridge_id}", response_model=CartridgeIDBaseSchema | None
)
async def get_cartridge_by_id(
    cartridge_id: IDType, repository=Depends(cartridge_repository)
):
    result = await repository.get_single(id=cartridge_id)
    return result


@cartridges_router.put("/{cartridge_id}", response_model=CartridgeIDBaseSchema)
async def update_cartridge(
    cartridge_id: IDType,
    cartridge: CartridgeUpdateBaseSchema,
    repository=Depends(cartridge_repository),
):
    result = await repository.update(
        cartridge, id=cartridge_id, exclude_unset=False
    )
    return result


@cartridges_router.patch(
    "/{cartridge_id}", response_model=CartridgeIDBaseSchema
)
async def patch_cartridge(
    cartridge_id: IDType,
    cartridge: CartridgeUpdateBaseSchema,
    repository=Depends(cartridge_repository),
):
    result = await repository.update(
        cartridge, id=cartridge_id, exclude_unset=True
    )
    return result


@cartridges_router.delete("/{cartridge_id}", response_model=IDType)
async def delete_cartridge(
    cartridge_id: IDType, repository=Depends(cartridge_repository)
):
    result = await repository.delete(id=cartridge_id)
    return cartridge_id
