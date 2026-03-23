from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SBookingBase(BaseModel):
    room_id: int
    date_from: datetime
    date_to: datetime

class SBookingCreate(SBookingBase):
    user_id: int

class SBookingRead(SBookingBase):
    id: int
    user_id: int
    status: str

    model_config = ConfigDict(from_attributes=True)