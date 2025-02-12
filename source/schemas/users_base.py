from typing import Generic

from fastapi_users import models
from fastapi_users.schemas import BaseUser, BaseUserUpdate
from pydantic import ConfigDict, EmailStr
from pydantic.version import VERSION as PYDANTIC_VERSION
from schemas.base import OptionalFieldsMixin
from types_custom import IDType


class UserBaseSchema(BaseUser):
    id: IDType
    is_active: bool = False


class UserUpdateBaseSchema(BaseUserUpdate):
    ...
