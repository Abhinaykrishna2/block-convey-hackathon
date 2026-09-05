"""
Multi-turn conversation loop - handles the full lifecycle of ONE
questionnaire item, including the "vague answer -> follow-up" case
(Gap 1 from the diagram review) that single-shot process_question()
doesn't cover on its own.

Flow for one question:
  1. Check security_profile - already answered? -> skip, done.
  2. Run process_question() (retrieval + LLM + guardrails).
  3. If final_status == "answered" -> save as verified_from_documents, done.
  4. If final_status == "conflict" -> surface conflict to human, get their
     resolution, save as confirmed_by_user with conflict noted, done.
  5. If final_status == "ask_user" -> ask human directly.
       5a. Evaluate their reply: complete, or vague?
       5b. If vague -> ask a specific follow-up (capped at MAX_FOLLOWUPS
           to avoid an infinite loop - a guardrail in its own right).
       5c. Once complete -> save as confirmed_by_user, done.

LIVE MODE: evaluate_user_reply() now calls the real Anthropic API (same
.env / ANTHROPIC_API_KEY as agent_loop.py). Falls back to the heuristic
mock on any failure so a flaky connection never breaks the demo.
"""
import json
try:
    from agent_loop import process_question, load_chunks, call_llm, extract_json, MODEL_NAME
    from retrieve_graph import GraphTreeRetriever as Retriever
    import security_profile as profile_store
except ImportError:
    from security_agent.agent_loop import process_question, load_chunks, call_llm, extract_json, MODEL_NAME
    from security_agent.retrieve_graph import GraphTreeRetriever as Retriever
    import security_agent.security_profile as profile_store

MAX_FOLLOWUPS = 3

EVALUATE_REPLY_PROMPT_TEMPLATE = """You are checking whether a human's answer to a security
questionnaire question is specific enough to record, or too vague and needs a follow-up.

ORIGINAL QUESTION:
{question}

CONVERSATION SO FAR:
{history_block}

LATEST REPLY:
{reply}

Respond ONLY as JSON, no markdown fences, no commentary:
{{
  "complete": true | false,
  "follow_up_question": "<one specific follow-up question, or null if complete>"
}}
"""


def _format_history(history):
    if not history:
        return "(none yet)"
    lines = []
    for turn in history:
        if "asked" in turn:
            lines.append(f"asked: {turn['asked']}\nreplied: {turn['replied']}")
    return "\n".join(lines) if lines else "(none yet)"


def _evaluate_user_reply_mock(question, reply, history):
    """
    MOCK fallback - simple heuristic: very short replies (<15 chars,
    roughly "yes"/"no"/one word) on a question that implies more detail
    is expected count as vague. Used when the real API call fails.
    """
    reply_clean = reply.strip().lower()
    is_short = len(reply_clean) < 15
    implies_detail = any(w in question.lower() for w in ["how", "describe", "process", "frequency", "do you"])

    if is_short and implies_detail and len(history) < MAX_FOLLOWUPS:
        return {
            "complete": False,
            "follow_up_question": "Can you give more detail on that? (e.g. how often, or whether it's automated)",
        }
    return {"complete": True, "follow_up_question": None}


def evaluate_user_reply(question, reply, history):
    """
    Decide if a human's reply is COMPLETE or too VAGUE to record yet.
    Tries the real LLM first; falls back to the heuristic mock on any
    failure (missing key, network error, bad JSON) so the demo keeps
    running end-to-end regardless.
    """
    if len(history) >= MAX_FOLLOWUPS:
        # guardrail: never loop forever even if the model keeps saying "vague"
        return {"complete": True, "follow_up_question": None}

    prompt = EVALUATE_REPLY_PROMPT_TEMPLATE.format(
        question=question, history_block=_format_history(history), reply=reply
    )
    try:
        # call_llm() already returns a parsed dict (it does its own JSON
        # extraction internally) - don't run extract_json() on it again,
        # that would call .strip() on a dict and raise AttributeError.
        parsed = call_llm(prompt)
        return {
            "complete": bool(parsed.get("complete", True)),
            "follow_up_question": parsed.get("follow_up_question"),
        }
    except Exception:
        return _evaluate_user_reply_mock(question, reply, history)


