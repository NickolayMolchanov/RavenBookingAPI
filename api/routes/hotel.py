from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from repositories.hotel_repository import HotelRepository
from schemas.hotel import SHotel, SHotelCreate

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"],
)

@router.post("", response_model=SHotel, status_code=status.HTTP_201_CREATED)
async def create_hotel(data: SHotelCreate, session: AsyncSession = Depends(get_db)):
    new_hotel = await HotelRepository.add_hotel(data, session)
    return new_hotel

@router.get("/{hotel_id}", response_model=SHotel, status_code=status.HTTP_200_OK)
async def get_hotel_by_id(hotel_id: int, session: AsyncSession = Depends(get_db)):
    db_hotel= await HotelRepository.get_hotel(hotel_id, session)
    if db_hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel with this ID not found")
    return db_hotel

@router.get("", response_model=List[SHotel], status_code=status.HTTP_200_OK)
async def get_all_hotels(session: AsyncSession = Depends(get_db)):
    all_hotels = await HotelRepository.get_hotels(session)
    return all_hotels

@router.put("/{hotel_id}", response_model=SHotel, status_code=status.HTTP_200_OK)
async def update_hotel(hotel_id: int, hotel: SHotelCreate, session: AsyncSession = Depends(get_db)):
    upd_hotel = await HotelRepository.update_hotel(hotel_id, hotel, session)
    return upd_hotel

@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel_by_id(hotel_id: int, session: AsyncSession = Depends(get_db)):
    rm_hotel = await HotelRepository.remove_hotel(hotel_id, session)
    if rm_hotel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    return  rm_hotel