from app.config.settings import settings
from pymilvus import AsyncMilvusClient, MilvusClient, DataType
from typing import List, Dict, Any, Optional

COLLECTION_NAME = "chat_memory"
VECTOR_DIM = 1536


class MilvusService:
    def __init__(self):
        self.client = AsyncMilvusClient(
            uri=settings.MILVUS_URL, token=settings.MILVUS_TOKEN
        )
        self.sync_client = MilvusClient(
            uri=settings.MILVUS_URL, token=settings.MILVUS_TOKEN
        )
        self.collection_loaded = False

    async def init_collection(self):
        """Initialize the chat memory collection if it doesn't exist."""
        has_collection = self.sync_client.has_collection(COLLECTION_NAME)

        if not has_collection:
            schema = self.client.create_schema(auto_id=True, enable_dynamic_field=False)
            schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
            schema.add_field(
                field_name="user_id", datatype=DataType.VARCHAR, max_length=36
            )
            schema.add_field(
                field_name="chat_id", datatype=DataType.VARCHAR, max_length=36
            )
            schema.add_field(
                field_name="message", datatype=DataType.VARCHAR, max_length=1024
            )
            schema.add_field(
                field_name="role", datatype=DataType.VARCHAR, max_length=20
            )
            schema.add_field(
                field_name="created_at", datatype=DataType.VARCHAR, max_length=30
            )
            schema.add_field(
                field_name="embedding", datatype=DataType.FLOAT_VECTOR, dim=VECTOR_DIM
            )

            index_params = {
                "metric_type": "COSINE",
                "index_type": "HNSW",
            }

            await self.client.create_collection(
                collection_name=COLLECTION_NAME,
                schema=schema,
            )

            # Create index on the vector field
            await self.client.create_index(
                collection_name=COLLECTION_NAME,
                field_name="embedding",
                index_params=index_params,
            )

            # Create index on user_id for faster filtering
            await self.client.create_index(
                collection_name=COLLECTION_NAME,
                field_name="user_id",
                index_params={"index_type": "STL_SORT"},
            )

            # Create index on chat_id for faster filtering
            await self.client.create_index(
                collection_name=COLLECTION_NAME,
                field_name="chat_id",
                index_params={"index_type": "STL_SORT"},
            )

    async def insert_message(
        self,
        user_id: str,
        chat_id: str,
        message: str,
        embedding: List[float],
        role: str,
        created_at: str,
    ) -> str:
        """Insert a message with its embedding into the collection."""
        data = [
            {"user_id": user_id},
            {"chat_id": chat_id},
            {"message": message},
            {"role": role},
            {"created_at": created_at},
            {"embedding": embedding},
        ]

        res = await self.client.insert(COLLECTION_NAME, data)
        return res.primary_keys[0]

    async def batch_insert_messages(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Batch insert multiple messages with their embeddings."""
        data = [
            [m["user_id"] for m in messages],
            [m["chat_id"] for m in messages],
            [m["message"] for m in messages],
            [m["role"] for m in messages],
            [m["created_at"] for m in messages],
            [m["embedding"] for m in messages],
        ]

        res = await self.client.insert(COLLECTION_NAME, data)
        return res.primary_keys
    
    async def ensure_collection_loaded(self):
        if not self.collection_loaded:
            await self.client.load_collection(COLLECTION_NAME)
            self.collection_loaded = True

    async def search_similar_messages(
        self,
        user_id: str,
        query_embedding: List[float],
        limit: int = 5,
        chat_id: Optional[str] = None,
    ) -> List[Dict]:
        """Search for similar messages based on embedding similarity."""
        search_params = {"metric_type": "COSINE", "params": {"ef": 32}}

        output_fields = ["user_id", "chat_id", "message", "role", "created_at"]
        expr = f"user_id == '{user_id}'"

        if chat_id:
            expr += f" and chat_id == '{chat_id}'"

        # await self.client.load_collection(COLLECTION_NAME)
        await self.ensure_collection_loaded()

        results = await self.client.search(
            collection_name=COLLECTION_NAME,
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=limit,
            expr=expr,
            output_fields=output_fields,
        )

        hits = results[0]
        search_results = []

        for hit in hits:
            entity = hit.entity
            search_results.append(
                {
                    "id": hit.id,
                    "user_id": entity.get("user_id"),
                    "chat_id": entity.get("chat_id"),
                    "message": entity.get("message"),
                    "role": entity.get("role"),
                    "created_at": entity.get("created_at"),
                    "distance": hit.distance,
                }
            )

        return search_results

    async def delete_chat_messages(self, chat_id: str) -> int:
        """Delete all messages belonging to a specific chat."""
        expr = f"chat_id == '{chat_id}'"
        res = await self.client.delete(COLLECTION_NAME, expr)
        return res.delete_count

    async def delete_user_messages(self, user_id: str) -> int:
        """Delete all messages belonging to a specific user."""
        expr = f"user_id == '{user_id}'"
        res = await self.client.delete(COLLECTION_NAME, expr)
        return res.delete_count

    async def get_messages_by_chat_id(self, chat_id: str) -> List[Dict]:
        """Retrieve all messages for a specific chat."""
        expr = f"chat_id == '{chat_id}'"
        output_fields = ["user_id", "message", "role", "created_at"]

        # await self.client.load_collection(COLLECTION_NAME)
        await self.ensure_collection_loaded()
        res = await self.client.query(COLLECTION_NAME, expr, output_fields)

        return res

    async def close(self):
        """Close the Milvus client connection."""
        await self.client.close()


milvus_service = MilvusService()


async def init_milvus():
    await milvus_service.init_collection()
    print("Milvus collection initialized.")


async def close_milvus():
    await milvus_service.close()
    print("Milvus connection closed.")
