from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models import Hotel, Room
from models.users import User
from schemas.hotels import SHotelCreate, SRoomCreate
from schemas.users import SUserCreate


class UserRepository:
    @classmethod
    async def add_user(cls,data:SUserCreate, session: AsyncSession):
        existing_email = await session.execute(select(User).where(User.email == data.email))
        if existing_email.scalars().first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
        existing_username = await session.execute(select(User).where(User.username == data.username))
        if existing_username.scalars().first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username already taken')

        user = User(
            username = data.username,
            email = data.email,
            password = data.password,
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
    async def get_user(cls, user_id:int, session: AsyncSession):
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        return user


class HotelRepository:
    @classmethod
    async def add_hotel(cls,data: SHotelCreate, session: AsyncSession):
        existing_name = await session.execute(select(Hotel).where(Hotel.name == data.name))
        if existing_name.scalars().first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This name is already exists')
        hotel = Hotel(
            name=data.name,
            address=data.address,
            description=data.description,
        )
        session.add(hotel)
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        await session.refresh(hotel)
        return hotel

    @classmethod
    async def get_hotel(cls, hotel_id:int, session: AsyncSession):
        query = select(Hotel).where(Hotel.id == hotel_id)
        result = await session.execute(query)
        hotel = result.scalars().first()
        return hotel

    @classmethod
    async def get_hotels(cls, session: AsyncSession):
        query = select(Hotel)
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


class RoomsRepository:
    @classmethod
    async def add_room(cls,data: SRoomCreate, session: AsyncSession):
        room = Room(**data.model_dump())
        session.add(room)
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        await session.refresh(room)
        return room

    @classmethod
    async def get_room(cls, room_id: int, session: AsyncSession):
        query = select(Room).where(Room.id == room_id)
        result = await session.execute(query)
        room = result.scalars().first()
        return room

    @classmethod
    async def get_rooms(cls, session: AsyncSession):
        query = select(Room)
        result = await session.execute(query)
        rooms = result.scalars().all()
        return rooms