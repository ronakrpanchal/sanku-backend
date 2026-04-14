from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.config.loggers import llm_logger
from app.services.chat_service import chat_with_stream, normal_Chat
from fastapi.responses import StreamingResponse
from app.utils.prompt_utils import prompt_render
from app.schemas.prompt_schema import ChatPrompt, ChatContext
from app.services.mongodb_service import (
    create_chat_if_missing,
    get_chat_messages,
    get_user_chats,
    store_message,
)
from app.core.models import Message, ChatRequest
from app.services.milvus_service import milvus_service
from app.services.embedding_service import get_text_embedding
from app.utils.milvus_utils import get_context

router = APIRouter(tags=["Chat"])

@router.post("/chat")
async def chat(body: ChatRequest):
    llm_logger.info("chat route is working fine")
    chat_id = body.chat_id
    user_id = body.user_id
    query = body.query
    llm_logger.info(f"Chat ID: {chat_id}, User ID: {user_id}, Query: {query}")
    
    try:
        await create_chat_if_missing(user_id=user_id, chat_id=chat_id, query=query)
        llm_logger.info("Chat created or reused successfully")
        
        # Store user message in MongoDB
        msg_obj = Message(
            user_id=user_id,
            chat_id=chat_id,
            role="user",
            content=query
        )
        await store_message(msg_obj)
        llm_logger.info("Message object stored successfully")
        
        # Store user message in Milvus
        user_embedding = await get_text_embedding(query)
        await milvus_service.insert_message(
            user_id=user_id,
            chat_id=chat_id,
            message=query,
            role="user",
            embedding=user_embedding,
            created_at=msg_obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
        )
        llm_logger.info("User message inserted into Milvus successfully")
        
        # Get context for AI response
        context = await get_context(user_id=user_id, chat_id=chat_id, query=query)
        llm_logger.info("Context retrieved successfully")
        
        if not context:
            llm_logger.info("No context found, proceeding with query only")
        
        # Create proper ChatPrompt object
        chat_context = ChatContext(context=context) if context else None
        chat_prompt_obj = ChatPrompt(
            query=body.query, 
            context=chat_context
        )
        chat_prompt = prompt_render(prompt_obj=chat_prompt_obj)
        
        # Get AI response
        response = await normal_Chat(provider="groq", query=chat_prompt)
        
        # Store AI response in MongoDB
        ai_msg_obj = Message(
            user_id=user_id,
            chat_id=chat_id,
            role="ai",
            content=response
        )
        await store_message(ai_msg_obj)
        llm_logger.info("AI Message object stored successfully")
        
        # Store AI response in Milvus
        ai_embedding = await get_text_embedding(response)
        await milvus_service.insert_message(
            user_id=user_id,
            chat_id=chat_id,
            message=response,
            role="ai",
            embedding=ai_embedding,
            created_at=ai_msg_obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
        )
        llm_logger.info("AI message inserted into Milvus successfully")
        
        return {"response": response}
        
    except Exception as e:
        llm_logger.error(f"Error in chat route: {e}")
        # Return more structured error response
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "message": str(e)}
        )


@router.get("/chats/{user_id}")
async def list_chats(user_id: str):
    try:
        chats = await get_user_chats(user_id)
        unique_chats = []
        seen_chat_ids = set()

        for chat in chats:
            if chat.chat_id in seen_chat_ids:
                continue
            seen_chat_ids.add(chat.chat_id)
            unique_chats.append(chat)

        return {
            "chats": [
                {
                    "chat_id": chat.chat_id,
                    "title": (chat.query[:60] + "...") if len(chat.query) > 60 else chat.query,
                    "created_at": chat.created_at.isoformat(),
                }
                for chat in unique_chats
            ]
        }
    except Exception as e:
        llm_logger.error(f"Error while listing chats for user {user_id}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "message": str(e)},
        )


@router.get("/chats/{user_id}/{chat_id}/messages")
async def list_chat_messages(user_id: str, chat_id: str):
    try:
        messages = await get_chat_messages(user_id=user_id, chat_id=chat_id)
        return {
            "messages": [
                {
                    "id": str(message.id),
                    "role": message.role,
                    "content": message.content,
                    "created_at": message.created_at.isoformat(),
                }
                for message in messages
            ]
        }
    except Exception as e:
        llm_logger.error(f"Error while listing messages for user {user_id}, chat {chat_id}: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "message": str(e)},
        )

@router.post("/chat-stream")
async def chat_stream(body: ChatRequest):
    try:
        return StreamingResponse(
            chat_with_stream(provider="openai", query=""),
        )
    except Exception as e:
        return str(e)
