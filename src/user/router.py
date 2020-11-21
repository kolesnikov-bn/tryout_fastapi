from typing import List

from fastapi import APIRouter

from src.user.repo import user_repo
from src.user.schemas import UserCreateSchema, UserSchema

user_router = APIRouter()


@user_router.get("/user", response_model=List[UserSchema])
async def get_users():
    return await user_repo.all()


@user_router.post("/user", response_model=UserSchema)
async def create_user(schema: UserCreateSchema):
    return await user_repo.create(schema)
