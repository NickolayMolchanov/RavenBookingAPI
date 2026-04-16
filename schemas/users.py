from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class SUserBase(BaseModel):
    username: str
    email: EmailStr


class SUserCreate(SUserBase):
    password: str = Field(min_length=6, max_length=72)

class SUserRead(SUserBase):
    id: int
    created_at: datetime
    is_active: bool = True
    role: str

    model_config = ConfigDict(from_attributes=True)

class SUserInDB(SUserRead):
    hashed_password: str
