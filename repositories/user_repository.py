from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_password_hash
from models.user import User
from schemas.user import SUserCreate


class UserRepository:
    @classmethod
    async def add_user(cls, data:SUserCreate, session: AsyncSession):
        existing_email = await session.execute(select(User).where(User.email == data.email))
        if existing_email.scalars().first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
        existing_username = await session.execute(select(User).where(User.username == data.username))
        if existing_username.scalars().first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already taken')

        result = await session.execute(
            select(User).where(User.role.in_(["admin", "moderator"]))
        )
        existing_admin = result.scalars().first()

        role = "user"
        if not existing_admin:
            role = "admin"

        user = User(
            username = data.username,
            email = data.email,
            hashed_password = get_password_hash(data.password),
            created_at = datetime.now(),
            role = role
        )
        session.add(user)
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        await session.refresh(user)
        return user


    @classmethod
    async def get_user_by_id(cls, user_id:int, session: AsyncSession):
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        return user

    @classmethod
    async def get_user_by_email(cls, user_email: str, session: AsyncSession):
        query = select(User).where(User.email == user_email)
        result = await session.execute(query)
        user = result.scalars().first()
        return user

    @classmethod
    async def get_user_by_username(cls, user_username: str, session: AsyncSession):
        query = select(User).where(User.username == user_username)
        result = await session.execute(query)
        user = result.scalars().first()
        return user

    @classmethod
    async def update_user(cls, user_id:int, data:SUserCreate, session: AsyncSession):
        user = await session.get(User, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        await session.commit()
        await session.refresh(user)
        return user

    @classmethod
    async def remove_user(cls, user_id, session: AsyncSession):
        user = await session.get(User, user_id)
        await session.delete(user)
        await session.commit()
        return True