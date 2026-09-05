"""HTTP API for the chat console. User question → graph query → security agent.

Run from the repo root:
    .venv/bin/python -m uvicorn server:app --host 127.0.0.1 --port 8000
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import unquote

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent
AGENT_DIR = ROOT / "security_agent"
CORPUS_DIR = ROOT / "corpus_text"
INDEX_PATH = CORPUS_DIR / "00_INDEX" / "master_corpus_index.json"

load_dotenv(ROOT / ".env")
sys.path.insert(0, str(AGENT_DIR))

from agent_loop import process_question  # noqa: E402
from graph_query import GraphQueryRetriever, tokens  # noqa: E402

SKIP_DIRS = {"00_INDEX", "01_SAMPLE_VENDOR_QUESTIONNAIRE"}
TARGET_CHARS = 900


def infer_source_type(name: str) -> str:
    n = name.lower()
    if "policy" in n or "risk" in n or "02_company" in n:
        return "policy"
    if "infra" in n or "05_infra" in n or "network" in n or "asset" in n:
        return "infra"
    if "message" in n or "slack" in n or "email" in n:
        return "message"
    if "employee" in n or "hr" in n or "employment" in n:
        return "employee"
    return "doc"


def chunk_markdown(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").split("\n")
    chunks: list[dict] = []
    buf: list[str] = []
    start = 0
    filename = path.name
    source_type = infer_source_type(str(path))

    def emit(end: int) -> None:
        nonlocal start, buf
        text = "\n".join(buf).strip()
        buf = []
        if len(text) < 80:
            start = end
            return
        chunks.append({
            "source": filename,
            "chunk_id": f"{filename}:L{start + 1}-L{end}",
            "text": text,
            "source_type": source_type,
        })
        start = end

    for i, line in enumerate(lines):
        heading_break = line.startswith("#") and buf and len("\n".join(buf)) >= 200
        if heading_break:
            emit(i)
        buf.append(line)
        if len("\n".join(buf)) >= TARGET_CHARS:
            emit(i + 1)
    emit(len(lines))
    return chunks


def load_corpus_chunks() -> list[dict]:
    canned = AGENT_DIR / "chunks.json"
    if canned.exists():
        return json.loads(canned.read_text(encoding="utf-8"))
    records: list[dict] = []
    if CORPUS_DIR.exists():
        for path in sorted(CORPUS_DIR.rglob("*")):
            if path.suffix.lower() not in {".md", ".txt"}:
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.name.startswith(".") or path.name == "MASTER_CORPUS_INDEX.md":
                continue
            records.extend(chunk_markdown(path))
    return records


def load_index() -> dict:
    if INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return {}


CHUNKS = load_corpus_chunks()
INDEX = load_index()
RETRIEVER = GraphQueryRetriever(INDEX, CHUNKS) if CHUNKS else None

app = FastAPI(title="SENTINEL chat agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class HistoryTurn(BaseModel):
    role: str
    text: str


class ChatBody(BaseModel):
    message: str
    history: list[HistoryTurn] = []


def compose_question(message: str, history: list[HistoryTurn]) -> str:
    prior = [t for t in history[-6:] if t.text.strip()]
    if not prior:
        return message
    lines = ["Prior conversation:"]
    for turn in prior:
        who = "User" if turn.role == "user" else "Analyst"
        lines.append(f"{who}: {turn.text.strip()}")
    lines.append("")
    lines.append(f"Current question:\n{message}")
    return "\n".join(lines)


INTENT_MAP = [
    (("mfa", "otp", "2fa", "authentication", "authenticator"), "MFA"),
    (("encrypt", "aes", "tls", "cryptograph"), "Encryption"),
    (("backup", "disaster", "recovery", "bcp"), "Backups"),
    (("vulnerab", "scan", "vapt", "pentest"), "VulnScans"),
    (("offboard", "deprovision", "revoke"), "Offboarding"),
    (("access", "production", "privilege", "iam"), "Access"),
    (("w-9", "w9", "legal", "entity", "solsphere"), "LegalEntity"),
    (("siem", "logging", "cloudwatch"), "Logging"),
]


def parse_intent(message: str) -> str:
    q = message.lower()
    for keys, label in INTENT_MAP:
        if any(k in q for k in keys):
            return label
    toks = tokens(message)
    return toks[0].upper() if toks else "Query"


def node_type_of(name: str) -> str:
    st = infer_source_type(name)
    return st if st in {"policy", "infra", "doc", "message", "employee"} else "doc"


def build_graph_trace(message: str, chunks: list[dict], hits: list[dict], result: dict | None) -> dict:
    intent = parse_intent(message)
    best = float(hits[0]["score"]) if hits else (float(chunks[0]["score"]) if chunks else 0.5)
    logs = [f"parsed intent → control:{intent}", f"matched node Control:{intent} (confidence {best:.2f})"]
    nodes: list[dict] = [
        {"id": "q", "label": message[:56], "type": "query", "layer": 0},
        {"id": "c-intent", "label": f"Control: {intent}", "type": "control", "layer": 1},
    ]
    edges = [{"from": "q", "to": "c-intent", "rel": "INTENT"}]

    entities: list[tuple[str, dict, str]] = []
    for i, hit in enumerate(hits[:4]):
        nid = f"e{i}"
        if hit.get("kind") == "conflict":
            ntype = "control"
            label = f"Conflict: {hit.get('title') or hit.get('id')}"
        else:
            ntype = node_type_of(str(hit.get("id") or ""))
            label = str(hit.get("title") or hit.get("id") or "node")
        nodes.append({"id": nid, "label": label[:44], "type": ntype, "layer": 1})
        rel = "FLAGGED_IN" if hit.get("kind") == "conflict" else "ENFORCED_BY"
        edges.append({"from": "c-intent", "to": nid, "rel": rel})
        entities.append((nid, hit, ntype))

    logs.append(f"traversing ENFORCED_BY → {len(entities)} nodes")
    for _nid, hit, _nt in entities:
        logs.append(f"  → {hit.get('title') or hit.get('id')}")

    sources: list[tuple[str, dict, str]] = []
    seen: set[str] = set()
    for chunk in chunks[:6]:
        cid = chunk.get("chunk_id") or chunk.get("source") or ""
        if not cid or cid in seen:
            continue
        seen.add(cid)
        sid = f"s{len(sources)}"
        src = chunk.get("source") or cid
        ntype = "control" if str(cid).startswith("graph:") else node_type_of(src)
        if ntype == "control":
            ntype = "doc"
        label = cid if len(cid) <= 40 else src
        nodes.append({"id": sid, "label": label, "type": ntype, "layer": 2})
        sources.append((sid, chunk, ntype))

    logs.append(f"traversing EVIDENCED_IN → {len(sources)} source chunks")
    for sid, chunk, ntype in sources:
        logs.append(f"  → {chunk.get('chunk_id')}  [{ntype}]")
        src = chunk.get("source") or ""
        linked = False
        for nid, hit, _nt in entities:
            hid = str(hit.get("id") or "")
            if hid and hid in src:
                edges.append({"from": nid, "to": sid, "rel": "EVIDENCED_IN"})
                linked = True
                break
            if hit.get("kind") == "conflict" and str(chunk.get("chunk_id", "")).startswith("graph:"):
                edges.append({"from": nid, "to": sid, "rel": "CONTRADICTED_BY"})
                linked = True
                break
        if not linked:
            rel = "CONTRADICTED_BY" if ntype in {"message", "infra"} and any(h.get("kind") == "conflict" for h in hits) else "EVIDENCED_IN"
            edges.append({"from": "c-intent", "to": sid, "rel": rel})

    status = (result or {}).get("final_status")
    if status == "conflict" or any(h.get("kind") == "conflict" for h in hits):
        logs.append("conflict check: policy(5) vs infra/message → DISAGREEMENT")
        verdict = "CONFLICT"
    elif status in {"ask_user", "insufficient"}:
        logs.append("conflict check: insufficient overlap → UNKNOWN")
        verdict = "UNKNOWN"
    elif result is None:
        logs.append("guardrails pending…")
        verdict = "PENDING"
    else:
        logs.append("conflict check: sources consistent")
        verdict = "VERIFIED"
    conf_n = (result or {}).get("confidence")
    try:
        c = float(conf_n)
        conf = "high" if c >= 0.7 else "medium" if c >= 0.4 else "low"
    except (TypeError, ValueError):
        conf = "medium"
    if verdict != "PENDING":
        logs.append(f"verdict → {verdict} · evidence {len(sources)} · confidence {conf}")
    return {"logs": logs, "nodes": nodes, "edges": edges}


def format_reply(result: dict) -> str:
    status = result.get("final_status")
    answer = (result.get("answer") or "").strip()
    if status == "answered":
        return answer or "The documents support an answer, but no wording was produced."
    if status == "conflict":
        note = (result.get("conflict_explanation") or "Company sources disagree on this point.").strip()
        if answer:
            return f"{answer}\n\n{note}\n\nWhich of those is current?"
        return f"{note}\n\nWhich of those is current?"
    note = (result.get("guardrail_note") or "The documents do not answer this clearly.").strip()
    return f"{note} If you know the current practice, tell me and I can use that."


@app.get("/api/corpus")
def corpus_status():
    docs = {}
    for chunk in CHUNKS:
        docs.setdefault(chunk["source"], infer_source_type(chunk.get("source", "")))
    return {
        "ready": bool(CHUNKS),
        "documentCount": len(docs),
        "chunkCount": len(CHUNKS),
        "graphNodes": len(INDEX.get("documents") or []),
        "conflicts": len(INDEX.get("contradictions_and_investigation_playbook") or []),
        "dir": str(CORPUS_DIR),
    }


@app.post("/api/chat")
def chat(body: ChatBody):
    message = (body.message or "").strip()
    if not message:
        raise HTTPException(400, "message required")
    if RETRIEVER is None:
        raise HTTPException(503, "No corpus loaded")

    question = compose_question(message, body.history)
    result = process_question(question, RETRIEVER, top_k=12)
    citations = []
    for cite in result.get("citations") or []:
        cid = cite.get("chunk_id") or cite.get("source") or ""
        if not cid:
            continue
        citations.append({
            "id": cid,
            "source": cite.get("source") or cid.split(":")[0],
            "quote": cite.get("quote") or "",
            "sourceType": infer_source_type(cite.get("source") or cid),
        })
    return {
        "reply": format_reply(result),
        "status": result.get("final_status") or "ask_user",
        "confidence": result.get("confidence"),
        "citations": citations,
        "graphHits": RETRIEVER.last_hits,
        "graphTrace": build_graph_trace(message, RETRIEVER.last_chunks, RETRIEVER.last_hits, result),
        "usedLiveLlm": bool(result.get("used_live_llm")),
    }


@app.post("/api/trace")
def trace(body: ChatBody):
    message = (body.message or "").strip()
    if not message:
        raise HTTPException(400, "message required")
    if RETRIEVER is None:
        raise HTTPException(503, "No corpus loaded")
    chunks = RETRIEVER.retrieve(message, top_k=12)
    return {
        "graphTrace": build_graph_trace(message, chunks, RETRIEVER.last_hits, None),
    }


@app.get("/api/evidence/{evidence_id:path}")
def evidence(evidence_id: str):
    wanted = unquote(evidence_id)
    if RETRIEVER and wanted in RETRIEVER.graph_passages:
        return {
            "id": wanted,
            "filename": "master_corpus_index.json",
            "sourceType": "doc",
            "text": RETRIEVER.graph_passages[wanted],
        }
    for chunk in CHUNKS:
        if chunk["chunk_id"] == wanted or chunk["source"] == wanted:
            return {
                "id": chunk["chunk_id"],
                "filename": chunk["source"],
                "sourceType": infer_source_type(chunk.get("source_type") or chunk["source"]),
                "text": chunk["text"],
            }
    raise HTTPException(404, "Evidence not found")
