from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database import Model


class User(Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column()

    bookings: Mapped[list["Booking"]] = relationship(
        'Booking',
        back_populates='user',
        init=False
    )

    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str] = mapped_column(default="user")