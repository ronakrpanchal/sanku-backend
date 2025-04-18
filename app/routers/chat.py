from fastapi import APIRouter
from app.config.loggers import llm_logger
from app.services.llm_service import chat_with_stream
from app.models.general_models import ChatRequest
from fastapi.responses import StreamingResponse
import asyncio


router = APIRouter(tags=["Chat"])

@router.post("/chat")
async def chat(body:ChatRequest):
    data = await chat_with_stream(provider="opsadasjdaskjenai",query=body.query)
    llm_logger.info("chat route is working fine")
    return {"message":data}


async def make_bytes():
    for i in range(10):
        yield f"data: chunk {i}\n\n"
        await asyncio.sleep(0.1)


@router.post("/chat-stream")
async def chat_stream():
    return StreamingResponse(
        make_bytes(),
    )

