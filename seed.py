import asyncio
from faker import Faker
import random
from sqlalchemy.ext.asyncio import AsyncSession

from database import new_session
from models import Hotel, Room

fake = Faker("ru_RU")

async def seed_hotels(session: AsyncSession, count: int = 123):
    hotels = []
    for _ in range(count):
        hotel = Hotel(
            name=fake.company(),
            address=fake.address(),
            country=fake.country(),
            city=fake.city(),
            description=fake.text(),
        )
        hotels.append(hotel)

    session.add_all(hotels)
    await session.commit()

async def seed_rooms(session: AsyncSession, count: int = 456):
    rooms = []
    for _ in range(count):
        room = Room(
            hotel_id=fake.random_int(min=1, max=123),
            price=fake.random_int(min=3000, max=130000),
            type=fake.random_element(elements=("Эконом", "Стандарт", "Люкс")),
        )
        rooms.append(room)

    session.add_all(rooms)
    await session.commit()

async def main():
    async with new_session() as session:
        await seed_hotels(session)

if __name__ == "__main__":
    asyncio.run(main())