from typing import List, Dict
from app.services.milvus_service import milvus_service
from app.services.embedding_service import get_text_embedding
from app.core.models import Message
from beanie.operators import And
from app.services.mongodb_service import first_usr

async def get_context(user_id: str, chat_id: str, query: str) -> List[Dict]:
    """
    Builds a context window for the chat model:
    - Top-k semantically similar messages from Milvus.
    - Last 5 chronological messages from chat history.
    """
    query_embedding = await get_text_embedding(query)
    
    if first_usr(user_id):
        return []

    # Semantic similarity from Milvus
    similar_messages = await milvus_service.search_similar_messages(
        user_id=user_id,
        query_embedding=query_embedding,
        chat_id=chat_id,
        limit=5,
    )

    # Last 5 recent messages from MongoDB
    recent_messages = await Message.find(
        And(Message.chat_id == chat_id)
    ).sort("-created_at").limit(5).to_list()

    recent_messages = list(reversed(recent_messages))

    # Format messages for LLM input
    def format_msg(m):
        return {
            "role": m["role"] if isinstance(m, dict) else m.role,
            "content": m["content"] if isinstance(m, dict) else m.content
        }

    return [format_msg(m) for m in similar_messages] + [format_msg(m) for m in recent_messages]