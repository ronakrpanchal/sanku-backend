from fastapi import FastAPI
from app.routers import chat
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.config.settings import settings

app = FastAPI(title="Sanku Backend")

app.include_router(chat.router)
app.add_middleware(SessionMiddleware, secret_key=settings.FASTAPI_KEY)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"AI":"Hello Humans!"}

