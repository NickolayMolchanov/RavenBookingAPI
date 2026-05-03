from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter

from database import engine, Model


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    print("База данных готова к работе")
    yield

app = FastAPI(
    title="API for hotel booking",
    version="1.0.0",
    lifespan=lifespan,
)

from routes.user import router as user_router

app.include_router(user_router)