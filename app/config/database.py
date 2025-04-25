from sqlalchemy.ext.asyncio import create_async_engine
from app.config.settings import settings
from typing import Annotated, AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from sqlmodel import SQLModel


engine = create_async_engine(url=settings.DATABASE_URL, echo=True)


async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator:
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
