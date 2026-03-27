from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from database import Model

if TYPE_CHECKING:
    from models.users import User
    from models.hotels import Room

class Booking(Model):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'), nullable=False)
    date_from: Mapped[datetime] = mapped_column()
    date_to: Mapped[datetime] = mapped_column()
    status: Mapped[str] = mapped_column(default="active")

    room: Mapped["Room"] = relationship("Room", back_populates="bookings", init=False)
    user: Mapped["User"] = relationship("User", back_populates="bookings", init=False)