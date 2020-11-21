from typing import Optional

from pydantic import BaseModel, Field


class GroupEntity(BaseModel):
    id: int
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
    parent: Optional[str] = None
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True
