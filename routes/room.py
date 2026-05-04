from typing import List
from fastapi import HTTPException, APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from repositories.room_repository import RoomsRepository
from schemas.room import SRoom, SRoomCreate


router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)

@router.post("", response_model=SRoom, status_code=status.HTTP_201_CREATED)
async def create_room(data: SRoomCreate, session: AsyncSession = Depends(get_db)):
    new_room = await RoomsRepository.add_room(data, session)
    return new_room

@router.get("/{room_id}", response_model=SRoom, status_code=status.HTTP_200_OK)
async def get_room_by_id(room_id: int, session: AsyncSession = Depends(get_db)):
    db_room = await RoomsRepository.get_room(room_id, session)
    if db_room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room with this ID not found")
    return db_room

@router.get("", response_model=List[SRoom], status_code=status.HTTP_200_OK)
async def get_all_rooms(session: AsyncSession = Depends(get_db)):
    db_rooms = await RoomsRepository.get_rooms(session)
    return db_rooms

@router.put('', response_model=SRoom, status_code=status.HTTP_200_OK)
async def update_room(room_id: int, room: SRoomCreate, session: AsyncSession = Depends(get_db)):
    upd_room = await RoomsRepository.update_room(room_id, room, session)
    return upd_room

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room_by_id(room_id: int, session: AsyncSession = Depends(get_db)):
    rm_room = await RoomsRepository.remove_room(room_id, session)
    if rm_room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return  rm_room