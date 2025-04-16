from pydantic_settings import BaseSettings

class Settings(BaseSettings):
   GROQ_API_KEY:str
   OPENAI_API_KEY:str



settings = Settings()