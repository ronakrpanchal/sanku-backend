import uuid
from sqlmodel import Field, SQLModel
from app.core.models import UUIDModel, TimestampModel
import datetime


class Chat(UUIDModel, TimestampModel, SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    title: str = Field(default="Untitled Chat")


class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    chat_id: uuid.UUID = Field(foreign_key="chat.id")
    role: str
    content: str
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
    feedback: str | None = None
    metadata: dict | None = None
