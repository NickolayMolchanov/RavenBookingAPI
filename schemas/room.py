from pydantic import BaseModel, ConfigDict


class SRoomBase(BaseModel):
    name: str
    type: str | None = None
    price: float

class SRoomCreate(SRoomBase):
    hotel_id: int

class SRoom(SRoomBase):
    id: int
    hotel_id: int

    model_config = ConfigDict(from_attributes=True)