from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repository import UserRepository
from schemas.users import SUserInDB, SUserCreate
from core.security import verify_password, get_password_hash, create_access_token


class AuthService:
    @classmethod
    async def register_user(cls, data: SUserCreate, session: AsyncSession):
        existing_user = await UserRepository.get_user_by_email(data.email, session)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='email already exists')
        user = await UserRepository.add_user(data, session)
        return user

    @classmethod
    async def login_user(cls, email: str, password: str, session: AsyncSession):
        user = await UserRepository.get_user_by_email(email, session)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        token = create_access_token(
            {
                "sub": str(user.id),
            }
        )
        return token