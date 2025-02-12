from pydantic import BaseModel
from schemas.mixins import OptionalFieldsMixin


class BaseSchema(BaseModel, OptionalFieldsMixin):
    ...