def handle_question(question_id, question_text, retriever, simulated_user_replies=None):
    """
    simulated_user_replies: for offline testing only - a list of canned
    replies to feed in sequence instead of a real human typing live.
    """
    simulated_user_replies = list(simulated_user_replies or [])

    if profile_store.already_answered(question_id):
        record = profile_store.get_record(question_id)
        print(f"[{question_id}] Already answered - skipping. ({record['status']})")
        return record

    result = process_question(question_text, retriever, top_k=12)
    status = result["final_status"]

    if status == "answered":
        record = profile_store.upsert_record(
            question_id, question_text, "verified_from_documents",
            answer=result.get("answer"), confidence=result.get("confidence"),
            citations=result.get("citations"),
        )
        print(f"[{question_id}] VERIFIED FROM DOCUMENTS: {result.get('answer')}")
        return record

    if status == "conflict":
        # In a real UI this pauses and shows the conflict to a human.
        # Here, we take the first simulated reply as their resolution.
        resolution = simulated_user_replies.pop(0) if simulated_user_replies else "(no resolution provided)"
        record = profile_store.upsert_record(
            question_id, question_text, "confirmed_by_user",
            answer=resolution, confidence=1.0,
            citations=result.get("citations"),
            conflict_explanation=result.get("conflict_explanation"),
            history=[{"conflict_explanation": result.get("conflict_explanation")}, {"human_resolution": resolution}],
        )
        print(f"[{question_id}] CONFLICT RESOLVED BY HUMAN: {resolution}")
        print(f"           (was: {result.get('conflict_explanation')})")
        return record

    if status == "ask_user":
        history = []
        current_question = question_text
        while True:
            reply = simulated_user_replies.pop(0) if simulated_user_replies else "(no reply provided)"
            history.append({"asked": current_question, "replied": reply})
            evaluation = evaluate_user_reply(question_text, reply, history)
            if evaluation["complete"] or not simulated_user_replies:
                record = profile_store.upsert_record(
                    question_id, question_text, "confirmed_by_user",
                    answer=reply, confidence=1.0, history=history,
                )
                print(f"[{question_id}] CONFIRMED BY USER: {reply}")
                if history and len(history) > 1:
                    print(f"           (after {len(history)-1} follow-up(s))")
                return record
            current_question = evaluation["follow_up_question"]
            print(f"[{question_id}] Reply too vague ('{reply}') -> follow-up: {current_question}")

if __name__ == "__main__":
    chunks = load_chunks()
    retriever = Retriever(chunks)

    print("=== Case 1: clean doc-answered question ===")
    handle_question("Q65", "Does your organization conduct penetration testing at least annually?", retriever)

    print("\n=== Case 2: conflict, human resolves it ===")
    handle_question(
        "Q60", "Does your organization require replay-resistant authentication mechanisms such as OTP or MFA?",
        retriever,
        simulated_user_replies=["MFA is enforced on all internal/admin systems; the customer-facing web app flagged in the pentest is being remediated this quarter."]
    )

    print("\n=== Case 3: ask_user with a vague reply needing follow-up ===")
    handle_question(
        "Q6", "Will you be using any contractors or sub-contractors to complete the engagement with Regodit?",
        retriever,
        simulated_user_replies=["yes", "Two infra subcontractors, both under signed NDAs with security clauses."]
    )

    print("\n=== Case 4: re-running Q65 should now be skipped (memory works) ===")
    handle_question("Q65", "Does your organization conduct penetration testing at least annually?", retriever)

    print("\n=== Final Security Profile Summary ===")
    import json
    print(json.dumps(profile_store.summary_report(), indent=2))
