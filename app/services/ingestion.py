import hashlib
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.embedding import EmbeddingService 
from sqlalchemy import select
from pathlib import Path


from app.db.models import Document,Chunk
from app.services.pdf import extract_text_from_pdf
from app.services.chunker import chunk_pages


async def ingest_pdf (file_path :str | Path ,
                       db : AsyncSession,
                         embedding_service : EmbeddingService |None = None,
                           force_reingest: bool = False)->Document:

    # setting the path of the pdf
    path = Path(file_path)

    #setting up the model
    service = embedding_service or EmbeddingService()


    #opening and getting the new pdf file has in sha256 format
    with open(path,"rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()


    #checking if that file_hash matches the existiing file_hash in the database it then 
    # deciding based on the flag whether to reingest it into the db or not 
    sql_query = select(Document).where(Document.file_hash == file_hash)
    result = await db.execute(sql_query)
    existing_doc = result.scalar_one_or_none()
    if existing_doc :
        if not force_reingest:
            return existing_doc
        await db.delete(existing_doc)
        await db.flush()

    # parsing the pdf and extracting the total number of pages and the content in the pages
    total_pages,pages = extract_text_from_pdf(str(path))



    # adding to db to get id 
    doc_db = Document(filename=path.name,file_hash=file_hash,page_count=total_pages)
    db.add(doc_db)
    await db.flush()

    # adding chunks to the db under Chunk table
    chunks = chunk_pages(pages) 
    sentences_with_10_sentences = [c["text"] for c in chunks]
    embeddings = service.embed_texts(sentences_with_10_sentences)
    chunk_db=[]
    for vec,chunk in zip(embeddings,chunks):
        chunk_db.append(Chunk(document_id=doc_db.id,
                         chunk_index=chunk["chunk_index"],
                         page_number=chunk["page_number"],
                         text=chunk["text"],
                         embedding=vec
                         ))
    db.add_all(chunk_db)
    await db.commit()
    await db.refresh(doc_db)
    return doc_db