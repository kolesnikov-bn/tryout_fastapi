from pydantic import BaseModel, Extra


class UserEntity(BaseModel):
    username: str
    first_name: str
    last_name: str

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
