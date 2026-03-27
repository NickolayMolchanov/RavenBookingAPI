from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import engine, Model
import models
from sqlalchemy.orm import configure_mappers
configure_mappers()


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


from routes.user import user_router
from routes.hotel import hotel_router

app.include_router(user_router)
app.include_router(hotel_router)
