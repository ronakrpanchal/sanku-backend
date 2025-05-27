from fastapi import APIRouter
from app.config.loggers import llm_logger
from app.services.chat_service import chat_with_stream, normal_Chat
from app.schemas.general_schema import ChatRequest
from fastapi.responses import StreamingResponse
from app.utils.prompt_utils import prompt_render
from app.schemas.prompt_schema import ChatPrompt
from app.services.mongodb_service import store_chat, store_message
from app.core.models import Chat,Message
from uuid import UUID
from app.core.models import ChatRequest

router = APIRouter(tags=["Chat"])


@router.post("/chat")
async def chat(body: ChatRequest):
    llm_logger.info("chat route is working fine")
    chat_id = body.chat_id
    user_id = body.user_id
    query = body.query
    llm_logger.info(f"Chat ID: {chat_id}, User ID: {user_id}, Query: {query}")
    chat_obj = Chat(user_id=user_id, chat_id=chat_id, query=query)
    await store_chat(chat_obj)
    llm_logger.info("Chat object stored successfully")
    msg_obj = Message(
        user_id=user_id,
        chat_id=chat_id,
        role="user",
        content=query
    )
    await store_message(msg_obj)
    llm_logger.info("Message object stored successfully")
    chat_prompt = prompt_render(prompt_obj=ChatPrompt(query=body.query))
    try:
        response = await normal_Chat(provider="groq", query=chat_prompt)
        ai_msg_obj = Message(
            user_id=user_id,
            chat_id=chat_id,
            role="ai",
            content=response
        )
        await store_message(ai_msg_obj)
        llm_logger.info("AI Message object stored successfully")
        return {"response": response}
    except Exception as e:
        llm_logger.error(f"Error in chat route: {e}")
        return {"error": str(e)}
    

@router.post("/chat-stream")
async def chat_stream(body: ChatRequest):
    try:
        return StreamingResponse(
            chat_with_stream(provider="openai", query=""),
        )
    except Exception as e:
        return str(e)
