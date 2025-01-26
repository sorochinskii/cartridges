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
            new_data = self._model(**data.model_dump())
            session.add(new_data)
            await session.commit()
            await session.refresh(new_data)
            return new_data

    async def update(
            self, data: BaseModel, exclude_unset=False, **filters
    ) -> Base | None:
        async with self._session as session:
            instance = await self.get_single(**filters)
            for k, v in data.model_dump(exclude_unset=exclude_unset).items():
                setattr(instance, k, v)
            session.add(instance)
            await session.commit()
            return instance

    async def delete(self, **filters) -> dict:
        async with self._session as session:
            instance = await self.get_single(**filters)
            await session.delete(instance)
            await session.commit()
            return filters

    async def get_single(self, **filters) -> Base | None:
        async with self._session as session:
            stmt = select(self._model).filter_by(**filters)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_all(self) -> list[Base]:
        async with self._session as session:
            stmt = select(self._model)
            result = await session.execute(stmt)
            return result.scalars().all()
