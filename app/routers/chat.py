from fastapi import APIRouter
from app.config.loggers import llm_logger

router = APIRouter(tags=["Chat"],prefix="/chat")

@router.get("/")
async def chat():
    llm_logger.info("chat route is working fine")
    return {"message":"Welcome to Chat Route"}
