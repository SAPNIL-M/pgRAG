import tempfile
from pathlib import Path
from fastapi import APIRouter, Depends,UploadFile,File,HTTPException,status,Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.services.ingestion import ingest_pdf
from app.schemas.document import DocumentResponse


router = APIRouter(prefix="/documents",tags=["documents"])

@router.post("/upload",status_code=status.HTTP_201_CREATED,response_model=DocumentResponse)
async def upload_documents(file: UploadFile = File(...),
                           force_reingest:bool=Form(False),
                           db:AsyncSession = Depends(get_db_session)):
    
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400,detail="Only PDF files allowed")

    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = Path(temp_file.name)

    try:
        doc = await ingest_pdf(file_path=temp_path,force_reingest=force_reingest,db=db,filename=file.filename)
        return doc

    finally:
        temp_path.unlink(missing_ok=True)

    

