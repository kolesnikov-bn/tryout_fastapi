from abc import ABC, abstractmethod
from typing import TypeVar, Optional

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
    async def all(self):
        raise NotImplementedError

    @abstractmethod
    async def get(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_obj(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError


class FakeRepo(BaseRepository):
    async def create(self, schema, **kwargs) -> Optional[CreateSchemaT]:
        pass

    async def update(self, schema, **kwargs) -> Optional[UpdateSchemaT]:
        pass

    async def all(self):
        pass

    async def get(self, **kwargs):
        pass

    async def get_obj(self, **kwargs):
        pass

    async def delete(self, **kwargs):
        pass
