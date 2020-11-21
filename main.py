import uvicorn
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

import settings
from src import routers

app = FastAPI(title="FastAPI example")

app.include_router(routers.api_router, prefix=settings.API)

register_tortoise(
    app,
    db_url=settings.DATABASE_URI,
    modules={"models": settings.APPS_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.on_event("startup")
async def startup_event():
    Tortoise.init_models(settings.APPS_MODELS, "models")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=settings.DEBUG)
