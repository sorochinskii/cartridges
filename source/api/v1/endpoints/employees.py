from apps.user_manager import fastapi_users
from fastapi import APIRouter, Depends
from repositories.repositories import employee_repository
from schemas.base import ItemIds
from schemas.employees import EmployeeSchema
from schemas.employees_base import EmployeeCreateBaseSchema, EmployeeIDBaseSchema, EmployeeUpdateBaseSchema
from types_custom import IDType

employees_router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    dependencies=[
        Depends(
            fastapi_users.authenticator.current_user(
                active=True, verified=True
            )
        )
    ],
)

@employees_router.get("", response_model=list[EmployeeIDBaseSchema])
async def get_employees(
    limit: int = 10, offset: int = 0, repository=Depends(employee_repository)
):
    employees = await repository.get_all(offset=offset, limit=limit)
    return employees

@employees_router.post("", response_model=EmployeeIDBaseSchema)
async def create_employee(
    employee: EmployeeCreateBaseSchema, repository=Depends(employee_repository)
):
    employee = await repository.create(employee)
    return employee

@employees_router.get("/{employee_id}", response_model=EmployeeSchema)
async def get_employee(
    employee_id: IDType, repository=Depends(employee_repository)
):
    employee = await repository.get_by_id(employee_id)
    return employee
