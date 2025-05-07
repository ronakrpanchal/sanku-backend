import contextvars
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from fastapi import Depends
from typing import Annotated, AsyncGenerator, Optional
from app.config.settings import settings

session_context = contextvars.ContextVar[Optional[AsyncSession]](
    "session_context", default=None
)

engine = create_async_engine(url=settings.DATABASE_URL, echo=True)


async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator:
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
