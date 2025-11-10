from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import APIRouter

from config.database import engine, get_db
from . import schemas
from . import crud

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post(
    "/",
    response_model=schemas.BookingResponse,
    status_code=status.HTTP_201_CREATED
)
def create_booking(
        booking: schemas.BookingCreate,
        db: Session = Depends(get_db)
):
    """Create a new train ticket booking"""

    if booking.time_of_arrival <= booking.time_of_departure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arrival time must be after departure time"
        )

    is_available = crud.check_seat_availability(
        db=db,
        train_name=booking.train_name,
        carriage_number=booking.carriage_number,
        seat_number=booking.seat_number,
        time_of_departure=booking.time_of_departure
    )

    if not is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Seat {booking.seat_number} in carriage {booking.carriage_number} "
                   f"is already booked for train {booking.train_name} at {booking.time_of_departure}"
        )

    return crud.create_booking(db=db, booking=booking)


@router.get(
    "/",
    response_model=List[schemas.BookingResponse]
)
def get_bookings(
        limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
        train_name: Optional[str] = Query(None, description="Filter by train name"),
        db: Session = Depends(get_db)
):
    """Get all bookings"""
    return crud.get_bookings(db=db, limit=limit, train_name=train_name)


@router.get(
    "/{booking_id}",
    response_model=schemas.BookingResponse
)
def get_booking(
        booking_id: int,
        db: Session = Depends(get_db)
):
    """Get a specific booking by ID"""
    db_booking = crud.get_booking(db=db, booking_id=booking_id)

    if db_booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found"
        )

    return db_booking


@router.put(
    "/{booking_id}",
    response_model=schemas.BookingResponse
)
def update_booking(
        booking_id: int,
        booking_update: schemas.BookingUpdate,
        db: Session = Depends(get_db)
):
    """Update a booking"""

    existing_booking = crud.get_booking(db=db, booking_id=booking_id)
    if not existing_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found"
        )

    updated_departure = booking_update.time_of_departure or existing_booking.time_of_departure
    updated_arrival = booking_update.time_of_arrival or existing_booking.time_of_arrival

    # Validate that arrival time is after departure time
    if updated_arrival <= updated_departure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arrival time must be after departure time"
        )

    if any([
        booking_update.train_name,
        booking_update.carriage_number is not None,
        booking_update.seat_number is not None,
        booking_update.time_of_departure
    ]):
        train_name = booking_update.train_name or existing_booking.train_name
        carriage = booking_update.carriage_number or existing_booking.carriage_number
        seat = booking_update.seat_number or existing_booking.seat_number
        departure = booking_update.time_of_departure or existing_booking.time_of_departure

        is_available = crud.check_seat_availability(
            db=db,
            train_name=train_name,
            carriage_number=carriage,
            seat_number=seat,
            time_of_departure=departure,
            exclude_booking_id=booking_id
        )

        if not is_available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Seat {seat} in carriage {carriage} is already booked"
            )

    updated_booking = crud.update_booking(db=db, booking_id=booking_id, booking_update=booking_update)
    return updated_booking


@router.delete(
    "/{booking_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_booking(
        booking_id: int,
        db: Session = Depends(get_db)
):
    """Delete a booking"""
    success = crud.delete_booking(db=db, booking_id=booking_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Booking with id {booking_id} not found"
        )

    return None
