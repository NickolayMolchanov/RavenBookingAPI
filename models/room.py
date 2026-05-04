from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Model


class Room(Model):
    __tablename__ = 'rooms'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))


    hotel: Mapped["Hotel"] = relationship(
        "Hotel",
        back_populates="rooms",
        init=False
    )

    type: Mapped[int | None] = mapped_column(default=None)
    price: Mapped[float] = mapped_column(default=0.0)
