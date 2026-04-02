from typing import List
from fastapi import APIRouter, HTTPException
from starlette import status

from database import SessionDep
from schemas.hotels import SHotelCreate, SHotelRead, SRoomRead, SRoomCreate
from repository import HotelRepository, RoomsRepository

hotel_router = APIRouter(
    prefix="/hotel",
    tags=["Hotel"]
)

# Hotels
@hotel_router.post("", response_model=SHotelRead, status_code=status.HTTP_201_CREATED)
async def create_hotel(data: SHotelCreate, session: SessionDep):
    new_hotel = await HotelRepository.add_hotel(data, session)
    return new_hotel

@hotel_router.get("/{hotel_id}", response_model=SHotelRead, status_code=status.HTTP_200_OK)
async def get_hotel_by_id(hotel_id: int, session: SessionDep):
    db_hotel= await HotelRepository.get_hotel(hotel_id, session)
    if db_hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel with this ID not found")
    return db_hotel

@hotel_router.get("", response_model=List[SHotelRead], status_code=status.HTTP_200_OK)
async def get_all_hotels(session: SessionDep):
    db_hotels = await HotelRepository.get_hotels(session)
    return db_hotels

@hotel_router.put("/{hotel_id}", response_model=SHotelRead, status_code=status.HTTP_200_OK)
async def update_hotel(hotel_id: int, hotel: SHotelCreate, session: SessionDep):
    upd_hotel = await HotelRepository.update_hotel(hotel_id, hotel, session)
    return upd_hotel

@hotel_router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel_by_id(hotel_id: int, session: SessionDep):
    rm_hotel = await HotelRepository.remove_hotel(hotel_id, session)
    if rm_hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return  rm_hotel

# Rooms
@hotel_router.post("/rooms", response_model=SRoomRead, status_code=status.HTTP_201_CREATED)
async def create_room(data: SRoomCreate, session: SessionDep):
    new_room = await RoomsRepository.add_room(data, session)
    return new_room

@hotel_router.get("/{room_id}", response_model=SRoomRead, status_code=status.HTTP_200_OK)
async def get_room_by_id(room_id: int, session: SessionDep):
    db_room = await RoomsRepository.get_room(room_id, session)
    if db_room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room with this ID not found")
    return db_room

@hotel_router.get("/rooms", response_model=List[SRoomRead], status_code=status.HTTP_200_OK)
async def get_all_rooms(session: SessionDep):
    db_rooms = await RoomsRepository.get_rooms(session)
    return db_rooms

@hotel_router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room_by_id(room_id: int, session: SessionDep):
    rm_room = await RoomsRepository.remove_room(room_id, session)
    if rm_room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return  rm_room