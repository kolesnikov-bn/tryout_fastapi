from typing import Optional

from src.auth.security import get_password_hash, verify_password
from src.repositories import DBRepo
from src.user.models import User, UserPDModel
from src.user.schemas import UserCreateSchema, UserEntity


class UserRepo(DBRepo):
    model = User
    get_schema = UserPDModel

    async def create_user(self, schema: UserCreateSchema, **kwargs):
        hash_password = get_password_hash(schema.dict().pop("password"))
        return await self.create(
            UserCreateSchema(
                **schema.dict(exclude={"password"}), password=hash_password, **kwargs
            )
        )

    async def authenticate(self, username: str, password: str) -> Optional[UserEntity]:
        user = await self.get_schema.from_queryset_single(
            self.model.get(username=username)
        )
        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user


user_repo = UserRepo()
