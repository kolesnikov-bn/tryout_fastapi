from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError

from src.constants import GroupId, ProductId
from src.product.models import GroupPDModel, ProductPDModel
from src.product.repo import group_repo, product_repo
from src.product.schemas import (
    GroupSchema,
    GroupUpdateSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductListSchema,
)

product_group_router = APIRouter()
product_router = APIRouter()


class Status(BaseModel):
    message: str


# <editor-fold desc="Groups">
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
    return Status(message=f"Group has been deleted: {group_id}")


# </editor-fold>


# <editor-fold desc="Products">
@product_router.get("/product", response_model=List[ProductPDModel])
async def get_products():
    return await product_repo.all()


@product_router.post("/product", response_model=ProductPDModel)
async def create_product(schema: ProductCreateSchema):
    return await product_repo.create(schema)


@product_router.put(
    "/product/{product_id}",
    response_model=ProductPDModel,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_product(product_id: ProductId, schema: ProductUpdateSchema):
    return await product_repo.update(schema, id=product_id)


@product_router.delete(
    "/product/{product_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_product(product_id: ProductId):
    await product_repo.delete(id=product_id)
    return Status(message=f"Product has been deleted: {product_id}")


@product_router.get("/product/{group_id}", response_model=List[ProductListSchema])
async def get_product(group_id: GroupId):
    return await product_repo.get_nested_products(group_id)


# </editor-fold>
