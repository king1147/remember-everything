from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime
from .models import Booking
from .schemas import BookingCreate, BookingUpdate


def create_booking(db: Session, booking: BookingCreate) -> Booking:
    """Create a new booking"""
    db_booking = Booking(**booking.model_dump())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_booking(db: Session, booking_id: int) -> Optional[Booking]:
    """Get a booking by id"""
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_bookings(
        db: Session,
        limit: int = 100,
        train_name: Optional[str] = None
) -> List[Booking]:
    """Get all bookings"""
    query = db.query(Booking)

    if train_name:
        query = query.filter(Booking.train_name.ilike(f"%{train_name}%"))

    return query.limit(limit).all()


def update_booking(
        db: Session,
        booking_id: int,
        booking_update: BookingUpdate
) -> Optional[Booking]:
    """Update a booking"""
    db_booking = get_booking(db, booking_id)

    if not db_booking:
        return None

    update_data = booking_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_booking, field, value)

    db.commit()
    db.refresh(db_booking)
    return db_booking


def delete_booking(db: Session, booking_id: int) -> bool:
    """Delete a booking"""
    db_booking = get_booking(db, booking_id)

    if not db_booking:
        return False

    db.delete(db_booking)
    db.commit()
    return True


def check_seat_availability(
        db: Session,
        train_name: str,
        carriage_number: int,
        seat_number: int,
        time_of_departure: datetime,
        exclude_booking_id: Optional[int] = None
) -> bool:
    """Check if a seat is available for a specific train and departure time"""
    query = db.query(Booking).filter(
        and_(
            Booking.train_name == train_name,
            Booking.carriage_number == carriage_number,
            Booking.seat_number == seat_number,
            Booking.time_of_departure == time_of_departure
        )
    )

    if exclude_booking_id:
        query = query.filter(Booking.id != exclude_booking_id)

    return query.first() is None