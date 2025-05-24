from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone
from beanie import Document


class ChatRequest(BaseModel):
    user_id: str
    chat_id: str
    query: str


class Chat(Document):
    user_id: str
    chat_id: str
    query: str
    created_at: datetime = datetime.now(timezone.utc)

    class Settings:
        collection_name = "chats"


class Message(Document):
    pass
