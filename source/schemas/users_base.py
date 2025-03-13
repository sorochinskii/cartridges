from fastapi_users.schemas import BaseUser, BaseUserUpdate, CreateUpdateDictModel
from pydantic import EmailStr
from types_custom import IDType


class UserBaseSchema(BaseUser):
    id: IDType
    is_active: bool = False


class UserUpdateBaseSchema(BaseUserUpdate):
    ...


class UserBaseCreate(CreateUpdateDictModel):
    email: EmailStr
    password: str
