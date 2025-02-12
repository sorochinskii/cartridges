from db.models.base import BaseCommon
from fastapi_users.db import SQLAlchemyBaseUserTableUUID


class User(SQLAlchemyBaseUserTableUUID, BaseCommon):
    ...
