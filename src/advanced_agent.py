# -*- coding: utf-8 -*-
"""Advanced Multimodal Agent for Vinamilk Annual Report 2023.

Coordinates retrieval across text, tables, charts, and diagrams,
handles multi-hop synthesis, enforces citation grounding and strict abstention.
"""

import json
import os
import re
import time
from typing import Dict, Any, List, Optional
from google import genai
from google.genai import types

from src.advanced_retrieval import MultimodalHybridRetriever

SYSTEM_PROMPT = """Bạn là Chuyên gia Phân tích Báo cáo Thường niên & Phát triển Bền vững cấp cao của Vinamilk.
Nhiệm vụ của bạn là trả lời các câu hỏi về Báo cáo Thường niên 2023 của Vinamilk (HOSE: VNM) dựa DUY NHẤT trên các thông tin được truy xuất.

Dữ liệu truy xuất bao gồm 4 dạng thức thông tin chính:
1. Văn bản (Text): Thông điệp lãnh đạo, chiến lược Net Zero, quản trị, nhân sự.
2. Bảng biểu (Table): Báo cáo tài chính, cơ cấu tài sản, phát thải KNK, cơ cấu lao động.
3. Biểu đồ (Chart): Biểu đồ cột doanh thu, biểu đồ tròn cơ cấu thị trường, biểu đồ đường năng lượng tái tạo, biểu đồ thị phần ngành hàng.
4. Ảnh và sơ đồ (Image/Diagram): Sơ đồ chuỗi giá trị từ đồng cỏ đến bàn ăn, sơ đồ luồng kinh tế tuần hoàn Biogas, sơ đồ tổ chức bộ máy quản trị, sơ đồ công nghệ xử lý nước thải, ma trận rủi ro.

QUY TẮC CỐT LÕI:
1. Độ chính xác tuyệt đối: Nêu đúng số liệu, đơn vị tính (tỷ đồng, %, tCO2e, điểm phần trăm, v.v.), điều kiện và các mốc thời gian.
2. Trích dẫn nguồn (Citations): Mọi khẳng định thông tin trích xuất phải đi kèm mã định danh chunk trong ngoặc vuông, ví dụ [vnm_p154_tab01], [vnm_p42_img01], [vnm_p92_chr03]. Chỉ trích dẫn các chunk có thực trong ngữ cảnh được cung cấp.
3. Nguyên tắc từ chối (Abstention): Nếu thông tin cần thiết không xuất hiện trong ngữ cảnh, hoặc câu hỏi hỏi về các dự án/số liệu không được công bố (ví dụ: thị trường không có trong báo cáo, công thức mật, lương chi tiết từng cá nhân), bạn BẮT BUỘC trả lời chính xác:
"Không đủ bằng chứng để trả lời."
và KHÔNG trích dẫn bất kỳ chunk nào (citations rỗng). Tuyệt đối không suy đoán hay bịa đặt.
"""

class AdvancedGeminiController:
    """Controller using Google GenAI SDK (gemini-3.5-flash-lite) with rate-limit backoff."""

    def __init__(self, model_name: str = "gemini-3.5-flash-lite"):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def decide(self, prompt: str) -> str:
        max_retries = 5
        base_delay = 5.0
        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.0,
                        max_output_tokens=1024
                    )
                )
                return response.text or ""
            except Exception as e:
                err_str = str(e).lower()
                if "429" in err_str or "resource_exhausted" in err_str or "quota" in err_str:
                    wait_time = base_delay * (attempt + 1)
                    print(f"       [Gemini 429 Rate Limit] Backing off for {wait_time:.1f}s (attempt {attempt+1}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    print(f"       [Gemini Error] {e}")
                    raise e
        raise RuntimeError("Exceeded maximum retries for Gemini API")

class AdvancedAgent:
    """Agent running search tool, context accumulation, and answer synthesis."""

    def __init__(self, retriever: MultimodalHybridRetriever, controller: AdvancedGeminiController, max_searches: int = 2, context_budget: int = 3500):
        self.retriever = retriever
        self.controller = controller
        self.max_searches = max_searches
        self.context_budget = context_budget

    def run(self, query: str) -> Dict[str, Any]:
        start_time = time.time()
        events = []
        retrieved_all = []
        seen_cids = set()

        # Step 1: Tool search
        res1 = self.retriever.search(query, top_k=8)
        for r in res1:
            if r["chunk_id"] not in seen_cids:
                retrieved_all.append(r)
                seen_cids.add(r["chunk_id"])

        events.append({
            "event": "search",
            "query": query,
            "filter": None,
            "num_results": len(res1),
            "context_ids": [r["chunk_id"] for r in res1[:5]]
        })

        # Pack context within budget
        packed_context = self.retriever.pack_context(retrieved_all, budget_chars=self.context_budget)

        # Step 2: Synthesize Answer
        prompt = f"""{SYSTEM_PROMPT}

NGỮ CẢNH TRÍCH XUẤT TỪ BÁO CÁO THƯỜNG NIÊN 2023 CỦA VINAMILK:
{packed_context}

CÂU HỎI CỦA NGƯỜI DÙNG:
{query}

HƯỚNG DẪN TRẢ LỜI:
- Trả lời ngắn gọn, trực diện, đúng trọng tâm và chính xác từng số liệu/chi tiết.
- Trích dẫn mã chunk [vnm_...] ngay sau luận điểm tương ứng.
- Nếu không có thông tin trong ngữ cảnh trên, chỉ trả lời duy nhất câu: "Không đủ bằng chứng để trả lời."
"""
        raw_response = self.controller.decide(prompt).strip()

        # Extract citations
        citations = sorted(list(set(re.findall(r'\[(vnm_[a-zA-Z0-9_]+)\]', raw_response))))
        # Verify citations exist in retrieved context
        valid_citations = [c for c in citations if c in seen_cids]

        # Determine status
        is_abstain = "không đủ bằng chứng" in raw_response.lower() or len(raw_response) == 0

        if is_abstain:
            status = "abstain"
            final_answer = "Không đủ bằng chứng để trả lời."
            final_citations = []
            events.append({"event": "abstain_intentional", "answer": final_answer})
        else:
            status = "answered"
            final_answer = raw_response
            final_citations = valid_citations
            events.append({"event": "answer", "valid_citations": len(valid_citations)})

        elapsed_ms = int((time.time() - start_time) * 1000)

        return {
            "query": query,
            "status": status,
            "answer": final_answer,
            "citations": final_citations,
            "events": events,
            "elapsed_ms": elapsed_ms,
            "search_count": 1
        }
