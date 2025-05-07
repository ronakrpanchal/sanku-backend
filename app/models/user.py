import uuid
from sqlmodel import Field, SQLModel
import datetime


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: str


class UserOathToken(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    access_token: str
    refresh_token: str = Field(default=None)
    expires_at: int
    scopes: str = Field(default="")
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now(datetime.UTC)
    )
