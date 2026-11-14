"""Day 7 — Agentic RAG: LLM-driven agent with retrieval tools.

Uses Google Gemini API for the controller (LLM with tool-calling).
Compatible with the Day 7 starter agent loop interface.
"""
import json
import os
import time
from typing import Any
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════
# Context packing (from starter baseline, extended)
# ═══════════════════════════════════════════════════════════════════
def pack_context(
    results: list[dict[str, Any]],
    budget: int = 1500,
    dedup: bool = True,
) -> tuple[str, list[str]]:
    """Pack retrieved chunks into a context string within budget.

    Returns (context_string, list_of_chunk_ids_included).
    """
    blocks, ids, seen = [], [], set()
    for c in results:
        cid = c["id"]
        if dedup and cid in seen:
            continue
        seen.add(cid)
        block = f"[{cid} | {c.get('source', '')} | trang {c.get('page', '?')}]\n{c['text']}"
        candidate = "\n\n".join(blocks + [block])
        if len(candidate) <= budget:
            blocks.append(block)
            ids.append(cid)
    return "\n\n".join(blocks), ids


# ═══════════════════════════════════════════════════════════════════
# LLM Controllers (Gemini & OpenAI / OpenRouter)
# ═══════════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """Bạn là trợ lý trả lời câu hỏi dựa trên tài liệu "Sổ tay Sinh viên 2024".

QUY TẮC BẮT BUỘC:
1. Chỉ trả lời dựa trên bằng chứng (evidence) từ tài liệu được cung cấp qua tool search.
2. Mỗi câu trả lời PHẢI có citation dạng [chunk-id] tham chiếu trực tiếp đến chunk trong ngữ cảnh chứa bằng chứng. Ví dụ: "...theo quy định 15 tiết [B_so-tay-sinh-vien-2024_p1_c0]".
3. Nếu tài liệu không chứa đủ thông tin để trả lời câu hỏi (hoặc câu hỏi về chủ đề không có trong sổ tay), bạn PHẢI từ chối trả lời: answer = "Không đủ bằng chứng để trả lời." và citations = [].
4. KHÔNG bịa đặt thông tin. KHÔNG suy diễn ngoài tài liệu.

ĐỊNH DẠNG TRẢ LỜI (BẮT BUỘC LÀ JSON DUY NHẤT):
- Khi cần tìm kiếm:
  {"action": "search", "query": "từ khóa tìm kiếm trọng tâm"}
- Khi đã đủ bằng chứng để trả lời:
  {"action": "answer", "answer": "Nội dung trả lời ngắn gọn, chính xác kèm [chunk-id].", "citations": ["chunk-id"]}
- Khi không đủ bằng chứng:
  {"action": "answer", "answer": "Không đủ bằng chứng để trả lời.", "citations": []}"""


class OpenAIController:
    """LLM controller using OpenAI-compatible API (OpenRouter, OpenAI, etc.)."""

    def __init__(
        self,
        model_name: str = "openai/gpt-4o-mini",
        api_key: str | None = None,
        base_url: str | None = None,
    ):
        from openai import OpenAI
        self.api_key = (
            api_key
            or os.environ.get("OPENROUTER_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or ""
        )
        self.base_url = (
            base_url
            or os.environ.get("OPENROUTER_BASE_URL")
            or "https://openrouter.ai/api/v1"
        )
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.model_name = model_name

    def decide(
        self, question: str, history: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Call LLM to decide: search or answer."""
        user_msg = f"Câu hỏi: {question}"
        if history:
            ctx = history[-1]
            if ctx.get("context"):
                user_msg += f"\n\nTài liệu đã tìm được:\n{ctx['context']}"
                user_msg += f"\n\nCác query đã dùng: {ctx.get('queries', [])}"
                user_msg += "\n\nHãy xem xét kỹ: Nếu đã có bằng chứng để trả lời, trả về action answer kèm citation [chunk-id]. Nếu chắc chắn không có bằng chứng trong sổ tay, trả về action answer từ chối với answer: 'Không đủ bằng chứng để trả lời.' và citations: []. Nếu cần tìm thêm, trả về action search."
            else:
                user_msg += "\n\nChưa có tài liệu. Hãy search từ khóa để tìm bằng chứng."
        else:
            user_msg += "\n\nHãy search từ khóa để tìm bằng chứng trước khi trả lời."

        resp = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
        )
        content = resp.choices[0].message.content.strip()

        import re
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            try:
                res = json.loads(match.group())
                if res.get("action") in ("search", "answer"):
                    return res
            except Exception:
                pass

        if history and any(h.get("context") for h in history):
            return {"action": "answer", "answer": content, "citations": []}
        return {"action": "search", "query": question}


