from fastapi import APIRouter

from src.product.router import product_group_router

api_router = APIRouter()
api_router.include_router(product_group_router, tags=["Product Groups"])
