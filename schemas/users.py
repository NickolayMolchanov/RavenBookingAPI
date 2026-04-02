from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SUserBase(BaseModel):
    username: str
    email: str


class SUserCreate(SUserBase):
    password: str

class SUserRead(SUserBase):
    id: int
    created_at: datetime
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class SUserInDB(SUserRead):
    hashed_password: str
