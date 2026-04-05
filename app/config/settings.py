from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GROQ_API_KEY: str
    OPENAI_API_KEY: str
    MILVUS_URL: str
    MILVUS_TOKEN: str
    FASTAPI_KEY: str
    MONGODB_URL: str
    MONGODB_DB: str = "sanku"

    class Config:
        env_file = ".env"


settings = Settings()
