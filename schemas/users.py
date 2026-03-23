from datetime import datetime
from typing import List
from pydantic import BaseModel, Field, ConfigDict

from bookings import SBookingRead

class SUserBase(BaseModel):
    username: str
    email: str


class SUserCreate(SUserBase):
    password: str

class SUserRead(SUserBase):
    id: int
    created_at: datetime
    bookings: List[SBookingRead] | None = None
