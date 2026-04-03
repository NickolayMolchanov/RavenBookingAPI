from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db
from dependencies import get_current_user
from models import User
from schemas.users import SUserCreate, SUserRead
from service.user_service import AuthService

auth_router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@auth_router.post("/register", response_model=SUserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user: SUserCreate, session: AsyncSession = Depends(get_db)):
    return await AuthService.register_user(user, session)

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_db)
):
    print(form_data.username, form_data.password)
    token = await AuthService.login_user(form_data.username, form_data.password, session)
    return {
        "access_token": token,
        "token_type": "bearer",
    }

@auth_router.get("/me", response_model=SUserRead)
async def me(user: User = Depends(get_current_user)):
    return user