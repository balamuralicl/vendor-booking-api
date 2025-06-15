from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.booking import BookingCreate, Booking
from app.models.booking import Booking as BookingModel
from app.models.user import User
from app.models.vendor import Vendor
from app.deps.db import get_db
from uuid import uuid4
from typing import List
from opentelemetry import trace
import logging

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

router = APIRouter()

@router.post("/", response_model=Booking)
async def create_booking(booking: BookingCreate, db: AsyncSession = Depends(get_db)):
    # Check user exists
    user = await db.get(User, booking.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check vendor and time slot
    vendor = await db.get(Vendor, booking.vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    if booking.time_slot not in vendor.slots_available:
        raise HTTPException(status_code=400, detail="Time slot not available")

    booking_id = str(uuid4())
    db_booking = BookingModel(id=booking_id, **booking.dict())
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking

@router.get("/", response_model=List[Booking])
async def list_bookings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookingModel))
    return result.scalars().all()

@router.get("/{booking_id}", response_model=Booking)
async def get_booking(booking_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookingModel).where(BookingModel.id == booking_id))
    booking = result.scalar_one_or_none()
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking
