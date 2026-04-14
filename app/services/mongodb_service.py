from pydantic import BaseModel
from pymongo import AsyncMongoClient
from app.config.settings import settings
from beanie import init_beanie
from app.core.models import Chat, Message
from typing import List


_mongo_client: AsyncMongoClient | None = None


# query: how's the weather today ?
# ai: some responses
"""
_
 3 collections
 user -> email,name, _id(this will be default in mongodb)
 chats -> user_id, _id, title (assume single chat rn)
 messages -> message_id(uuid), chat_id,role=ai/user,created_id,message
"""


async def init_db():
    global _mongo_client
    _mongo_client = AsyncMongoClient(settings.MONGODB_URL)
    database = _mongo_client.get_database(settings.MONGODB_DB)
    await init_beanie(database=database, document_models=[Chat, Message])
    
async def store_chat(chat:Chat):
    await chat.insert()
    
async def store_message(message: Message):
    await message.insert()
    
async def first_usr(user_id: str) -> bool:
    return await Chat.find_one(Chat.user_id == user_id) is None


async def create_chat_if_missing(user_id: str, chat_id: str, query: str) -> Chat:
    existing_chat = await Chat.find_one(Chat.user_id == user_id, Chat.chat_id == chat_id)
    if existing_chat:
        return existing_chat

    chat = Chat(user_id=user_id, chat_id=chat_id, query=query)
    await chat.insert()
    return chat


async def get_user_chats(user_id: str) -> List[Chat]:
    return await Chat.find(Chat.user_id == user_id).sort(-Chat.created_at).to_list()


async def get_chat_messages(user_id: str, chat_id: str) -> List[Message]:
    return await Message.find(
        Message.user_id == user_id,
        Message.chat_id == chat_id,
    ).sort(Message.created_at).to_list()
