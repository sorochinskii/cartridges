from schemas.base import BaseSchema
from types_custom import IDType


class EmployeeBaseSchema(BaseSchema):
    name: str


class EmployeeIDBaseSchema(EmployeeBaseSchema):
    id: IDType

class EmployeeCreateBaseSchema(EmployeeIDBaseSchema):
    ...

class EmployeeUpdateBaseSchema(EmployeeBaseSchema):
    ...
