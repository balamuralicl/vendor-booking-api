from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.vendor import VendorCreate, Vendor
from app.models.vendor import Vendor as VendorModel
from app.deps.db import get_db
from uuid import uuid4
from typing import List
from opentelemetry import trace
import logging

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

router = APIRouter()

@router.post("/", response_model=Vendor)
async def create_vendor(vendor: VendorCreate, db: AsyncSession = Depends(get_db)):
    with tracer.start_as_current_span("create_vendor_logic"):
        logger.info(f"Creating vendor: {vendor.name}")
        vendor_id = str(uuid4())
        db_vendor = VendorModel(id=vendor_id, **vendor.dict())
        db.add(db_vendor)
        await db.commit()
        await db.refresh(db_vendor)
        logger.info(f"Vendor created with id={db_vendor.id}")
        return db_vendor


@router.get("/", response_model=List[Vendor])
async def list_vendors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(VendorModel))
    return result.scalars().all()

@router.get("/{vendor_id}", response_model=Vendor)
async def get_vendor(vendor_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(VendorModel).where(VendorModel.id == vendor_id))
    vendor = result.scalar_one_or_none()
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor
