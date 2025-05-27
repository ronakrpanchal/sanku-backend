from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings
from beanie import init_beanie
from app.core.models import Chat, Message


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
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(database=client.sanku, document_models=[Chat, Message])
    
async def store_chat(chat:Chat):
    await chat.insert()
    
async def store_message(message: Message):
    await message.insert()
    
def first_usr(user_id:str):
    return Chat.find_one(Chat.user_id == user_id) is None
