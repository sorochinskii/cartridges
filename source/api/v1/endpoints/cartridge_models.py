from apps.user_manager import fastapi_users
from fastapi import APIRouter, Depends
from repositories.repositories import cartridge_model_repository
from schemas.cartridge_models import (
    CartridgeModelSchema,
    CartridgeModelSchemaCreate,
)
from schemas.cartridge_models_base import CartridgeModelIDBaseSchema
from types_custom import IDType

cartridge_models_router = APIRouter(
    prefix="/cartridge_models",
    tags=["cartridge_models"],
    dependencies=[
        Depends(
            fastapi_users.authenticator.current_user(
                active=True, verified=True, superuser=False
            )
        )
    ],
)


@cartridge_models_router.get(
    "", response_model=list[CartridgeModelIDBaseSchema]
)
async def get_cartridge_models(
    limit: int = 10,
    offset: int = 0,
    repository=Depends(cartridge_model_repository),
):
    result = await repository.get_all(offset, limit)
    return result


@cartridge_models_router.post("", response_model=CartridgeModelSchema)
async def create_cartridge_model(
    model: CartridgeModelSchemaCreate,
    repository=Depends(cartridge_model_repository),
):
    await repository.create(model)
    return model


@cartridge_models_router.get(
    "/{item_id}", response_model=CartridgeModelSchema | None
)
async def get_cartridge_model(
    item_id: IDType, repository=Depends(cartridge_model_repository)
):
    result = await repository.get_single_with_related(id=item_id)
    return result
