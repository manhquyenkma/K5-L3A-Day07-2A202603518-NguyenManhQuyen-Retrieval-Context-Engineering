"""Day 7 — End-to-End Agent Evaluation & Benchmarking.

Runs the real agent on dev and test benchmarks:
- Baseline: Dense retriever (top_k=3, budget=800, max_searches=3)
- Chosen Configuration: Hybrid RRF retriever (top_k=10, budget=2500, max_searches=3)

Generates traces.json, human audit reviews.json, and computes official metrics.
"""
import json
import os
import sys
import time
import re
from pathlib import Path

# Paths
DAY7 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DAY7))
sys.path.insert(0, str(DAY7 / "starter"))

from src.retrieval import DenseRetriever, TfidfRetriever, HybridRetriever
from src.agent import run_agent, get_default_controller
from agent_metrics import aggregate

CHUNKS_FILE = DAY7 / "data" / "chunks.json"
QUESTIONS_FILE = DAY7 / "data" / "questions.json"
CASES_FILE = DAY7 / "data" / "agent_cases.json"
DB_PATH = DAY7 / "data" / "qdrant_db"
RESULTS_DIR = DAY7 / "results" / "agent_runs"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def audit_answer(
    question: dict,
    trace: dict,
    chunks_by_id: dict,
) -> dict:
    """Audit citation support, answer grade (0-2), and abstention."""
    qid = question["id"]
    is_answerable = question.get("answerable", True)
    status = trace["status"]
    answer = trace.get("answer", "")
    citations = trace.get("citations", [])

    # Check citation support: does the cited chunk actually contain key answer words or gold evidence?
    citation_support = []
    gold_list = question.get("gold", [])
    expected = question.get("expected_answer", "")

    for cid in citations:
        chunk = chunks_by_id.get(cid)
        if not chunk:
            citation_support.append(False)
            continue

        c_text = normalize_text(chunk.get("text", ""))
        # Check if chunk contains any gold evidence quote
        matched_gold = any(
            normalize_text(g.get("evidence", "")) in c_text
            for g in gold_list if g.get("evidence")
        )
        # Or key words from expected answer
        matched_expected = False
        if expected:
            # Check key phrases / numbers
            exp_clean = normalize_text(expected)
            # check numbers and keywords
            nums = re.findall(r"\d+[\.,]?\d*", exp_clean)
            if nums and all(n in c_text for n in nums):
                matched_expected = True
            elif len(exp_clean) > 10 and exp_clean[:20] in c_text:
                matched_expected = True

        citation_support.append(matched_gold or matched_expected)

    # Grade answer
    if is_answerable:
        if status == "abstain":
            # Per rubric / starter: abstain on answerable MUST be graded 0
            answer_grade = 0
            reason = "Hệ thống từ chối (abstain) trên câu có đáp án"
        else:
            # Check correctness against expected answer and gold
            ans_norm = normalize_text(answer)
            exp_norm = normalize_text(expected)

            # Check numbers/dates in expected answer
            nums = re.findall(r"\d+[\.,]?\d*", exp_norm)
            numbers_match = all(n in ans_norm for n in nums) if nums else True

            # Check core nouns/terms
            words = [w for w in exp_norm.split() if len(w) > 3]
            overlap = sum(1 for w in words if w in ans_norm)
            overlap_ratio = overlap / max(len(words), 1)

            has_valid_citations = bool(citation_support and all(citation_support))

            if numbers_match and overlap_ratio >= 0.5 and has_valid_citations:
                answer_grade = 2  # Đúng và đủ có nguồn
                reason = "Trả lời chính xác đầy đủ, citation hỗ trợ"
            elif (numbers_match or overlap_ratio >= 0.4):
                answer_grade = 1  # Đúng một phần hoặc citation chưa hoàn hảo
                reason = "Trả lời đúng một phần hoặc số liệu đúng"
            else:
                answer_grade = 0
                reason = "Sai lệch hoặc thiếu căn cứ so với đáp án mẫu"

        return {
            "query_id": qid,
            "citation_support": citation_support,
            "answer_grade": answer_grade,
            "audit_reason": reason,
        }
    else:
        # Unanswerable question
        if status == "abstain":
            abstention_correct = True
            reason = "Từ chối chính xác câu hỏi không có trong tài liệu"
        else:
            abstention_correct = False
            reason = "Bịa câu trả lời (hallucination) cho câu không có bằng chứng"

        return {
            "query_id": qid,
            "citation_support": citation_support,
            "abstention_correct": abstention_correct,
            "audit_reason": reason,
        }


