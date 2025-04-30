import contextvars
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
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


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        token = session_context.set(session)
        try:
            yield session
        finally:
            session_context.reset(token)


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_current_session() -> AsyncSession:
    session = session_context.get()
    if session is None:
        raise RuntimeError("No database session found in context")
    return session
