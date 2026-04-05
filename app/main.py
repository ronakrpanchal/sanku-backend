from fastapi import FastAPI
from app.routers import chat
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging
from app.services.milvus_service import init_milvus, close_milvus
from app.services.mongodb_service import init_db


logger = logging.getLogger(__name__)


async def init_services():
    try:
        await init_db()
        await init_milvus()
    except Exception:
        logger.exception("Background service initialization failed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(init_services())
    yield
    await close_milvus()


app = FastAPI(title="Sanku Backend", lifespan=lifespan)

app.include_router(chat.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"AI": "Hello Humans!"}
