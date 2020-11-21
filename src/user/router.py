from typing import List

from fastapi import APIRouter, Depends

from src.auth.jwt import get_current_active_user
from src.user.repo import user_repo
from src.user.schemas import UserCreateSchema, UserSchema, UserEntity

user_router = APIRouter()


@user_router.get("/user", response_model=List[UserSchema])
async def get_users():
    return await user_repo.all()


@user_router.post("/user", response_model=UserSchema)
async def create_user(schema: UserCreateSchema):
    return await user_repo.create_user(schema)


@user_router.get("/user/self/", response_model=UserEntity)
async def try_yourself(current_user: UserEntity = Depends(get_current_active_user)):
    return current_user
