from pydantic_settings import BaseSettings

class Settings(BaseSettings):
   GROQ_API_KEY:str
   OPENAI_API_KEY:str
   MILVUS_URL:str
   MILVUS_TOKEN:str
   FASTAPI_KEY:str
   GOOGLE_CLIENT_ID:str
   GOOGLE_CLIENT_SECRET:str
   FASTAPI_KEY:str
   FRONTEND_URL:str
   DATABASE_URL:str


   class Config:
      env_file = ".env"



settings = Settings()