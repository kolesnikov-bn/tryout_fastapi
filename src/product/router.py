from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError

from constants import GroupId
from product.models import GroupPDModel
from src.product.repo import group_repo
from src.product.schemas import GroupSchema, GroupUpdateSchema

product_group_router = APIRouter()


class Status(BaseModel):
    message: str


@product_group_router.get("/group", response_model=List[GroupPDModel])
async def get_groups():
    return await group_repo.all()


@product_group_router.post(
    "/group",
    response_model=GroupPDModel,
    responses={404: {"model": HTTPNotFoundError}},
)
async def create_group(schema: GroupSchema):
    return await group_repo.create_node(schema)


@product_group_router.get(
    "/group/{group_id}",
    response_model=GroupPDModel,
    responses={404: {"model": HTTPNotFoundError}},
)
async def get_group(group_id: GroupId):
    return await group_repo.get(id=group_id)


@product_group_router.put(
    "/group/{group_id}",
    response_model=GroupPDModel,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_group(group_id: GroupId, schema: GroupUpdateSchema):
    return await group_repo.update_node(group_id, schema)


@product_group_router.delete(
    "/group/{group_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
)
async def delete_group(group_id: GroupId):
    await group_repo.delete_node(group_id)
    return Status(message=f"Deleted group: {group_id}")
