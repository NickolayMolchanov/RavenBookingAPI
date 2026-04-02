from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.security import get_password_hash
from models import Hotel, Room, Booking
from models.users import User
from schemas.bookings import SBookingCreate
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
            hashed_password = get_password_hash(data.password),
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

    @classmethod
    async def update_hotel(cls, hotel_id: int, data: SHotelCreate, session: AsyncSession):
        hotel = await session.get(Hotel, hotel_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(hotel, key, value)
        await session.commit()
        await session.refresh(hotel)
        return hotel

    @classmethod
    async def remove_hotel(cls, hotel_id, session: AsyncSession):
        hotel = await session.get(Hotel, hotel_id)
        await session.delete(hotel)
        await session.commit()
        return True



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

    @classmethod
    async def remove_room(cls, room_id, session: AsyncSession):
        room = await session.get(Room, room_id)
        await session.delete(room)
        await session.commit()
        return True


class BookingRepository:
    @classmethod
    async def create_booking(cls, data:SBookingCreate, session: AsyncSession):
        booking = Booking(**data.model_dump())
        session.add(booking)
        try:
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        await session.refresh(booking)
        return booking

    @classmethod
    async def is_room_busy(cls,room_id, date_from, date_to, session: AsyncSession):
        query = select(Booking).where(
            and_(
                Booking.room_id == room_id,
                Booking.date_from < date_to,
                Booking.date_to > date_from,
                Booking.status == 'active',
            )
        )
        result = await session.execute(query)
        booking = result.scalars().first()
        return booking is not None

    @classmethod
    async def get_bookings_by_user(cls, user_id: int, session: AsyncSession):
        query = select(Booking).where(User.id == user_id)
        result = await session.execute(query)
        user_bookings = result.scalars().all()
        return user_bookings

    @classmethod
    async def get_bookings_by_room(cls, room_id: int, session: AsyncSession):
        query = select(Booking).where(Room.id == room_id)
        result = await session.execute(query)
        room_bookings = result.scalars().all()
        return room_bookings

    @classmethod
    async def remove_booking(cls, booking_id: int, session: AsyncSession):
        booking = await session.get(Booking, booking_id)
        await session.delete(booking)
        await session.commit()
        return True