class GeminiController:
    """LLM controller using Google Gemini API."""

    def __init__(self, model_name: str = "gemini-3.5-flash-lite", api_key: str | None = None):
        from google import genai
        self.api_key = (
            api_key
            or os.environ.get("GOOGLE_API_KEY")
            or ""
        )
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name

    def decide(
        self, question: str, history: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Call Gemini to decide: search or answer."""
        user_msg = f"Câu hỏi: {question}"
        if history:
            ctx = history[-1]
            if ctx.get("context"):
                user_msg += f"\n\nTài liệu đã tìm được:\n{ctx['context']}"
                user_msg += f"\n\nCác query đã dùng: {ctx.get('queries', [])}"
                user_msg += "\n\nHãy xem xét: Nếu có đủ bằng chứng, trả về action answer kèm citation [chunk-id]. Nếu tài liệu không có thông tin, trả về action answer từ chối với answer: 'Không đủ bằng chứng để trả lời.' và citations: []. Nếu cần tìm thêm, trả về action search."
            else:
                user_msg += "\n\nChưa có tài liệu. Hãy search để tìm bằng chứng."
        else:
            user_msg += "\n\nHãy search để tìm bằng chứng trước khi trả lời."

        response = None
        for attempt in range(5):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=user_msg,
                    config={
                        "system_instruction": SYSTEM_PROMPT,
                        "response_mime_type": "application/json",
                    },
                )
                break
            except Exception as e:
                if ("429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "503" in str(e)) and attempt < 4:
                    time.sleep(8 * (attempt + 1))
                    continue
                raise e

        text = response.text.strip() if response else ""

        import re
        match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
        if match:
            try:
                action = json.loads(match.group())
                if action.get("action") in ("search", "answer"):
                    return action
            except json.JSONDecodeError:
                pass

        if history and any(h.get("context") for h in history):
            return {"action": "answer", "answer": text, "citations": []}
        return {"action": "search", "query": question}


def get_default_controller():
    """Factory to get the best available controller."""
    # Always prioritize GeminiController with user's key
    return GeminiController()


# ═══════════════════════════════════════════════════════════════════
# Agent Loop
# ═══════════════════════════════════════════════════════════════════
def run_agent(
    question: str,
    controller: GeminiController,
    retriever,  # Any retriever with .search() method
    *,
    filters: dict[str, Any] | None = None,
    max_searches: int = 3,
    top_k: int = 5,
    budget: int = 1500,
    strategy_name: str = "unknown",
) -> dict[str, Any]:
    """Run the agent loop: search → accumulate context → answer.

    Returns trace dict with status, answer, citations, events, timing, etc.
    """
    if not question.strip():
        raise ValueError("question cannot be empty")

    start_time = time.perf_counter()
    history: list[dict[str, Any]] = []
    all_candidates: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    search_count = 0

    for step in range(max_searches + 1):
        try:
            action = controller.decide(question, history)
        except Exception as e:
            events.append({"event": "controller_error", "error": str(e)})
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "status": "error",
                "answer": f"Lỗi kết nối model: {e}",
                "citations": [],
                "events": events,
                "elapsed_ms": elapsed,
                "strategy": strategy_name,
                "search_count": search_count,
            }

        if action.get("action") == "search":
            if search_count >= max_searches:
                events.append({"event": "search_limit"})
                elapsed = (time.perf_counter() - start_time) * 1000
                return {
                    "status": "abstain",
                    "answer": "Không đủ bằng chứng để trả lời.",
                    "citations": [],
                    "events": events,
                    "elapsed_ms": elapsed,
                    "strategy": strategy_name,
                    "search_count": search_count,
                }

            query = action.get("query", question)
            if not isinstance(query, str) or not query.strip():
                query = question

            try:
                results = retriever.search(query, top_k=top_k, filters=filters)
            except Exception as e:
                events.append({"event": "retriever_error", "error": str(e), "query": query})
                continue

            all_candidates.extend(results)
            context, ctx_ids = pack_context(all_candidates, budget=budget)
            search_count += 1

            events.append({
                "event": "search",
                "query": query,
                "filter": filters,
                "num_results": len(results),
                "context_ids": ctx_ids,
                "context_chars": len(context),
            })

            history = [{
                "tool": "search",
                "queries": [e["query"] for e in events if e["event"] == "search"],
                "context": context,
                "context_ids": ctx_ids,
            }]

        elif action.get("action") == "answer":
            answer = action.get("answer", "")
            citations = action.get("citations", [])

            if not isinstance(citations, list):
                citations = []
            citations = [c for c in citations if isinstance(c, str)]

            # Get current context IDs
            ctx_ids = set()
            if history:
                ctx_ids = set(history[-1].get("context_ids", []))

            # Validate citations
            valid_citations = [c for c in citations if c in ctx_ids and f"[{c}]" in answer]

            if answer.strip() and valid_citations:
                events.append({"event": "answer", "valid_citations": len(valid_citations)})
                elapsed = (time.perf_counter() - start_time) * 1000
                return {
                    "status": "answered",
                    "answer": answer,
                    "citations": valid_citations,
                    "events": events,
                    "elapsed_ms": elapsed,
                    "strategy": strategy_name,
                    "search_count": search_count,
                }
            elif not citations and any(w in answer.lower() for w in ("không đủ", "không có", "chưa đủ")):
                events.append({"event": "abstain_intentional", "answer": answer})
                elapsed = (time.perf_counter() - start_time) * 1000
                return {
                    "status": "abstain",
                    "answer": "Không đủ bằng chứng để trả lời.",
                    "citations": [],
                    "events": events,
                    "elapsed_ms": elapsed,
                    "strategy": strategy_name,
                    "search_count": search_count,
                }
            else:
                # No valid citations or empty answer → abstain
                events.append({
                    "event": "invalid_or_missing_citations",
                    "answer_given": answer[:200],
                    "citations_given": citations,
                    "valid_in_context": list(ctx_ids),
                })
                elapsed = (time.perf_counter() - start_time) * 1000
                return {
                    "status": "abstain",
                    "answer": "Không đủ bằng chứng để trả lời.",
                    "citations": [],
                    "events": events,
                    "elapsed_ms": elapsed,
                    "strategy": strategy_name,
                    "search_count": search_count,
                }
        else:
            events.append({"event": "invalid_action", "raw": str(action)[:200]})

    # Exhausted all steps
    elapsed = (time.perf_counter() - start_time) * 1000
    return {
        "status": "abstain",
        "answer": "Không đủ bằng chứng để trả lời.",
        "citations": [],
        "events": events,
        "elapsed_ms": elapsed,
        "strategy": strategy_name,
        "search_count": search_count,
    }

