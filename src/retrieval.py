"""Day 7 — Retrieval methods: Dense, TF-IDF Lexical, Hybrid (RRF).

Provides three retrieval strategies sharing a common interface,
plus a reranker wrapper for improvement experiments.
"""
import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import json
import math
import re
import time
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

# ── Tokeniser (shared by lexical methods) ───────────────────────────
def tokenize(text: str) -> list[str]:
    return re.findall(r'\w+', unicodedata.normalize('NFC', text).casefold())


# ═══════════════════════════════════════════════════════════════════
# 1. DENSE RETRIEVAL  (Qdrant + SentenceTransformers)
# ═══════════════════════════════════════════════════════════════════
class DenseRetriever:
    """Query the Day 6 Qdrant vector store with compatible embeddings."""

    def __init__(
        self,
        db_path: str,
        collection: str = "collection_strategy_c",
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    ):
        import qdrant_client
        self.client = qdrant_client.QdrantClient(path=db_path)
        self.collection = collection

        from sentence_transformers import SentenceTransformer
        try:
            self._model = SentenceTransformer(model_name, local_files_only=True)
        except Exception:
            self._model = SentenceTransformer(model_name)

    def search(
        self, query: str, *, top_k: int = 5, filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        vector = self._model.encode(query, normalize_embeddings=True).tolist()

        qf = None
        if filters:
            qf = Filter(must=[
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in filters.items()
            ])

        res = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            query_filter=qf,
            limit=top_k,
            with_payload=True,
        )

        hits: list[dict[str, Any]] = []
        for pt in res.points:
            p = pt.payload or {}
            hits.append({
                "id": p.get("chunk_id", str(pt.id)),
                "text": p.get("text", ""),
                "source_id": p.get("document_id", ""),
                "source": "so_tay_sinh_vien_2024",
                "page": p.get("page", 0),
                "metadata": {
                    "section": p.get("section", ""),
                    "title": p.get("title", ""),
                    "year": p.get("year", 2024),
                },
                "score": float(pt.score),
                "strategy": "dense",
            })
        return hits


