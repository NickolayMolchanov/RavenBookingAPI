from typing import List
from fastapi import APIRouter, HTTPException
from starlette import status

from repository import BookingRepository
from schemas.bookings import SBookingCreate, SBookingRead
from database import SessionDep
from service.booking_service import create_booking_service


booking_router = APIRouter(
    prefix="/booking",
    tags=["booking"],
)

@booking_router.post("", response_model=SBookingRead, status_code=status.HTTP_201_CREATED)
async def create_booking(booking_request: SBookingCreate, session: SessionDep):
    new_booking = await create_booking_service(booking_request, session)
    return new_booking

@booking_router.get("/{user_id}", response_model=List[SBookingRead], status_code=status.HTTP_200_OK)
async def get_bookings_by_user(user_id: int, session: SessionDep):
    return await BookingRepository.get_bookings_by_user(user_id, session)

@booking_router.get("/{room_id}", response_model=List[SBookingRead], status_code=status.HTTP_200_OK)
async def get_bookings_by_room(room_id: int, session: SessionDep):
    return await BookingRepository.get_bookings_by_user(room_id, session)

@booking_router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, session: SessionDep):
    rm_book = await BookingRepository.remove_booking(booking_id, session)
    if rm_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return rm_book