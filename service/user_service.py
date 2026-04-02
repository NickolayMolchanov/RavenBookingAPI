from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas.users import SUserInDB
from core.security import verify_password,get_password_hash


async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    user = result.scalars().first()
    return user

async def authenticate_user(username: str, password: str, session: AsyncSession) -> User | None:
    user = await get_user_by_username(username, session)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user