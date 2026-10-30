# Project 1: Document Q&A service (production-style RAG)

Goal: a running service where I upload a PDF, ask questions about it,
and get a streamed answer with page citations, backed by Postgres
instead of in-memory data. It hardens the pipeline I built following
Daniel Bourke's tutorial (test document: the Human Nutrition 2020 PDF).

## Definition of done
I can start the service, upload a PDF, ask a question, watch a streamed
answer with citations, and run an eval script that prints scores.

## Core scope (required)
1. Postgres + pgvector, with tables for documents and chunks.
2. Upload endpoint: parse PDF, chunk, embed, store.
3. Retrieval: vector search + Postgres full-text search, merged.
4. Question endpoint: retrieve chunks, call the model, return an answer.
5. Citations: document and page for each chunk used.
6. Streaming: the answer arrives token by token.
7. Model swap: one setting switches between Gemini and local Ollama.
8. Small eval set (20-30 questions): compare vector-only vs hybrid.
9. README with setup, short architecture, demo GIF, eval result.

## Stretch (only after core is done, in this order)
Reranker, metadata filtering, multi-document queries, simple frontend,
Docker polish, better chunking compared using the eval set.

## Out of scope
User accounts, non-PDF files, conversation memory, LangChain.

## Decided
- Layout: layered `app/` package with `api/`, `core/`, `db/`,
  `services/`, `schemas/`. Outside it: `tests/`, `eval/`, `alembic/`,
  `docker-compose.yml`, `pyproject.toml`, `.env.example`.
- Database access: SQLAlchemy 2.0 (async) for models and ordinary
  queries. The hybrid search query is handwritten SQL.
- Environment: Windows 11, 16GB RAM, RTX 3060 (6GB VRAM).

## Proposed in planning, not final
These are the picks from planning. Still present the options and trade-offs
per rule 4 when each comes up, and let me choose.
FastAPI, Postgres + pgvector, async driver (asyncpg), Alembic, my
current local embedding model (check vector size before creating the
schema), PyMuPDF, Postgres full-text search, Reciprocal Rank Fusion, my
own thin LLM interface (Gemini and Ollama classes), Server-Sent Events,
pydantic-settings, uv, Docker Compose for Postgres, pytest, ruff.

## 8-day target
1: Postgres + pgvector running, schema, design lesson.
2-3: Ingestion with embeddings stored.
4: Vector search from the database matches my notebook's results.
5: Keyword search and merge; eval set drafted.
6: FastAPI endpoints and citations.
7: Streaming and the model swap.
8: Eval comparison, README, demo GIF.