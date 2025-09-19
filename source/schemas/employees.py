from schemas.cartridges_base import CartridgeIDBaseSchema
from schemas.employees_base import EmployeeIDBaseSchema


class EmployeeSchema(EmployeeIDBaseSchema):
    cartridges: list[CartridgeIDBaseSchema]