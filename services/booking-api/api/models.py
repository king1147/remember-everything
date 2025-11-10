from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    train_name = Column(String, nullable=False)
    carriage_number = Column(Integer, nullable=False)
    seat_number = Column(Integer, nullable=False)
    time_of_creation = Column(DateTime, default=datetime.utcnow, nullable=False)
    time_of_departure = Column(DateTime, nullable=False)
    time_of_arrival = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Booking(id={self.id}, name={self.name}, train={self.train_name})>"