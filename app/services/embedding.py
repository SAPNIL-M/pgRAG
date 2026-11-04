from app.core.config import settings
import torch
from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self, model_name:str | None = None, device: str|None = None) -> None:
        self.model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model= SentenceTransformer(self.model_name,device=self.device)

    def embed_texts(self, texts : list[str], batch_size : int =64 )-> list[list[float]]:
        if not texts:
            return []
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True
        )
        return embeddings.tolist()

    def embed_query(self,query:str)->list[float]:
        embeddings = self.model.encode(query)
        return embeddings.tolist()

