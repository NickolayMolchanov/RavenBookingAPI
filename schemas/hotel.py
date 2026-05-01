from pydantic import BaseModel, ConfigDict


class SHotelBase(BaseModel):
    name: str
    country: str
    city: str
    address: str
    description: str | None = None

class SHotelCreate(SHotelBase):
    pass

class SHotel(SHotelBase):
    id: int

    model_config = ConfigDict(from_attributes=True)