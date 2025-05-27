from sentence_transformers import SentenceTransformer
from typing import List

# load once on import
_model = SentenceTransformer('all-MiniLM-L6-v2')

async def get_text_embedding(text: str) -> List[float]:
    """
    Synchronous embedding under the hood but exposed async.
    Returns a 384-dim vector.
    """
    return _model.encode(text).tolist()