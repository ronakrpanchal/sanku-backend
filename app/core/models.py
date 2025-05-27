from pydantic import BaseModel, Field
from datetime import datetime
from beanie import Document


class ChatRequest(BaseModel):
    user_id: str
    chat_id: str
    query: str


class Chat(Document):
    user_id: str
    chat_id: str
    query: str
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "chats"


class Message(Document):
    user_id : str
    chat_id : str
    role : str
    content : str
    created_at : datetime = Field(default_factory=datetime.now)
    
    class Settings:
        name = "messages"
