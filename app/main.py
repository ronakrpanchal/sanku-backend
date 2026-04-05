from fastapi import FastAPI
from app.routers import chat
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.services.milvus_service import init_milvus, close_milvus
from app.services.mongodb_service import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_milvus()
    yield
    await close_milvus()


app = FastAPI(title="Sanku Backend", lifespan=lifespan)

app.include_router(chat.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"AI": "Hello Humans!"}
