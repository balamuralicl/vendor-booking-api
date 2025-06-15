from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from app.db.session import Base

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    vendor_id: Mapped[str] = mapped_column(String, ForeignKey("vendors.id"))
    time_slot: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending")
