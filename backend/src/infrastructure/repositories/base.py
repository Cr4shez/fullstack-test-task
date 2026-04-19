from typing import Generic, TypeVar, Type, Optional, List, Union, Tuple

from pydantic import BaseModel
from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.models import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: Type[ModelType],
        schema: Type[SchemaType],
        session: AsyncSession
    ):
        self._model = model
        self._session = session
        self._schema = schema

    async def find_by_id(self, id: str) -> Optional[SchemaType]:
        query = select(self._model).where(self._model.id == id)
        result = await self._session.execute(query)
        db_obj = result.scalar_one_or_none()
        return self._schema.model_validate(db_obj) if db_obj else None

    async def find_all(
        self,
        limit: int = 10,
        offset: int = 0,
        **filters: list[SchemaType]
    ) -> List[SchemaType]:
        query = select(self._model).limit(limit).offset(offset)
        if filters:
            query = query.filter_by(**filters)
        result = await self._session.execute(query)
        db_objs = result.scalars().all()
        return [self._schema.model_validate(obj) for obj in db_objs]

    async def count(self, **filters: dict[str, Union[str, int]]) -> int:
        query = select(func.count()).select_from(self._model)
        if filters:
            query = query.filter_by(**filters)
        result = await self._session.execute(query)
        count = result.scalar()
        return count

    async def create(self, schema: CreateSchemaType) -> SchemaType:
        obj = self._model(**schema.model_dump())
        self._session.add(obj)
        await self._session.flush()
        await self._session.refresh(obj)
        return self._schema.model_validate(obj)

    async def update(self, id: str, schema: UpdateSchemaType) -> Optional[SchemaType]:
        query = select(self._model).where(self._model.id == id)
        result = await self._session.execute(query)
        db_obj = result.scalar_one_or_none()

        if not db_obj:
            return None

        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        await self._session.flush()
        await self._session.refresh(db_obj)
        return self._schema.model_validate(db_obj)

    async def delete(self, id: str) -> bool:
        query = delete(self._model).where(self._model.id == id)
        result = await self._session.execute(query)
        await self._session.flush()
        return result.rowcount > 0
