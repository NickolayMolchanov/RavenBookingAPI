from fastapi import HTTPException
from starlette import status

from repository import BookingRepository


async def create_booking_service(data, session):
    if data.date_from >= data.date_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date when you leaving cannot be before date"
        )

    is_busy = await BookingRepository.is_room_busy(
        room_id=data.room_id,
        date_from=data.date_from,
        date_to=data.date_to,
        session=session
    )

    if is_busy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is already taken"
        )

    booking = await BookingRepository.create_booking(data, session)
    return booking