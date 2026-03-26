from pydantic import BaseModel
from pymongo import AsyncMongoClient
from app.config.settings import settings
from beanie import init_beanie
from app.core.models import Chat, Message


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
