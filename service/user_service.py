from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.user import SUserInDB
from core.security import verify_password, get_password_hash
from repositories.user_repository import UserRepository


async def authenticate_user(username: str, password: str, session):
    user = await UserRepository.get_user_by_username(username, session)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user