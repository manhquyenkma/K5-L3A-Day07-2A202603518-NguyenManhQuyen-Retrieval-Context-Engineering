"""Day 7 — Benchmark: compare 3 retrieval methods on dev/test.

Runs Dense (Qdrant), TF-IDF, and Hybrid (RRF) on the same questions.
No LLM API key needed — this evaluates retrieval quality only.
"""
import json
import sys
import time
import statistics
from pathlib import Path

# Paths
DAY7 = Path(r"d:\AI_In_Action\K5-L3-Day07-Retrieval-Context-Engineering\K5-L3A-Day07-2A202603518-NguyenManhQuyen-Retrieval-Context-Engineering")
DAY6_DB = DAY7 / "data" / "qdrant_db"

CHUNKS_PATH = DAY7 / "data" / "chunks.json"
QUESTIONS_PATH = DAY7 / "data" / "questions.json"
RESULTS_DIR = DAY7 / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(DAY7))

# ── Load data ───────────────────────────────────────────────────────
print("=" * 70)
print("DAY 07 · RETRIEVAL BENCHMARK")
print("=" * 70)

chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))
questions = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
print(f"Loaded {len(chunks)} chunks, {len(questions)} questions")

# Separate answerable vs unanswerable
answerable_qs = [q for q in questions if q.get("answerable", True) is not False]
unanswerable_qs = [q for q in questions if q.get("answerable") is False]
print(f"  Answerable: {len(answerable_qs)}, Unanswerable: {len(unanswerable_qs)}")


# ── Evidence hit check ──────────────────────────────────────────────
def evidence_hit(chunk: dict, gold_list: list[dict]) -> bool:
    """Check if chunk contains evidence from any gold entry."""
    for g in gold_list:
        if (chunk.get("source_id") == g.get("source_id")
                and chunk.get("page") == g.get("page")
                and g.get("evidence", "") in chunk.get("text", "")):
            return True
    return False


def pack_context(results, budget=1500):
    blocks, ids, seen = [], [], set()
    for c in results:
        cid = c["id"]
        if cid in seen:
            continue
        seen.add(cid)
        block = f"[{cid} | {c.get('source','')} | trang {c.get('page','?')}]\n{c['text']}"
        if len("\n\n".join(blocks + [block])) <= budget:
            blocks.append(block)
            ids.append(cid)
    return "\n\n".join(blocks), ids


# ── Evaluate one retrieval method ───────────────────────────────────
def evaluate_retriever(retriever, name: str, qs: list[dict], top_k: int = 5, budget: int = 1500):
    """Run retriever on answerable questions, compute metrics."""
    traces = []
    for q in qs:
        if q.get("answerable") is False:
            continue  # Skip unanswerable for retrieval metrics

        start = time.perf_counter()
        filt = q.get("filter")
        results = retriever.search(q["question"], top_k=top_k, filters=filt)
        elapsed_ms = (time.perf_counter() - start) * 1000

        gold = q.get("gold", [])
        marked = [{**c, "hit": evidence_hit(c, gold)} for c in results]

        context, ctx_ids = pack_context(results, budget)
        context_hit = any(c["hit"] and c["id"] in ctx_ids for c in marked)

        traces.append({
            "query_id": q["id"],
            "split": q["split"],
            "question": q["question"],
            "strategy": name,
            "top_k": top_k,
            "budget_chars": budget,
            "gold": gold,
            "results": [{
                "id": c["id"],
                "page": c.get("page"),
                "score": round(c.get("score", 0), 4),
                "hit": c["hit"],
                "text_snippet": c["text"][:150],
            } for c in marked],
            "context": context,
            "context_ids": ctx_ids,
            "context_chars": len(context),
            "elapsed_ms": round(elapsed_ms, 2),
            "hit1": bool(marked and marked[0]["hit"]),
            "hit3": any(c["hit"] for c in marked[:3]),
            "hit5": any(c["hit"] for c in marked[:5]),
            "context_hit": context_hit,
        })
    return traces


