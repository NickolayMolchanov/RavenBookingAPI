from fastapi import APIRouter, HTTPException
from starlette import status

from database import SessionDep
from repository import UserRepository
from schemas.users import SUserCreate, SUserRead

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user_router.post("", response_model=SUserRead, status_code=status.HTTP_201_CREATED)
async def add_user(user: SUserCreate, session: SessionDep):

    new_user = await UserRepository.add_user(user, session)

    return SUserRead.from_orm(new_user)

@user_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, session: SessionDep):
    db_user = await UserRepository.get_user(user_id, session)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this ID not found")
    return db_user