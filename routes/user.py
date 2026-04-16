from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db
from repository import UserRepository
from schemas.users import SUserCreate, SUserRead

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user_router.post("", response_model=SUserRead, status_code=status.HTTP_201_CREATED)
async def add_user(user: SUserCreate, session: AsyncSession = Depends(get_db)):
    new_user = await UserRepository.add_user(user, session)
    return SUserRead.from_orm(new_user)

@user_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db)):
    db_user = await UserRepository.get_user_by_id(user_id, session)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this ID not found")
    return db_user

@user_router.put("/{user_id}", response_model=SUserRead, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: SUserCreate, session: AsyncSession = Depends(get_db)):
    upd_user = await UserRepository.update_user(user_id, user, session)
    return upd_user

@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db)):
    rm_user = await UserRepository.remove_user(user_id, session)
    if rm_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this ID not found")
    return rm_user

# @user_router.get("/me", status_code=status.HTTP_200_OK)
# async def get_me(current_user: SUserRead = Depends(get_current_active_user())):
#     return current_user