from pydantic import BaseModel
from typing import List, Optional


class ChatContext(BaseModel):
    context : Optional[List[str]] = None


class ChatPrompt(BaseModel):
    context: Optional[ChatContext] = None
    query: str
    character: str = "senku"
    filename: str = "chat_prompt.md"
