from pydantic import BaseModel
from typing import List

class VendorCreate(BaseModel):
    name: str
    type: str
    location: str
    slots_available: List[str]

class Vendor(VendorCreate):
    id: str
