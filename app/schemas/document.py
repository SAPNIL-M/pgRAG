from datetime import datetime
from pydantic import BaseModel,ConfigDict

class DocumentResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id:int
    filename : str
    file_hash : str
    page_count : int
    created_at: datetime