from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from src.config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.DB_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session

class Base(DeclarativeBase):
    pass