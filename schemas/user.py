from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SUserBase(BaseModel):
    username: str
    email: str

class SUserCreate(SUserBase):
    password: str = Field(min_length=6, max_length=128)

class SUser(SUserBase):
    id: int
    created_at: datetime
    is_active: bool
    role: str

    model_config = ConfigDict(from_attributes=True)