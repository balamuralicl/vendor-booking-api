# app/schemas/user.py

from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str

class User(UserCreate):
    id: str