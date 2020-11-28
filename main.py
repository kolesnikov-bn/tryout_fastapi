import sys

import uvicorn
from fastapi import FastAPI
from loguru import logger
from tortoise.contrib.fastapi import register_tortoise

import settings
from src import routers
from src.auth.router import auth_router

logger.add(
    sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>"
)
app = FastAPI(title="FastAPI example")

app.include_router(routers.api_router, prefix=settings.API)
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
