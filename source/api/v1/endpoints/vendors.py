from fastapi import APIRouter, Depends
from repositories.repositories import vendor_repository
from schemas.vendors_base import VendorIDBaseSchema, VendorUpdateBaseSchema
from types_custom import IDType

vendors_router = APIRouter(prefix='/vendors', tags=['vendors'])


@vendors_router.get('', response_model=list[VendorIDBaseSchema])
async def get_Vendors(repository=Depends(vendor_repository)):
    vendors = await repository.get_all()
    return vendors


@vendors_router.post('/', response_model=VendorIDBaseSchema)
async def create_vendor(vendor: VendorIDBaseSchema,
                        repository=Depends(vendor_repository)):
    await repository.create(vendor)
    return vendor


@vendors_router.get('/{vendor_id}', response_model=VendorIDBaseSchema | None)
async def get_vendor(vendor_id: IDType,
                     repository=Depends(vendor_repository)):
    result = await repository.get_single(id=vendor_id)
    return result


@vendors_router.put('/{vendor_id}', response_model=VendorIDBaseSchema)
async def update_vendor(vendor_id: IDType,
                        vendor: VendorUpdateBaseSchema,
                        repository=Depends(vendor_repository)):
    result = await repository.update(vendor, id=vendor_id, exclude_unset=False)
    return result


@vendors_router.patch('/{vendor_id}', response_model=VendorIDBaseSchema)
async def patch_vendor(vendor_id: IDType,
                       vendor: VendorUpdateBaseSchema,
                       repository=Depends(vendor_repository),
                       ):
    result = await repository.update(vendor, id=vendor_id, exclude_unset=True)
    return result


@vendors_router.delete('/{vendor_id}', response_model=IDType)
async def delete_vendor(vendor_id: IDType,
                        repository=Depends(vendor_repository)):
    result = await repository.delete(id=vendor_id)
    return vendor_id
