from pydantic import BaseModel, ConfigDict


# Схемы комнаты
class SRoomBase(BaseModel):
    type: str | None = None
    price: float

class SRoomCreate(SRoomBase):
    hotel_id: int

class SRoomRead(SRoomBase):
    id: int
    hotel_id: int

    model_config = ConfigDict(from_attributes=True)


# Схемы отеля
class SHotelBase(BaseModel):
    name: str
    address: str
    description: str | None = None

class SHotelCreate(SHotelBase):
    pass

class SHotelRead(SHotelBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

