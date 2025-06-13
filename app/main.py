from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from uuid import uuid4

app = FastAPI(title="Vendor Booking API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# In-Memory Datastores
# ----------------------
users = {}
vendors = {}
bookings = {}

# ----------------------
# Models
# ----------------------
class UserCreate(BaseModel):
    name: str
    email: str
    phone: str

class User(UserCreate):
    id: str

class VendorCreate(BaseModel):
    name: str
    type: str
    location: str
    slots_available: List[str]

class Vendor(VendorCreate):
    id: str

class BookingCreate(BaseModel):
    user_id: str
    vendor_id: str
    time_slot: str
    status: str = "pending"

class Booking(BookingCreate):
    id: str

# ----------------------
# Users Endpoints
# ----------------------
@app.post("/users", response_model=User)
def create_user(user: UserCreate):
    user_id = str(uuid4())
    new_user = User(id=user_id, **user.dict())
    users[user_id] = new_user
    return new_user

@app.get("/users", response_model=List[User])
def list_users():
    return list(users.values())

# ----------------------
# Vendors Endpoints
# ----------------------
@app.post("/vendors", response_model=Vendor)
def create_vendor(vendor: VendorCreate):
    vendor_id = str(uuid4())
    new_vendor = Vendor(id=vendor_id, **vendor.dict())
    vendors[vendor_id] = new_vendor
    return new_vendor

@app.get("/vendors", response_model=List[Vendor])
def list_vendors():
    return list(vendors.values())

# ----------------------
# Bookings Endpoints
# ----------------------
@app.post("/bookings", response_model=Booking)
def create_booking(booking: BookingCreate):
    if booking.vendor_id not in vendors:
        raise HTTPException(status_code=404, detail="Vendor not found")
    if booking.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    if booking.time_slot not in vendors[booking.vendor_id].slots_available:
        raise HTTPException(status_code=400, detail="Time slot not available")

    booking_id = str(uuid4())
    new_booking = Booking(id=booking_id, **booking.dict())
    bookings[booking_id] = new_booking
    return new_booking

@app.get("/bookings", response_model=List[Booking])
def list_bookings():
    return list(bookings.values())
