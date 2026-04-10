import asyncio
from faker import Faker
import random
from sqlalchemy.ext.asyncio import AsyncSession

from database import new_session
from models import Hotel


fake = Faker("ru_RU")

async def seed_hotels(session: AsyncSession, count: int = 123):
    hotels = []
    for _ in range(count):
        hotel = Hotel(
            name=fake.company(),
            address=fake.address(),
            country=fake.country(),
            description=fake.text(),
        )
        hotels.append(hotel)

    session.add_all(hotels)
    await session.commit()

async def main():
    async with new_session() as session:
        await seed_hotels(session)

if __name__ == "__main__":
    asyncio.run(main())