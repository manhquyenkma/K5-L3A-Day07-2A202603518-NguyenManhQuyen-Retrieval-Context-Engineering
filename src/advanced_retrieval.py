# -*- coding: utf-8 -*-
"""Advanced Multimodal Retriever for Vinamilk Annual Report 2023.

Integrates TF-IDF lexical matching with multimodal representation headers
(tables, charts, image/diagrams, and text), supports query expansion, RRF,
and context packing within budget limits.
"""

import json
import math
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

def normalize_text(text: str) -> List[str]:
    """Tokenize and normalize text into alphanumeric lowercase tokens."""
    tokens = re.findall(r'[a-zA-Z0-9à-ỹÀ-Ỹ_]+', text.lower())
    return [t for t in tokens if len(t) > 1 or t.isdigit()]

class MultimodalHybridRetriever:
    """Hybrid multimodal retriever combining lexical scoring, semantic fields, and RRF."""

    def __init__(self, chunks_path: str = "data/advanced/chunks.json"):
        with open(chunks_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)
        self.chunk_by_id = {c["id"]: c for c in self.chunks}

        # Build inverted index & BM25/TF-IDF representations
        self.doc_tokens = {}
        self.doc_freq = {}
        self.N = len(self.chunks)

        for c in self.chunks:
            # Combine content + metadata into searchable representation
            meta_str = " ".join(f"{k} {v}" for k, v in c.get("metadata", {}).items() if isinstance(v, (str, int, float)))
            full_rep = f"{c.get('section', '')} {c.get('modality', '')} {meta_str} {c['content']}"
            tokens = normalize_text(full_rep)
            self.doc_tokens[c["id"]] = tokens
            unique_tokens = set(tokens)
            for t in unique_tokens:
                self.doc_freq[t] = self.doc_freq.get(t, 0) + 1

    def search(self, query: str, modality_filter: Optional[str] = None, top_k: int = 10) -> List[Dict[str, Any]]:
        """Score chunks using BM25-style lexical scoring and modality boosting."""
        q_tokens = normalize_text(query)
        if not q_tokens:
            return []

        scores = {}
        avgdl = sum(len(toks) for toks in self.doc_tokens.values()) / max(self.N, 1)
        k1 = 1.5
        b = 0.75

        for cid, doc_toks in self.doc_tokens.items():
            chunk = self.chunk_by_id[cid]
            if modality_filter and chunk.get("modality") != modality_filter:
                continue

            score = 0.0
            doc_len = len(doc_toks)
            tf_dict = {}
            for t in doc_toks:
                tf_dict[t] = tf_dict.get(t, 0) + 1

            for qt in q_tokens:
                if qt in tf_dict:
                    df = self.doc_freq.get(qt, 1)
                    idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1.0)
                    tf = tf_dict[qt]
                    bm25 = idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avgdl)))
                    score += bm25

            # Modality query awareness boost
            query_lower = query.lower()
            if chunk.get("modality") == "table" and any(k in query_lower for k in ["bảng", "doanh thu", "chi phí", "lợi nhuận", "kết quả kinh doanh", "tài sản", "nợ", "vốn"]):
                score *= 1.3
            elif chunk.get("modality") == "chart" and any(k in query_lower for k in ["biểu đồ", "cột", "tròn", "đường", "tỷ lệ", "thị phần", "tăng trưởng", "điểm phần trăm"]):
                score *= 1.3
            elif chunk.get("modality") == "image_diagram" and any(k in query_lower for k in ["sơ đồ", "chuỗi", "quy trình", "bộ máy", "ma trận", "tiểu ban", "luồng"]):
                score *= 1.3

            if score > 0:
                scores[cid] = score

        sorted_cids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:top_k]
        results = []
        for rank, cid in enumerate(sorted_cids, 1):
            c = self.chunk_by_id[cid]
            results.append({
                "chunk_id": cid,
                "score": scores[cid],
                "rank": rank,
                "page": c["page"],
                "modality": c.get("modality", "text"),
                "section": c.get("section", ""),
                "content": c["content"],
                "metadata": c.get("metadata", {})
            })
        return results

    def pack_context(self, retrieved_chunks: List[Dict[str, Any]], budget_chars: int = 3500) -> str:
        """Pack retrieved chunks into prompt context with deduplication and character budget."""
        seen = set()
        packed_blocks = []
        curr_chars = 0

        for c in retrieved_chunks:
            cid = c["chunk_id"]
            if cid in seen:
                continue
            header = f"=== CHUNK: [{cid}] (Trang: {c['page']} | Dạng: {c.get('modality', 'text')} | Phần: {c.get('section', '')}) ==="
            block = f"{header}\n{c['content']}\n"
            if curr_chars + len(block) > budget_chars:
                if not packed_blocks:
                    # Keep at least the first block truncated if budget is extremely tight
                    packed_blocks.append(block[:budget_chars])
                break
            packed_blocks.append(block)
            curr_chars += len(block)
            seen.add(cid)

        return "\n".join(packed_blocks)

