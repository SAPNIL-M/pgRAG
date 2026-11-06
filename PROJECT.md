# Project 1: Document Q&A service (production-style RAG)

Goal: a running service where I upload a PDF, ask questions about it,
and get a streamed answer with page citations, backed by Postgres
instead of in-memory data. It rebuilds the pipeline I made following
Daniel Bourke's tutorial as a real service, then improves on it with
measured experiments. Test document: the Human Nutrition 2020 PDF.

## Definition of done
I can start the service, upload a PDF, ask a question, watch a streamed
answer with citations, and run an eval script that prints scores. I also
have a results table comparing my experiments against the Bourke
baseline.

## Core scope (required, days 1-8)
1. Postgres + pgvector (0.8.2 or later), with tables for documents and
   chunks.
2. Upload endpoint: parse PDF, chunk, embed, store.
3. Retrieval: vector search + Postgres full-text search, merged.
4. Question endpoint: retrieve chunks, call the model, return an answer.
5. Citations: document and page for each chunk used.
6. Streaming: the answer arrives token by token.
7. Model swap: one setting switches between Gemini and local Ollama.
   Model names (chat and embedding) are config values, never hardcoded.
8. Eval set of 20-30 questions with page-level labels, plus about 10
   held-out questions I don't look at until the end. Hand-written
   recall@k and MRR. Compare dense-only vs hybrid.
9. README with setup, short architecture, demo GIF, eval results.

## Experiment phase (days 9-11)
Baseline first: reproduce my Bourke configuration (same embedding model,
same chunking, vector search only) and score it. Then change one thing
at a time, in this order, scoring each against the baseline:
1. Embedding model: Bourke model vs Qwen3-Embedding-0.6B (optionally
   gemini-embedding-2 at 768 dims).
2. Chunking: baseline vs recursive 512-token vs page-aware chunks.
3. Reranker: a 0.6B cross-encoder over about 50 candidates. Log latency.
4. Optional: contextual retrieval on a slice of the book (it needs an
   LLM call per chunk, so watch free-tier limits).
Compare answers by hand on a sample of about 10 questions. Stop at the
end of day 11. Leftovers go to the next project's buffer.

## Stretch (after the above, in this order)
Metadata filtering, multi-document queries, simple frontend, Docker
polish, second textbook, generation-model comparison.

## Out of scope for this project
User accounts, non-PDF files, conversation memory. Parser
comparison (Docling etc.) moves to Project 3. BM25 extensions, SPLADE
and Ragas are deferred.

## Decided
- Layout: layered `app/` package with `api/`, `core/`, `db/`,
  `services/`, `schemas/`. Outside it: `tests/`, `eval/`, `alembic/`,
  `docker-compose.yml`, `pyproject.toml`, `.env.example`.
- Database access: SQLAlchemy 2.0 (async) for models and ordinary
  queries. The hybrid search query is handwritten SQL.
- Keyword search: Postgres full-text search. No BM25 comparison for now.
- No LangChain or other orchestration framework in this project.
- Environment: Windows 11, 16GB RAM, RTX 3060 (6GB VRAM).

## Open decision to raise in the design lesson
Embedding dimension and column type, before the first migration. Comparing
embedding models means vectors of different sizes. pgvector indexes
`vector` up to 2,000 dims and `halfvec` up to 4,000. Present the options
(for example one table per model, or a separate embeddings table) under
rule 4. Also check the Bourke model's input limit against my chunk sizes.

## Proposed in planning, not final
Present options and trade-offs per rule 4 when each comes up.
FastAPI (check whether its built-in SSE support is available in my
version before choosing a streaming library), Postgres + pgvector,
asyncpg, Alembic, PyMuPDF behind a small interface, Reciprocal Rank
Fusion, my own thin LLM interface (Gemini and Ollama classes),
pydantic-settings, uv, Docker Compose for Postgres, pytest, ruff.
Pin SQLAlchemy to a deliberate version (2.0.x unless I choose
otherwise). Check Postgres 18's Docker volume-mount change when
writing Compose. Verify Gemini free-tier limits and data-use terms
before sending any private documents through it.

## Day plan
1: Postgres + pgvector running, schema, design lesson.
2-3: Ingestion with embeddings stored.
4: Vector search from the database matches my notebook's results.
5: Keyword search and merge; eval set finished (needed for experiments).
6: FastAPI endpoints and citations.
7: Streaming and the model swap.
8: Eval comparison (dense vs hybrid), README draft.
9-11: Experiment phase, results table, README and demo GIF finished.