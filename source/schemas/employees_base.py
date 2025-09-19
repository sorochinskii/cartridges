from schemas.base import BaseSchema
from types_custom import IDType


class EmployeeBaseSchema(BaseSchema):
    name: str
    personnel_number: str


class EmployeeIDBaseSchema(EmployeeBaseSchema):
    id: IDType


class EmployeeUpdateBaseSchema(EmployeeBaseSchema):
    ...
