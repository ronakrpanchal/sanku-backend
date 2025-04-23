from fastapi import APIRouter
from app.config.loggers import llm_logger
from app.services.chat_service import chat_with_stream
from app.models.general_models import ChatRequest
from fastapi.responses import StreamingResponse
from app.utils.prompt_utils import prompt_render
from app.models.prompt_models import ChatPrompt


router = APIRouter(tags=["Chat"])


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
