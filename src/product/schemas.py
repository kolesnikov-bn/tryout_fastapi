from typing import Optional

from pydantic import BaseModel, Field

from src.constants import GroupId, ProductId


class GroupEntity(BaseModel):
    id: GroupId
    name: str
    parent: Optional[str]

    class Config:
        orm_mode = True


class GroupSchema(BaseModel):
    name: str = Field(..., description="Leaf node name")
    parent: Optional[str] = Field(None, description="Parent node name")

    class Config:
        orm_mode = True


class GroupUpdateSchema(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[GroupId] = None

    class Config:
        orm_mode = True


class ProductEntity(BaseModel):
    id: ProductId
    name: str
    group_id: GroupId

    class Config:
        orm_mode = True


class ProductInDBSchema(BaseModel):
    name: str
    group_id: GroupId

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "string",
                "group_id": 1,
            }
        }


class ProductGroupSchema(BaseModel):
    id: GroupId
    name: str

    class Config:
        orm_mode = True


class ProductListSchema(BaseModel):
    name: Optional[str]
    group: ProductGroupSchema

    class Config:
        orm_mode = True
