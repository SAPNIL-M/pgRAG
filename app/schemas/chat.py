from pydantic import BaseModel,Field

class ChatRequest(BaseModel):
    query : str = Field(...,min_length=1,description="Search Term")
    top_k : int = Field(default=10,ge=1,le=50)
    document_id : int | None = None