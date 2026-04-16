from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from faker import Faker

from database import engine, Model
import models
from core.middleware import AuthMiddleware
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

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)

from routes.user import user_router
from routes.hotel import hotel_router
from routes.booking import booking_router
from routes.auth import auth_router
from routes.templates import templates_router
app.include_router(user_router)
app.include_router(hotel_router)
app.include_router(booking_router)
app.include_router(auth_router)
app.include_router(templates_router)

