from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatContext(BaseModel):
    context: Optional[List[Dict[str, Any]]] = None  # Changed to accept Dict format

class ChatPrompt(BaseModel):
    context: Optional[ChatContext] = None
    query: str
    character: str = "senku"
    filename: str = "chat_prompt.md"