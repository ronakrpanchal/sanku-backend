from fastapi import FastAPI
from app.routers import chat, auth
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.config.settings import settings

app = FastAPI(title="Sanku Backend")

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
