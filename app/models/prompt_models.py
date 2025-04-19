from pydantic import BaseModel
from typing import Optional


class ChatContext(BaseModel):
    pass


class ChatPrompt(BaseModel):
    context:Optional[ChatContext] = None
    query:str
    character:str = "senku"
    filename:str = "chat_prompt.md"

