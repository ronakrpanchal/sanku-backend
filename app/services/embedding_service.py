from fastembed import TextEmbedding
from typing import List

# Keep a single model instance and initialize lazily to reduce startup memory spikes.
_model: TextEmbedding | None = None


def _get_model() -> TextEmbedding:
    global _model
    if _model is None:
        _model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return _model

async def get_text_embedding(text: str) -> List[float]:
    """
    Synchronous embedding under the hood but exposed async.
    Returns a 384-dim vector.
    """
    model = _get_model()
    # FastEmbed returns an iterator of vectors; fetch the first vector for one input text.
    return next(model.embed([text])).tolist()