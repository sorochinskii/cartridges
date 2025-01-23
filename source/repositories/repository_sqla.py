from typing import TypeVar

from db.models.base import Base
from pydantic import BaseModel
from repositories.repository_interface import AbstractRepository
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from types_custom import CreateSchemaType, UpdateSchemaType


class RepositorySqla(AbstractRepository):

    def __init__(self, model: Base, session: AsyncSession):
        self._session = session
        self._model = model

    async def create(self, data: BaseModel) -> Base:
        async with self._session as session:
            instance = self._model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def update(self, data: BaseModel, **filters) -> Base:
        async with self._session as session:
            stmt = update(self._model
                          ).values(**data
                                   ).filter_by(**filters
                                               ).returning(self._model)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()

    async def delete(self, **filters) -> dict:
        async with self._session as session:
            await session.execute(delete(self._model).filter_by(**filters))
            await session.commit()
            return filters

    async def get_single(self, **filters) -> Base | None:
        async with self._session as session:
            row = await session.execute(select(self._model).filter_by(**filters))
            return row.scalar_one_or_none()

    async def all(
            self,
    ) -> list[Base]:
        async with self._session as session:
            stmt = select(self._model)
            row = await session.execute(stmt)
            return row.scalars().all()
