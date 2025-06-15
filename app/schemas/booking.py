from pydantic import BaseModel

class BookingCreate(BaseModel):
    user_id: str
    vendor_id: str
    time_slot: str
    status: str = "pending"

class Booking(BookingCreate):
    id: str
