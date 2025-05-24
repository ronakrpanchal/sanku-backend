from fastapi import APIRouter
from app.config.loggers import llm_logger
from app.services.chat_service import chat_with_stream
from app.schemas.general_schema import ChatRequest
from fastapi.responses import StreamingResponse
from app.utils.prompt_utils import prompt_render
from app.schemas.prompt_schema import ChatPrompt
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

router = APIRouter(tags=["Chat"])


class ChatStreamRequestModel(BaseModel):
    user_id: UUID
    chat_id: Optional[UUID] = None
    query: str


@router.post("/chat")
async def chat(body: ChatRequest):
    llm_logger.info("chat route is working fine")
    chat_prompt = prompt_render(prompt_obj=ChatPrompt(query="Hello how you doing?"))
    return {"message": "it is fun"}


@router.post("/chat-stream")
async def chat_stream():
    try:
        return StreamingResponse(
            chat_with_stream(provider="openai", query="prodive me best eassy on nepal"),
        )
    except Exception as e:
        return str(e)
