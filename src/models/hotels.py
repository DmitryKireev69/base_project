from src.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String

class HotelOrm(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]
