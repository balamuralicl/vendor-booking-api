from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON
from app.db.session import Base

class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    slots_available: Mapped[list[str]] = mapped_column(JSON)
