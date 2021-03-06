from fastapi import APIRouter

from src.product.router import group_router, product_router
from src.user.router import user_router

api_router = APIRouter()
api_router.include_router(group_router, tags=["Product Groups"])
api_router.include_router(product_router, tags=["Products"])
api_router.include_router(user_router, tags=["Users"])
