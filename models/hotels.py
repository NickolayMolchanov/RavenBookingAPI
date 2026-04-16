from typing import List
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import TYPE_CHECKING

from database import Model


if TYPE_CHECKING:
    from models.bookings import Booking

hotel_owners = Table(
    "hotel_owners",
    Model.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("hotel_id", ForeignKey("hotels.id"), primary_key=True),
)

class Hotel(Model):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    country: Mapped[str]
    city: Mapped[str]
    address: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)


    rooms: Mapped[List["Room"]] = relationship(back_populates="hotel", cascade="all, delete-orphan", init=False)
    owners: Mapped[List["User"]] = relationship(
        "User",
        secondary=hotel_owners,
        back_populates="hotels",
        init=False
    )

class Room(Model):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    price: Mapped[float]
    type: Mapped[str | None] = mapped_column(default=None)

    hotel: Mapped["Hotel"] = relationship(back_populates="rooms", init=False)
    bookings: Mapped[List["Booking"]] = relationship(back_populates="room", cascade="all, delete-orphan", init=False)

