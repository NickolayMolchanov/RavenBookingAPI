from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from repositories.booking_repository import BookingRepository
from schemas.booking import SBooking, SBookingCreate
from service.booking_service import create_booking_service

router = APIRouter(
    prefix="/booking",
    tags=["booking"],
)

@router.post("", response_model=SBooking, status_code=status.HTTP_201_CREATED)
async def create_booking(booking_request: SBookingCreate, session: AsyncSession = Depends(get_db)):
    new_booking = await create_booking_service(booking_request, session)
    return new_booking

@router.get("/{user_id}", response_model=List[SBooking], status_code=status.HTTP_200_OK)
async def get_bookings_by_user(user_id: int, session: AsyncSession = Depends(get_db)):
    return await BookingRepository.get_bookings_by_user(user_id, session)

@router.get("/{room_id}", response_model=List[SBooking], status_code=status.HTTP_200_OK)
async def get_bookings_by_room(room_id: int, session: AsyncSession = Depends(get_db)):
    return await BookingRepository.get_bookings_by_user(room_id, session)

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, session: AsyncSession = Depends(get_db)):
    rm_book = await BookingRepository.remove_booking(booking_id, session)
    if rm_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return rm_book