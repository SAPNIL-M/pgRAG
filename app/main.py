from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="pg RAG",
    version="1.0.0",
    description="first rag app"
)

app.include_router(api_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}