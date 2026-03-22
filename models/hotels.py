from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Model


class Hotel(Model):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    address: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)

    rooms: Mapped[List["Room"]] = relationship(back_populates="hotel", cascade="all, delete-orphan")

class Room(Model):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    type: Mapped[str | None] = mapped_column(default=None)
    price: Mapped[float]

    hotel: Mapped["Hotel"] = relationship(back_populates="rooms")
    bookings: Mapped[List["Booking"]] = relationship(back_populates="room", cascade="all, delete-orphan")