"""
Core agent decision loop + guardrails for the Regodit AI Security Analyst.

Owns: given a question + retrieved evidence chunks, decide one of:
  - ANSWERED   : confident answer, backed by cited evidence
  - CONFLICT   : evidence disagrees across sources, needs human resolution
  - ASK_USER   : no sufficient evidence found, needs human input
  - FOLLOW_UP  : user's prior answer was vague, needs a specific follow-up

GUARDRAIL PRINCIPLE (the "never fabricate" rule):
  The LLM's raw output is NEVER trusted blindly. Every response is
  checked by enforce_guardrails() before it's allowed to become a
  final answer. This is the layer that makes the system defensible
  to judges - the LLM proposes, the guardrail layer disposes.

LIVE MODE: call_llm() now calls the real Anthropic API (needs
ANTHROPIC_API_KEY in a .env file next to this script). If the key is
missing, or the API call fails for any reason, we fall back to
simulate_llm_reasoning() so a demo never hard-crashes on a bad network
or a rate limit - it just becomes visibly less "smart", not broken.
"""
import json
import os
import re

from dotenv import load_dotenv
from retrieve_v2 import load_chunks, Retriever

load_dotenv()  # reads .env in this folder, sets ANTHROPIC_API_KEY etc.

_client = None


def _get_client():
    """Lazily create the Anthropic client so importing this module never
    fails just because a key isn't set yet (e.g. running eval_set.py
    standalone before the .env exists)."""
    global _client
    if _client is None:
        import anthropic
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY not set. Create a .env file next to this "
                "script with ANTHROPIC_API_KEY=sk-ant-... "
            )
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


MODEL_NAME = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")

# ---- 1. Prompt template (use this verbatim at the hackathon) ----

DECISION_PROMPT_TEMPLATE = """You are a security compliance analyst completing a vendor security questionnaire.
You must NEVER fabricate an answer. Only use the evidence provided below.

QUESTION:
{question}

EVIDENCE (retrieved from company documents):
{evidence_block}

Decide one of the following, and respond ONLY as JSON:
1. "answered" - the evidence clearly and consistently answers the question
2. "conflict" - two or more evidence pieces disagree with each other
3. "insufficient" - the evidence does not address this question at all

Respond in this exact JSON shape, and nothing else - no markdown fences, no commentary:
{{
  "status": "answered" | "conflict" | "insufficient",
  "answer": "<your answer in plain language, or null>",
  "confidence": <0.0 to 1.0>,
  "citations": [{{"source": "<filename>", "chunk_id": "<id>", "quote": "<short supporting quote>"}}],
  "conflict_explanation": "<if status is conflict, explain the disagreement, else null>"
}}
"""

def build_evidence_block(chunks):
    lines = []
    for c in chunks:
        lines.append(f"- [{c['chunk_id']}] ({c['source']}): {c['text']}")
    return "\n".join(lines)


def extract_json(raw_text):
    """
    Models sometimes wrap JSON in ```json ... ``` fences, or add a
    stray sentence before/after it despite instructions. Strip fences
    first, then fall back to grabbing the outermost {...} block.
    """
    text = raw_text.strip()
    fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1)
    else:
        brace_match = re.search(r"\{.*\}", text, re.DOTALL)
        if brace_match:
            text = brace_match.group(0)
    return json.loads(text)

# ---- 2. LLM call (LIVE - real Anthropic API) ----

