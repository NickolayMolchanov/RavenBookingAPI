from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Model
from models.hotels import hotel_owners


if TYPE_CHECKING:
    from models.bookings import Booking

class User(Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    role: Mapped[str] = mapped_column(default="user")

    bookings: Mapped[list["Booking"]] = relationship(
        "Booking",
        back_populates="user",
        cascade="all, delete-orphan",
        init=False,
        lazy="selectin"
    )
    hotels: Mapped[list["Hotel"]] = relationship(
        "Hotel",
        secondary=hotel_owners,
        back_populates="owners",
        init=False,
        lazy="selectin"
    )