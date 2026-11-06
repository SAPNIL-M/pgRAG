from pydantic import BaseModel

class RetrievedChunk(BaseModel):
    chunk_id : int
    document_id : int
    text : str
    page_number : int 
    score : float
