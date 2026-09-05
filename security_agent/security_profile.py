"""
Persistent state store for the Regodit AI Security Analyst.

Owns the "remember everything, no duplicate questions, corrections
update in place" behavior that conversation_loop.py depends on:

  - already_answered(question_id)  -> has this question already been
                                       resolved (verified or confirmed)?
  - get_record(question_id)        -> the current stored answer, if any
  - upsert_record(...)             -> create a new record, OR correct an
                                       existing one in place (never a
                                       duplicate second entry for the
                                       same question_id)
  - summary_report()               -> the full profile for the demo/UI

STATUS VALUES (match what conversation_loop.py passes in):
  - "verified_from_documents" : answered straight from company docs
  - "confirmed_by_user"       : a human supplied or resolved the answer
    (covers both the "ask_user" path and the "conflict, human resolves"
    path - conversation_loop.py distinguishes those via conflict_explanation)

PERSISTENCE:
  Backed by a JSON file (security_profile.json, next to this module by
  default) so the profile survives across process restarts - this is
  the actual "persistent memory" the README promises. Every write goes
  through save() immediately; there's no separate flush step to forget.

  For the hackathon demo this being a plain JSON file is a feature, not
  a shortcut: judges can literally open it and see the running state.
"""
import json
import os
import threading
from datetime import datetime, timezone

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "security_profile.json")

# Statuses that count as "resolved" for already_answered() - i.e. the
# question should be SKIPPED on a re-run, not re-asked.
RESOLVED_STATUSES = {"verified_from_documents", "confirmed_by_user"}

_lock = threading.Lock()


def _now():
    return datetime.now(timezone.utc).isoformat()


def _empty_profile():
    return {"questions": {}, "meta": {"created_at": _now()}}


def load_profile(path=DEFAULT_PATH):
    if not os.path.exists(path):
        return _empty_profile()
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            # corrupt/empty file - don't crash the demo, start fresh
            return _empty_profile()
    data.setdefault("questions", {})
    data.setdefault("meta", {"created_at": _now()})
    return data


def save_profile(profile, path=DEFAULT_PATH):
    tmp_path = path + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(profile, f, indent=2)
    os.replace(tmp_path, path)  # atomic on same filesystem - no half-written file


# Module-level cache so repeated calls within one run don't re-read the
# file every time; still reloaded fresh at import and after every save.
_profile = load_profile()


def already_answered(question_id):
    """True if this question has a resolved (non-duplicate-worthy) record."""
    record = _profile["questions"].get(question_id)
    return bool(record) and record["status"] in RESOLVED_STATUSES


def get_record(question_id):
    return _profile["questions"].get(question_id)


def upsert_record(question_id, question_text, status, answer=None, confidence=None,
                   citations=None, conflict_explanation=None, history=None):
    """
    Create a new record for question_id, or CORRECT the existing one in
    place if it already exists - never a second entry for the same
    question_id. Returns the stored record.
    """
    with _lock:
        existing = _profile["questions"].get(question_id)

        record = {
            "question_id": question_id,
            "question_text": question_text,
            "status": status,
            "answer": answer,
            "confidence": confidence,
            "citations": citations or [],
            "conflict_explanation": conflict_explanation,
            "history": history or [],
            "updated_at": _now(),
        }

        if existing:
            # Correction, not a duplicate: keep the original first-seen
            # timestamp and bump a correction counter so the demo can
            # show "this was corrected N times".
            record["created_at"] = existing.get("created_at", _now())
            record["correction_count"] = existing.get("correction_count", 0) + (
                1 if existing.get("answer") != answer or existing.get("status") != status else 0
            )
            record["prior_answer"] = existing.get("answer") if existing.get("answer") != answer else existing.get("prior_answer")
        else:
            record["created_at"] = record["updated_at"]
            record["correction_count"] = 0
            record["prior_answer"] = None

        _profile["questions"][question_id] = record
        save_profile(_profile)
        return record


def summary_report():
    """Full profile snapshot - handy for the demo / judge-facing UI."""
    questions = _profile["questions"]
    by_status = {}
    for record in questions.values():
        by_status.setdefault(record["status"], 0)
        by_status[record["status"]] += 1

    return {
        "total_questions": len(questions),
        "by_status": by_status,
        "corrected_count": sum(1 for r in questions.values() if r["correction_count"] > 0),
        "questions": questions,
    }


def reset_profile(path=DEFAULT_PATH):
    """Wipe the stored profile. Only for tests/demos - never called from
    the main conversation flow."""
    global _profile
    _profile = _empty_profile()
    save_profile(_profile, path)


if __name__ == "__main__":
    # Standalone self-test - doesn't need chunks.json/docx files, so it
    # runs today even before the real hackathon documents land.
    reset_profile()

    print("=== 1. New question, not yet answered ===")
    print("already_answered(Q1):", already_answered("Q1"))

    print("\n=== 2. First answer recorded ===")
    r1 = upsert_record(
        "Q1", "Does your organization have a formal Information Security Program established?",
        "verified_from_documents", answer="Yes, per the Information Security Policy.", confidence=0.9,
        citations=[{"source": "info_security_policy.docx", "chunk_id": "x::0", "quote": "..."}],
    )
    print(json.dumps(r1, indent=2))

    print("\n=== 3. Re-run same question -> should be skipped ===")
    print("already_answered(Q1):", already_answered("Q1"))
    print("get_record(Q1):", get_record("Q1")["status"])

    print("\n=== 4. Correction: user overrides the stored answer ===")
    r2 = upsert_record(
        "Q1", "Does your organization have a formal Information Security Program established?",
        "confirmed_by_user", answer="Yes, and it was re-certified last quarter.", confidence=1.0,
    )
    print("correction_count:", r2["correction_count"], "| prior_answer:", r2["prior_answer"])

    print("\n=== 5. Summary report ===")
    print(json.dumps(summary_report(), indent=2))

    print(f"\n(profile persisted to {DEFAULT_PATH} - delete it or call reset_profile() to clear)")