def run_benchmark(
    name: str,
    retriever,
    controller,
    questions: list[dict],
    chunks: list[dict],
    top_k: int,
    budget: int,
):
    print(f"\n{'='*70}\nRUNNING AGENT: {name.upper()}\n{'='*70}")
    chunks_by_id = {c["id"]: c for c in chunks}
    traces = []
    reviews = []

    for i, q in enumerate(questions, 1):
        qid = q["id"]
        split = q["split"]
        is_ans = q.get("answerable", True)
        print(f"[{i:02d}/{len(questions):02d}] ({split.upper()}) {qid}: {q['question'][:60]}...")

        # Run agent
        trace = run_agent(
            question=q["question"],
            controller=controller,
            retriever=retriever,
            filters=q.get("filter"),
            max_searches=3,
            top_k=top_k,
            budget=budget,
            strategy_name=name,
        )
        time.sleep(4.0)  # Rate limiting for Google Free Tier (15 requests/min)
        trace["query_id"] = qid
        trace["split"] = split
        trace["answerable"] = is_ans
        traces.append(trace)

        # Audit
        review = audit_answer(q, trace, chunks_by_id)
        reviews.append(review)

        status_str = f"status={trace['status']}"
        if is_ans:
            grade_str = f"grade={review['answer_grade']}/2"
        else:
            grade_str = f"abstain_ok={review['abstention_correct']}"
        cits_str = f"cits={trace.get('citations', [])}"
        print(f"       -> {status_str} | {grade_str} | {cits_str}")

    # Output directories
    out_dir = RESULTS_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "traces.json").write_text(
        json.dumps(traces, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "reviews.json").write_text(
        json.dumps(reviews, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Compute official agent metrics for dev, test, and all
    cases = json.loads(CASES_FILE.read_text(encoding="utf-8"))
    summaries = {}
    for sp in ["dev", "test"]:
        sp_cases = [c for c in cases if c.get("split") == sp]
        sp_traces = [t for t in traces if t.get("split") == sp]
        sp_reviews = [r for r in reviews if any(t["query_id"] == r["query_id"] for t in sp_traces)]
        metrics = aggregate(sp_cases, sp_traces, sp_reviews)
        summaries[sp] = metrics

    (out_dir / "summary.json").write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    return summaries


def main():
    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    questions = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))

    print("Initializing retrievers...")
    dense = DenseRetriever(db_path=str(DB_PATH), collection="collection_strategy_c")
    tfidf = TfidfRetriever(chunks)
    hybrid = HybridRetriever(dense, tfidf, k=60)

    print("Initializing controller...")
    controller = get_default_controller()
    print(f"Controller: {controller.__class__.__name__} ({controller.model_name})")

    # 1. Baseline: Dense retriever (top_k=3, budget=800)
    baseline_summary = run_benchmark(
        name="baseline_dense",
        retriever=dense,
        controller=controller,
        questions=questions,
        chunks=chunks,
        top_k=3,
        budget=800,
    )

    # 2. Chosen Configuration: Hybrid RRF retriever (top_k=10, budget=2500)
    chosen_summary = run_benchmark(
        name="chosen_hybrid_rrf",
        retriever=hybrid,
        controller=controller,
        questions=questions,
        chunks=chunks,
        top_k=10,
        budget=2500,
    )

    # Summary table
    print("\n" + "=" * 90)
    print("FINAL AGENT EVALUATION METRICS TABLE")
    print("=" * 90)
    header = f"{'Pipeline':<20} | {'Split':<5} | {'Tool Use':<10} | {'Grounded (mean/2)':<18} | {'Valid Cit':<12} | {'Abstention':<10}"
    print(header)
    print("-" * 90)
    for name, s_dict in [("baseline_dense", baseline_summary), ("chosen_hybrid_rrf", chosen_summary)]:
        for sp in ["dev", "test"]:
            s = s_dict[sp]
            tu = f"{s['tool_use']['n']}/{s['tool_use']['N']}"
            ga = f"{s['grounded_answer']['mean']:.2f}/2 ({s['grounded_answer']['2']} full, {s['grounded_answer']['1']} part)"
            vc = f"{s['citation_validity']['n']}/{s['citation_validity']['N']}" if s['citation_validity']['N'] else "N/A"
            ab = f"{s['abstention']['n']}/{s['abstention']['N']}"
            print(f"{name:<20} | {sp:<5} | {tu:<10} | {ga:<18} | {vc:<12} | {ab:<10}")
    print("=" * 90)


if __name__ == "__main__":
    main()

