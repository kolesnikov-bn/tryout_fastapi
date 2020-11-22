from typing import Optional, Any

from pydantic import BaseModel


class UserEntity(BaseModel):
    username: str
    first_name: str
    last_name: str
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True


class UserSchema(UserEntity):
    full_name: str

    class Config:
        orm_mode = True


class UserCreateSchema(UserEntity):
    password: str

    class Config:
        orm_mode = True
