from fastapi import APIRouter, HTTPException
from starlette import status

from models.user import User
from schemas.user import SUserCreate

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/create_user", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(data: SUserCreate):
    