# ═══════════════════════════════════════════════════════════════════
# 2. LEXICAL RETRIEVAL  (TF-IDF, offline, no external dependency)
# ═══════════════════════════════════════════════════════════════════
class TfidfRetriever:
    """TF-IDF retrieval over pre-loaded chunks (standard library only)."""

    def __init__(self, chunks: list[dict[str, Any]]):
        self.chunks = chunks
        counts = [Counter(tokenize(c["text"])) for c in chunks]
        n = len(chunks)
        df = Counter(t for row in counts for t in row)
        self.idf = {t: math.log((1 + n) / (1 + c)) + 1 for t, c in df.items()}
        self.vectors = [self._vec(row) for row in counts]

    def _vec(self, counts: Counter) -> dict[str, float]:
        v = {t: c * self.idf[t] for t, c in counts.items() if t in self.idf}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        return {t: x / norm for t, x in v.items()}

    def search(
        self, query: str, *, top_k: int = 5, filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        qv = self._vec(Counter(tokenize(query)))
        results = []
        for chunk, vec in zip(self.chunks, self.vectors):
            # Apply metadata filters
            if filters:
                meta = chunk.get("metadata", {})
                if not all(meta.get(k) == v or chunk.get(k) == v for k, v in filters.items()):
                    continue
            score = sum(val * vec.get(t, 0) for t, val in qv.items())
            if score > 0:
                results.append({**chunk, "score": score, "strategy": "tfidf"})
        return sorted(results, key=lambda c: (-c["score"], c["id"]))[:top_k]


# ═══════════════════════════════════════════════════════════════════
# 3. HYBRID RETRIEVAL  (Dense + TF-IDF via Reciprocal Rank Fusion)
# ═══════════════════════════════════════════════════════════════════
class HybridRetriever:
    """Reciprocal Rank Fusion of dense and lexical retrievers."""

    def __init__(self, dense: DenseRetriever, lexical: TfidfRetriever, k: int = 60):
        self.dense = dense
        self.lexical = lexical
        self.k = k  # RRF constant

    def search(
        self, query: str, *, top_k: int = 5, filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        # Fetch more candidates from each source for better fusion
        fetch_k = max(top_k * 3, 10)
        dense_hits = self.dense.search(query, top_k=fetch_k, filters=filters)
        lex_hits = self.lexical.search(query, top_k=fetch_k, filters=filters)

        scores: dict[str, float] = {}
        docs: dict[str, dict[str, Any]] = {}

        for rank, hit in enumerate(dense_hits, 1):
            cid = hit["id"]
            scores[cid] = scores.get(cid, 0) + 1.0 / (self.k + rank)
            docs[cid] = hit

        for rank, hit in enumerate(lex_hits, 1):
            cid = hit["id"]
            scores[cid] = scores.get(cid, 0) + 1.0 / (self.k + rank)
            if cid not in docs:
                docs[cid] = hit

        ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
        results = []
        for cid, score in ranked:
            doc = dict(docs[cid])
            doc["score"] = score
            doc["strategy"] = "hybrid_rrf"
            results.append(doc)
        return results


# ═══════════════════════════════════════════════════════════════════
# 4. RERANKER  (wraps any retriever, uses Gemini for reranking)
# ═══════════════════════════════════════════════════════════════════
class RerankerRetriever:
    """Fetch candidates from base retriever, then rerank with LLM scoring."""

    def __init__(self, base_retriever, model_name: str = "gemini-2.0-flash"):
        self.base = base_retriever
        self.model_name = model_name

    def search(
        self, query: str, *, top_k: int = 5, filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        # Fetch more candidates
        fetch_k = max(top_k * 3, 15)
        candidates = self.base.search(query, top_k=fetch_k, filters=filters)
        if len(candidates) <= top_k:
            return candidates

        # Build rerank prompt
        docs_text = ""
        for i, c in enumerate(candidates):
            docs_text += f"\n[Doc {i}] (id={c['id']}, page={c['page']})\n{c['text'][:300]}\n"

        prompt = (
            f"Given the question: \"{query}\"\n"
            f"Rank the following documents by relevance. "
            f"Return ONLY a JSON array of document indices sorted by relevance, most relevant first.\n"
            f"Example: [2, 0, 5, 1, 3, 4]\n{docs_text}"
        )

        try:
            from google import genai
            import os
            client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY", ""))
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            text = response.text.strip()
            # Extract JSON array from response
            import re as _re
            match = _re.search(r'\[[\d,\s]+\]', text)
            if match:
                indices = json.loads(match.group())
                reranked = []
                seen = set()
                for idx in indices:
                    if 0 <= idx < len(candidates) and idx not in seen:
                        seen.add(idx)
                        doc = dict(candidates[idx])
                        doc["score"] = 1.0 / (len(reranked) + 1)  # reciprocal rank
                        doc["strategy"] = f"reranked_{candidates[idx].get('strategy', 'unknown')}"
                        reranked.append(doc)
                    if len(reranked) >= top_k:
                        break
                return reranked
        except Exception as e:
            print(f"Reranker fallback (error: {e}), using base ranking")

        return candidates[:top_k]


# ═══════════════════════════════════════════════════════════════════
# Factory function
# ═══════════════════════════════════════════════════════════════════
def load_chunks(path: str | Path) -> list[dict[str, Any]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def create_retrievers(
    chunks_path: str | Path,
    qdrant_db_path: str,
    collection: str = "collection_strategy_c",
) -> dict[str, Any]:
    """Create all retrievers and return them in a dict."""
    chunks = load_chunks(chunks_path)
    dense = DenseRetriever(db_path=qdrant_db_path, collection=collection)
    tfidf = TfidfRetriever(chunks)
    hybrid = HybridRetriever(dense, tfidf)
    return {
        "dense": dense,
        "tfidf": tfidf,
        "hybrid": hybrid,
        "chunks": chunks,
    }

