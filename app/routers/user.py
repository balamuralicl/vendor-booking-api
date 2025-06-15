from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user import UserCreate, User
from app.models.user import User as UserModel
from app.deps.db import get_db
from uuid import uuid4
from typing import List

from opentelemetry import trace
import logging

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    with tracer.start_as_current_span("create_user_logic"):
        logger.info(f"Creating user with email={user.email}")
        user_id = str(uuid4())
        db_user = UserModel(id=user_id, **user.dict())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        logger.info(f"User created with id={db_user.id}")
        return db_user


@router.get("/", response_model=List[User])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel))
    users = result.scalars().all()
    return users

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
