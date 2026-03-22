from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Model


class User(Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column()

    bookings: Mapped[list["Booking"]] = relationship(back_populates="user", cascade="all, delete-orphan")