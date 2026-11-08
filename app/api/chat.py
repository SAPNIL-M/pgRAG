import json

from fastapi import APIRouter, Depends,status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession



from app.schemas.chat import ChatRequest
from app.db.session import get_db_session
from app.services.retrieval import RetrievalService,format_chunks_for_prompt
from app.services.generation import GenerationService

router = APIRouter(prefix="/chat",tags=["chat"])

@router.post("",status_code=status.HTTP_200_OK)
async def get_answer(request:ChatRequest,db:AsyncSession = Depends(get_db_session)):
    retrieval_service = RetrievalService()
    generation_service = GenerationService()
    async def event_stream():
        retrieved_chunks = await retrieval_service.retrieve(db=db,query=request.query,
                                                            top_k=request.top_k,
                                                            document_id=request.document_id)
        citations = [c.model_dump() for c in retrieved_chunks]
        yield f"data: {json.dumps({"type": "citations" , "data" : citations})}\n\n"

        context = format_chunks_for_prompt(retrieved_chunks)

        async for token in generation_service.generate_answer_stream(query=request.query,context=context):
            yield f"data: {json.dumps({"type":"token","data":token})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(event_stream(),media_type="text/event-stream")

