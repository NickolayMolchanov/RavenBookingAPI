from pydantic import BaseModel


class SToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

class STokenData(BaseModel):
    username: str | None = None