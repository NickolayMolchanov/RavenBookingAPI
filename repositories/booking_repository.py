from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models.booking import Booking
from models.room import Room
from models.user import User
from schemas.booking import SBookingCreate


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