def call_llm(prompt):
    client = _get_client()
    resp = client.messages.create(
        model=MODEL_NAME,
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def simulate_llm_reasoning(question, chunks):
    """
    Transparent MOCK reasoning - kept as the offline/no-key/API-failure
    fallback so a flaky connection or a missing key at demo time doesn't
    take the whole pipeline down. Not meant to be smart.
    """
    texts = " ".join(c["text"].lower() for c in chunks)

    requires_lang = any(w in texts for w in ["required across", "is enforced", "is required"])
    recommends_lang = any(w in texts for w in ["recommend", "enhance security by implementing", "encourage or require"])

    if requires_lang and recommends_lang:
        return {
            "status": "conflict",
            "answer": None,
            "confidence": 0.4,
            "citations": [
                {"source": c["source"], "chunk_id": c["chunk_id"], "quote": c["text"][:100]}
                for c in chunks[:3]
            ],
            "conflict_explanation": (
                "Company policy states MFA is enforced/required across all core systems, "
                "but a penetration test report recommends implementing MFA on a "
                "customer-facing application - suggesting it may not actually be enforced there."
            ),
        }

    if not chunks or max(c["score"] for c in chunks) < 0.15:
        return {
            "status": "insufficient",
            "answer": None,
            "confidence": 0.1,
            "citations": [],
            "conflict_explanation": None,
        }

    top = chunks[0]
    return {
        "status": "answered",
        "answer": f"Based on company documentation: {top['text'][:200]}",
        "confidence": min(0.9, top["score"] * 3),
        "citations": [{"source": top["source"], "chunk_id": top["chunk_id"], "quote": top["text"][:150]}],
        "conflict_explanation": None,
    }


def get_llm_decision(question, chunks, evidence_block, prompt):
    """
    Try the real API first; fall back to the deterministic mock on any
    failure (missing key, network error, bad JSON back) so the demo
    keeps running. `used_live_llm` is stamped on the result so you can
    tell judges honestly whether a given answer came from the real
    model or the offline fallback.
    """
    try:
        raw = call_llm(prompt)
        parsed = extract_json(raw)
        parsed.setdefault("citations", [])
        parsed.setdefault("conflict_explanation", None)
        parsed["used_live_llm"] = True
        return parsed
    except Exception as e:
        fallback = simulate_llm_reasoning(question, chunks)
        fallback["used_live_llm"] = False
        fallback["llm_error"] = str(e)
        return fallback

# ---- 3. Guardrail enforcement (THE key deliverable) ----

CONFIDENCE_FLOOR = 0.5  # below this, force human review even if LLM says "answered"

def enforce_guardrails(llm_output, question):
    """
    Never trust the LLM's self-report blindly. This function is the
    actual guardrail layer - it can OVERRIDE the LLM's proposed status.
    """
    status = llm_output["status"]
    citations = llm_output.get("citations", [])
    confidence = llm_output.get("confidence", 0)

    if status == "answered" and not citations:
        return _override(llm_output, "ask_user", "No evidence citation provided - refusing to auto-answer.")

    if status == "answered" and confidence < CONFIDENCE_FLOOR:
        return _override(llm_output, "ask_user", f"Confidence {confidence} below floor {CONFIDENCE_FLOOR} - escalating to human.")

    if status == "conflict":
        return _override(llm_output, "conflict", "Conflicting evidence detected - human resolution required.", keep_explanation=True)

    if status == "insufficient":
        return _override(llm_output, "ask_user", "No sufficient evidence found in company documents.")

    return {**llm_output, "final_status": "answered", "guardrail_note": "Passed all checks."}

def _override(llm_output, final_status, note, keep_explanation=False):
    return {
        **llm_output,
        "final_status": final_status,
        "guardrail_note": note,
    }

# ---- 4. Orchestration: the full loop for one question ----

def process_question(question, retriever, top_k=12):
    chunks = retriever.retrieve(question, top_k=top_k)
    evidence_block = build_evidence_block(chunks) if chunks else "(no relevant evidence found)"
    prompt = DECISION_PROMPT_TEMPLATE.format(question=question, evidence_block=evidence_block)

    raw_output = get_llm_decision(question, chunks, evidence_block, prompt)

    result = enforce_guardrails(raw_output, question)
    result["question"] = question
    result["prompt_used"] = prompt  # for debugging/demo transparency
    return result

if __name__ == "__main__":
    chunks = load_chunks()
    retriever = Retriever(chunks)

    test_questions = [
        "Does your organization have a formal Information Security Program established?",
        "Does your organization require replay-resistant authentication mechanisms such as OTP or MFA?",
        "Will you be using any contractors or sub-contractors to complete the engagement with Regodit?",
    ]

    for q in test_questions:
        result = process_question(q, retriever)
        print("=" * 80)
        print("Q:", q)
        print("FINAL STATUS:", result["final_status"], "| LIVE LLM:", result.get("used_live_llm"))
        print("GUARDRAIL NOTE:", result["guardrail_note"])
        if result.get("answer"):
            print("ANSWER:", result["answer"])
        if result.get("conflict_explanation"):
            print("CONFLICT:", result["conflict_explanation"])
        print("CITATIONS:", json.dumps(result.get("citations", []), indent=2))
        print()
