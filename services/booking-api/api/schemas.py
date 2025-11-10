from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BookingBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Passenger's first name")
    lastname: str = Field(..., min_length=1, max_length=100, description="Passenger's last name")
    train_name: str = Field(..., min_length=1, max_length=100, description="Name of the train")
    carriage_number: int = Field(..., gt=0, description="Carriage number")
    seat_number: int = Field(..., gt=0, description="Seat number")
    time_of_departure: datetime = Field(..., description="Departure time")
    time_of_arrival: datetime = Field(..., description="Arrival time")


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    lastname: Optional[str] = Field(None, min_length=1, max_length=100)
    train_name: Optional[str] = Field(None, min_length=1, max_length=100)
    carriage_number: Optional[int] = Field(None, gt=0)
    seat_number: Optional[int] = Field(None, gt=0)
    time_of_departure: Optional[datetime] = None
    time_of_arrival: Optional[datetime] = None


class BookingResponse(BookingBase):
    id: int
    time_of_creation: datetime

    class Config:
        from_attributes = True