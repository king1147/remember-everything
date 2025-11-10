from fastapi import FastAPI
from api.routes import router


app = FastAPI(
    title="Ticket Booking API",
    description="API for booking train tickets",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Ticket Booking API",
        "endpoints": {
            "docs": "/docs",
            "bookings": "/bookings"
        }
    }