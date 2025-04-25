from typing import Optional
import uuid
from sqlmodel import Field, SQLModel, create_engine, Session
from app.config.settings import settings
from typing import Annotated
from fastapi import Depends


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: str
    age: int


engine = create_engine(url=settings.DATABASE_URL, echo=True)


def create_db_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
