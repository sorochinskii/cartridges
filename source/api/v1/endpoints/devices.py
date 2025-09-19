from apps.user_manager import fastapi_users
from fastapi import APIRouter, Depends
from repositories.repositories import device_repository
from schemas.devices_base import DeviceIDBaseSchema, DeviceUpdateBaseSchema
from types_custom import IDType

devices_router = APIRouter(
    prefix="/devices",
    tags=["devices"],
    dependencies=[
        Depends(
            fastapi_users.authenticator.current_user(active=True, verified=True)
        )
    ],
)


@devices_router.get("", response_model=list[DeviceIDBaseSchema])
async def get_devices(repository=Depends(device_repository)):
    devices = await repository.get_all()
    return devices


@devices_router.post("", response_model=DeviceIDBaseSchema)
async def create_device(
    device: DeviceIDBaseSchema, repository=Depends(device_repository)
):
    await repository.create(device)
    return device


@devices_router.get("/{device_id}", response_model=DeviceIDBaseSchema | None)
async def get_device(device_id: IDType, repository=Depends(device_repository)):
    result = await repository.get_single(id=device_id)
    return result


@devices_router.put("/{device_id}", response_model=DeviceIDBaseSchema)
async def update_device(
    device_id: IDType,
    device: DeviceUpdateBaseSchema,
    repository=Depends(device_repository),
):
    result = await repository.update(device, id=device_id, exclude_unset=False)
    return result


@devices_router.patch("/{device_id}", response_model=DeviceIDBaseSchema)
async def patch_device(
    device_id: IDType,
    device: DeviceUpdateBaseSchema,
    repository=Depends(device_repository),
):
    result = await repository.update(device, id=device_id, exclude_unset=True)
    return result


@devices_router.delete("/{device_id}", response_model=IDType)
async def delete_device(
    device_id: IDType, repository=Depends(device_repository)
):
    result = await repository.delete(id=device_id)
    return device_id
