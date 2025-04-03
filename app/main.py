from fastapi import FastAPI
from app.routes import chat


app = FastAPI(title="Gymbro Backend")

app.include_router(chat.router,tags=["Chat"],prefix="/chat")


@app.get("/")
async def root():
    return {"AI":"Hello Humans!"}