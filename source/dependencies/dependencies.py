from collections.abc import Callable

from db.db import get_async_session
from db.models.base import Base
from fastapi import Depends
from repositories.repository_interface import AbstractRepository
from sqlalchemy.ext.asyncio import AsyncSession


def get_db_repository(
        model: type[Base],
        repository: type[AbstractRepository]):
    # ) -> Callable[[AsyncSession], AbstractRepository]:
    def func(session: AsyncSession = Depends(get_async_session)):
        return repository(model, session)
    return func
