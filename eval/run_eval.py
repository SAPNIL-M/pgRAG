import json,asyncio
from pathlib import Path

from app.db.session import async_session_factory
from app.services.retrieval import RetrievalService
from eval.metrics import hit_rate_at_k,mrr_at_k


async def main():
    data_path = Path("eval/data/ground_truth.jsonl")
    with open(data_path, "r", encoding="utf-8") as f:
        cases = [json.loads(line) for line in f]

    retriever = RetrievalService()
    
    k_list=[1,3,5]
    hitrates={k:[] for k in k_list}
    mrrs={k:[] for k in k_list}
    async with async_session_factory() as session:
        for case in cases:
            chunks = await retriever.retrieve(db=session,query=case["query"],top_k=5)
            retrieved_pages = [c.page_number for c in chunks]
            for k in k_list:
                hit_rate = hit_rate_at_k(retrieved_pages=retrieved_pages,target_pages=case["target_pages"],k=k)
                mrr = mrr_at_k(retrieved_pages=retrieved_pages,target_pages=case["target_pages"],k=k)
                hitrates[k].append(hit_rate)
                mrrs[k].append(mrr)

    print("\n=== Retrieval Benchmark Results (Dense Cosine Baseline) ===")
    print(f"{'k':<5} | {'Recall@k':<12} | {'MRR@k':<12}")
    print("-" * 35)

    for k in k_list:
        avg_hr = sum(hitrates[k])/len(hitrates[k])
        avg_mrr = sum(mrrs[k])/len(mrrs[k])
        print(f"{k:<5} | {avg_hr:<12.4f} | {avg_mrr:<12.4f}")




if __name__ == "__main__":
    asyncio.run(main())