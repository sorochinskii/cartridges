from db.models.base import Base
from pydantic import BaseModel
from repositories.repository_interface import AbstractRepository
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, Load, RelationshipProperty


class RepositorySqla(AbstractRepository):
    def __init__(self, model: Base, session: AsyncSession):
        self._session = session
        self._model = model

    def get_session(self):
        return self._session

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
            if instance:
                await session.delete(instance)
                await session.commit()
            return filters

    async def get_single(self, **filters) -> Base | None:
        stmt = select(self._model).filter_by(**filters)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_single_with_related(self, **filters) -> Base | None:
        mapper = inspect(self._model)
        load = []
        for relationship in mapper.relationships:
            if relationship.lazy == "joined":
                load.append(joinedload(getattr(self._model, relationship.key)))
        stmt = select(self._model).filter_by(**filters).options(*load)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 10) -> list[Base]:
        async with self._session as session:
            stmt = select(self._model).offset(offset).limit(limit)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_batch(self, *ids) -> list[Base]:
        async with self._session as session:
            stmt = select(self._model).where(self._model.id.in_(*ids))
            result = await session.execute(stmt)
            return result.scalars().all()

    async def batch_create(self, data: list[BaseModel]) -> None:
        async with self._session as session:
            datas = [item.model_dump() for item in data]
            new_data = [self._model(**item) for item in datas]
            session.add_all(new_data)
            await session.commit()
            [await session.refresh(data) for data in new_data]
            return new_data

    async def get_name_filtered(self, str) -> list[Base]:
        async with self._session as session:
            stmt = select(self._model).where(self._model.name.ilike(f"%{str}%"))
            result = await session.execute(stmt)
            return result.scalars().all()
