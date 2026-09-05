"""Graph query over master_corpus_index.json, then TF-IDF on linked docs."""
from __future__ import annotations

import re

from retrieve_v2 import Retriever
from retriever_base import validate_retrieval_results

STOP = {
    "the", "and", "for", "are", "you", "your", "does", "do", "did", "how",
    "what", "where", "when", "who", "with", "from", "this", "that", "have",
    "has", "was", "were", "will", "can", "not", "any", "all", "our", "their",
}


def tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]{3,}", (text or "").lower()) if t not in STOP]


class GraphQueryRetriever:
    def __init__(self, index: dict, chunks: list[dict]):
        self.index = index
        self.chunks = chunks
        self.tfidf = Retriever(chunks) if chunks else None
        self.docs = index.get("documents") or []
        self.conflicts = index.get("contradictions_and_investigation_playbook") or []
        self.last_hits: list[dict] = []
        self.last_chunks: list[dict] = []
        self.graph_passages: dict[str, str] = {}
        for row in self.conflicts:
            cid = f"graph:{row.get('id')}"
            self.graph_passages[cid] = (
                f"Indexed conflict {row.get('id')} — {row.get('topic')}. "
                f"{row.get('description')} "
                f"Evidence A: {row.get('evidence_a')} "
                f"Evidence B: {row.get('evidence_b')} "
                f"Guidance: {row.get('agent_guidance')}"
            )

    def _overlap(self, query_tokens: list[str], text: str) -> float:
        if not query_tokens:
            return 0.0
        bag = set(tokens(text))
        if not bag:
            return 0.0
        return sum(1 for t in query_tokens if t in bag) / len(query_tokens)

    def graph_hits(self, query: str, limit: int = 6) -> list[dict]:
        qtoks = tokens(query)
        hits: list[dict] = []
        for doc in self.docs:
            blob = " ".join([
                doc.get("title") or "",
                doc.get("summary") or "",
                " ".join(doc.get("topics_covered") or []),
                " ".join(doc.get("key_entities") or []),
                doc.get("file") or "",
            ])
            score = self._overlap(qtoks, blob)
            if score <= 0:
                continue
            hits.append({
                "kind": "document",
                "id": doc.get("file"),
                "title": doc.get("title") or doc.get("file"),
                "score": round(score, 3),
            })
        for row in self.conflicts:
            blob = " ".join([
                row.get("topic") or "",
                row.get("description") or "",
                row.get("evidence_a") or "",
                row.get("evidence_b") or "",
                row.get("agent_guidance") or "",
            ])
            score = self._overlap(qtoks, blob)
            if score <= 0:
                continue
            hits.append({
                "kind": "conflict",
                "id": row.get("id"),
                "title": row.get("topic"),
                "score": round(min(1.0, score + 0.15), 3),
            })
        hits.sort(key=lambda h: h["score"], reverse=True)
        return hits[:limit]

    def retrieve(self, query: str, top_k: int = 12) -> list[dict]:
        self.last_hits = self.graph_hits(query)
        boosted = {h["id"] for h in self.last_hits if h["kind"] == "document"}
        base = self.tfidf.retrieve(query, top_k=max(top_k * 2, 16)) if self.tfidf else []
        results = []
        for row in base:
            score = float(row["score"])
            if row.get("source") in boosted:
                score = min(1.0, score * 1.35 + 0.05)
            results.append({**row, "score": round(score, 4)})
        qtoks = tokens(query)
        for row in self.conflicts:
            blob = " ".join([
                row.get("topic") or "",
                row.get("description") or "",
                row.get("agent_guidance") or "",
            ])
            score = self._overlap(qtoks, blob)
            if score < 0.18:
                continue
            cid = f"graph:{row.get('id')}"
            results.append({
                "chunk_id": cid,
                "source": "master_corpus_index.json",
                "text": self.graph_passages[cid],
                "score": round(min(0.99, 0.68 + score), 4),
            })
        results.sort(key=lambda r: r["score"], reverse=True)
        seen: set[str] = set()
        uniq: list[dict] = []
        for row in results:
            key = row["chunk_id"]
            if key in seen:
                continue
            seen.add(key)
            uniq.append(row)
            if len(uniq) >= top_k:
                break
        self.last_chunks = uniq
        return validate_retrieval_results(uniq, query=query)
