from pydantic import BaseModel


class SToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class TokenData(BaseModel):
    username: str | None = None