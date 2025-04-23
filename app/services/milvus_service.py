from app.config.settings import settings
from pymilvus import MilvusClient

client = MilvusClient(uri=settings.MILVUS_URL, token=settings.MILVUS_TOKEN)
