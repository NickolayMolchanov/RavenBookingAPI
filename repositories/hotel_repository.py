from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.hotel import Hotel
from schemas.hotel import SHotelCreate


class HotelRepository:
    @classmethod
    async def add_hotel(cls,data: SHotelCreate, session: AsyncSession):
        existing_name = await session.execute(select(Hotel).where(Hotel.name == data.name))
        if existing_name.scalars().first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This name is already exists')
        hotel = Hotel(
            name=data.name,
            country=data.country,
            city=data.city,
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