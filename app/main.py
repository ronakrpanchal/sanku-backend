from fastapi import FastAPI
from app.routers import chat


app = FastAPI(title="Sanku Backend")

app.include_router(chat.router)


@app.get("/")
async def root():
    return {"AI":"Hello Humans!"}