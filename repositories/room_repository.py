from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.room import Room
from schemas.room import SRoomCreate


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
        return rooms\

    @classmethod
    async def update_room(cls, room_id: int, data: SRoomCreate, session: AsyncSession):
        room = await session.get(Room, room_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(room, key, value)
        await session.commit()
        await session.refresh(room)
        return room

    @classmethod
    async def remove_room(cls, room_id, session: AsyncSession):
        room = await session.get(Room, room_id)
        await session.delete(room)
        await session.commit()
        return True