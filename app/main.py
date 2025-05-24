from fastapi import FastAPI
from app.routers import chat, auth
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.config.settings import settings
from contextlib import asynccontextmanager
from app.services.milvus_service import init_milvus, close_milvus


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_milvus()
    yield
    await close_milvus()


app = FastAPI(title="Sanku Backend", lifespan=lifespan)

app.include_router(chat.router)
app.include_router(auth.router)

app.add_middleware(SessionMiddleware, secret_key=settings.FASTAPI_KEY)


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