def summarize_traces(traces, split=None):
    if split:
        traces = [t for t in traces if t["split"] == split]
    n = len(traces)
    if n == 0:
        return {"n": 0}
    return {
        "n": n,
        "hit1": sum(t["hit1"] for t in traces),
        "hit1_pct": round(sum(t["hit1"] for t in traces) / n * 100, 1),
        "hit3": sum(t["hit3"] for t in traces),
        "hit3_pct": round(sum(t["hit3"] for t in traces) / n * 100, 1),
        "hit5": sum(t["hit5"] for t in traces),
        "hit5_pct": round(sum(t["hit5"] for t in traces) / n * 100, 1),
        "context_hit": sum(t["context_hit"] for t in traces),
        "context_hit_pct": round(sum(t["context_hit"] for t in traces) / n * 100, 1),
        "avg_context_chars": round(statistics.mean(t["context_chars"] for t in traces)),
        "median_ms": round(statistics.median(t["elapsed_ms"] for t in traces), 1),
    }


# ═══════════════════════════════════════════════════════════════════
# Create retrievers and run benchmark
# ═══════════════════════════════════════════════════════════════════
from src.retrieval import DenseRetriever, TfidfRetriever, HybridRetriever

print("\n[1/3] Initializing Dense Retriever (Qdrant + SentenceTransformers)...")
t0 = time.time()
dense = DenseRetriever(db_path=str(DAY6_DB), collection="collection_strategy_c")
print(f"  Dense retriever ready ({time.time()-t0:.1f}s)")

print("[2/3] Initializing TF-IDF Retriever...")
t0 = time.time()
tfidf = TfidfRetriever(chunks)
print(f"  TF-IDF index built ({time.time()-t0:.1f}s, {len(chunks)} docs)")

print("[3/3] Initializing Hybrid Retriever (RRF)...")
hybrid = HybridRetriever(dense, tfidf, k=60)
print("  Hybrid (RRF) ready\n")

# ── Run benchmarks ──────────────────────────────────────────────────
configs = [
    ("dense", dense, 5, 1500),
    ("tfidf", tfidf, 5, 1500),
    ("hybrid_rrf", hybrid, 5, 1500),
    # Improvement experiments
    ("dense_top10", dense, 10, 2500),
    ("hybrid_top10", hybrid, 10, 2500),
]

all_results = {}
for name, retriever, top_k, budget in configs:
    print(f"Running [{name}] (top_k={top_k}, budget={budget})...")
    traces = evaluate_retriever(retriever, name, answerable_qs, top_k=top_k, budget=budget)

    dev_summary = summarize_traces(traces, "dev")
    test_summary = summarize_traces(traces, "test")
    all_summary = summarize_traces(traces)

    all_results[name] = {
        "config": {"top_k": top_k, "budget": budget},
        "dev": dev_summary,
        "test": test_summary,
        "all": all_summary,
        "traces": traces,
    }

    # Save individual traces
    out_dir = RESULTS_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "traces.json").write_text(
        json.dumps(traces, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "summary.json").write_text(
        json.dumps({"dev": dev_summary, "test": test_summary, "all": all_summary},
                    ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

# ── Print comparison table ──────────────────────────────────────────
print("\n" + "=" * 95)
print("RETRIEVAL BENCHMARK — COMPARISON TABLE")
print("=" * 95)
header = f"{'Config':<18} | {'Split':<5} | {'Hit@1':<12} | {'Hit@3':<12} | {'Hit@5':<12} | {'Ctx Hit':<12} | {'Time(ms)':<8}"
print(header)
print("-" * 95)

for name in all_results:
    for split in ["dev", "test"]:
        s = all_results[name][split]
        if s["n"] == 0:
            continue
        print(
            f"{name:<18} | {split:<5} | "
            f"{s['hit1']}/{s['n']} ({s['hit1_pct']}%) | "
            f"{s['hit3']}/{s['n']} ({s['hit3_pct']}%) | "
            f"{s['hit5']}/{s['n']} ({s['hit5_pct']}%) | "
            f"{s['context_hit']}/{s['n']} ({s['context_hit_pct']}%) | "
            f"{s['median_ms']:<8}"
        )
    print("-" * 95)

print("=" * 95)

# ── Save combined summary ──────────────────────────────────────────
combined = {}
for name in all_results:
    combined[name] = {
        "config": all_results[name]["config"],
        "dev": all_results[name]["dev"],
        "test": all_results[name]["test"],
        "all": all_results[name]["all"],
    }

(RESULTS_DIR / "retrieval_comparison.json").write_text(
    json.dumps(combined, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"\nResults saved to {RESULTS_DIR}")
print("  retrieval_comparison.json — combined summary")
print("  <method>/traces.json — per-query traces")
print("  <method>/summary.json — per-method summary")

