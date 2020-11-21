from abc import ABC, abstractmethod
from typing import TypeVar, Optional, Type

from fastapi import HTTPException
from pydantic import BaseModel
from tortoise import Model

ModelT = TypeVar("ModelT", bound=Model)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)
GetSchemaT = TypeVar("GetSchemaT", bound=BaseModel)


class BaseRepository(ABC):
    @abstractmethod
    async def create(self, schema, **kwargs) -> Optional[CreateSchemaT]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, schema, **kwargs) -> Optional[UpdateSchemaT]:
        raise NotImplementedError

    @abstractmethod
    async def all(self) -> GetSchemaT:
        raise NotImplementedError

    @abstractmethod
    async def get(self, **kwargs) -> GetSchemaT:
        raise NotImplementedError

    @abstractmethod
    async def get_obj(self, **kwargs) -> ModelT:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs) -> None:
        raise NotImplementedError


class FakeRepo(BaseRepository):
    async def create(self, schema, **kwargs) -> Optional[CreateSchemaT]:
        pass

    async def update(self, schema, **kwargs) -> Optional[UpdateSchemaT]:
        pass

    async def all(self) -> GetSchemaT:
        pass

    async def get(self, **kwargs) -> GetSchemaT:
        pass

    async def get_obj(self, **kwargs) -> ModelT:
        pass

    async def delete(self, **kwargs) -> None:
        pass


class DBRepo(BaseRepository):
    model: Type[ModelT]
    get_schema: GetSchemaT

    async def create(self, schema, **kwargs) -> Optional[CreateSchemaT]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        return await self.get_schema.from_tortoise_orm(obj)

    async def update(self, schema, **kwargs) -> Optional[UpdateSchemaT]:
        await self.model.filter(**kwargs).update(**schema.dict(exclude_unset=True))
        return await self.get_schema.from_queryset_single(self.model.get(**kwargs))

    async def all(self) -> GetSchemaT:
        return await self.get_schema.from_queryset(self.model.all())

    async def get(self, **kwargs) -> GetSchemaT:
        return await self.get_schema.from_queryset_single(self.model.get(**kwargs))

    async def get_obj(self, **kwargs) -> ModelT:
        return await self.model.get_or_none(**kwargs)

    async def delete(self, **kwargs) -> None:
        obj = await self.model.filter(**kwargs).delete()
        if not obj:
            raise HTTPException(status_code=404, detail="Object does not exist")
