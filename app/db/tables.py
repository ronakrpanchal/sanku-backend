from typing import Optional
import uuid
from sqlmodel import Field, SQLModel, create_engine, Session
from app.config.settings import settings
from typing import Annotated
from fastapi import Depends


connect_args = {"check_same_thread": False}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)


def create_db_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=uuid.uuid5, primary_key=True)
    name: str
    email: str
    age: int
