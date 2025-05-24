import uuid
from sqlmodel import Field, SQLModel
from app.core.models import UUIDModel, TimestampModel


class Chat(UUIDModel, TimestampModel, SQLModel, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    title: str = Field(default="Untitled Chat")


class Message(UUIDModel, TimestampModel, SQLModel, table=True):
    chat_id: uuid.UUID = Field(foreign_key="chat.id")
    role: str
    content: str
    feedback: str | None = None
    metadata: dict | None = None
