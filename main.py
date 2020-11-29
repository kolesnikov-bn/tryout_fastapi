import uvicorn
from fastapi import FastAPI, Depends
from starlette.requests import Request
from tortoise.contrib.fastapi import register_tortoise

import settings
from src import routers, is_group_allowed
from src.auth.jwt import get_current_user
from src.auth.router import auth_router
from src.user.schemas import UserSchema

app = FastAPI(title="FastAPI example")


async def check_permissions(
    request: Request,
    user: UserSchema = Depends(get_current_user),
):
    # TODO: Изменить проверку прав доступа к группе. Сейчас это костыль чтобы получить требуемое поведение.
    group_id = request.path_params.get("group_id")

    if group_id:
        await is_group_allowed(int(group_id), user)

    return True


app.include_router(
    routers.api_router,
    prefix=settings.API,
    dependencies=[Depends(check_permissions)],
)
app.include_router(auth_router, tags=["Auth"])

register_tortoise(
    app,
    db_url=settings.DATABASE_URI,
    modules={"models": settings.APPS_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=settings.DEBUG)
