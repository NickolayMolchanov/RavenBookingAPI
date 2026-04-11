from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import TYPE_CHECKING

from database import Model


if TYPE_CHECKING:
    from models.bookings import Booking

class Hotel(Model):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    country: Mapped[str]
    city: Mapped[str]
    address: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)

    rooms: Mapped[List["Room"]] = relationship(back_populates="hotel", cascade="all, delete-orphan", init=False)

class Room(Model):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    price: Mapped[float]
    type: Mapped[str | None] = mapped_column(default=None)

    hotel: Mapped["Hotel"] = relationship(back_populates="rooms", init=False)
    bookings: Mapped[List["Booking"]] = relationship(back_populates="room", cascade="all, delete-orphan", init=False)