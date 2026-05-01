from database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Hotel(Model):
    __tablename__ = 'hotels'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(unique=True)
    country: Mapped[str]
    city: Mapped[str]
    adress: Mapped[str]
    desciption: Mapped[str | None] = mapped_column(default=None)

    rooms: Mapped["Room"] = relationship("Room", back_populates="hotel", cascade="all, delete-orphan")