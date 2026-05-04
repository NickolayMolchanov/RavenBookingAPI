from typing import List

from database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Hotel(Model):
    __tablename__ = 'hotels'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(unique=True)
    country: Mapped[str]
    city: Mapped[str]
    address: Mapped[str]

    rooms: Mapped[List["Room"]] = relationship(
        "Room",
        back_populates="hotel",
        cascade="all, delete-orphan",
        init=False
    )

    description: Mapped[str | None] = mapped_column(default=None)
