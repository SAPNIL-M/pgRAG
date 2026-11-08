from sqlalchemy import select

from app.services.embedding import EmbeddingService
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.retrieval import RetrievedChunk
from app.db.models import Chunk


class RetrievalService:

    def __init__(self,embedding_service: EmbeddingService |None = None) -> None:
        self.embedding_service = embedding_service or EmbeddingService()

    async def retrieve(self,
                       db:AsyncSession,
                       query:str,
                       top_k:int = 5,
                       document_id : int | None = None)-> list[RetrievedChunk]:

        embedded_query = self.embedding_service.embed_query(query)
        
        stmt=select(Chunk,Chunk.embedding.cosine_distance(embedded_query).label("cos_distance"))
        if document_id is not None:
            stmt=stmt.where(Chunk.document_id==document_id)
        stmt=(stmt.order_by("cos_distance").limit(top_k))


        query_fetch_relevant_chunk = (stmt)

        result = await db.execute(query_fetch_relevant_chunk)
        top_chunks=[]

        for chunk,distance in result.all():
            similarity = 1-distance
            top_chunks.append(RetrievedChunk(
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                text=chunk.text,
                page_number=chunk.page_number,
                score=similarity
            ))

        return top_chunks

def format_chunks_for_prompt(chunks : list[RetrievedChunk])-> str:
    if not chunks:
        return ""
    blocks=[f"[Page {chunk.page_number}]\n{chunk.text}" for chunk in chunks]
    formatted_chunk_blocks = "\n\n---\n\n".join(blocks)
    return formatted_chunk_blocks