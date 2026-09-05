"""
Eval runner: runs the agent's process_question() against every case
in eval_set.py, compares the FINAL STATUS (after guardrails) to the
expected_status, and reports a simple pass/fail scorecard.

This is the actual answer to "how will you write the evals" -
it's just this file, made bigger over time as you verify more
of the 66 questions by hand.
"""
from agent_loop import process_question, load_chunks
from retrieve_graph import GraphTreeRetriever as Retriever
from eval_set import EVAL_CASES

def run_evals():
    chunks = load_chunks()
    retriever = Retriever(chunks)

    results = []
    for case in EVAL_CASES:
        result = process_question(case["question"], retriever, top_k=12)
        passed = result["final_status"] == case["expected_status"]
        results.append({
            "id": case["id"],
            "question": case["question"],
            "expected": case["expected_status"],
            "actual": result["final_status"],
            "passed": passed,
            "guardrail_note": result["guardrail_note"],
        })

    print("=" * 70)
    print("EVAL RESULTS")
    print("=" * 70)
    passed_count = 0
    for r in results:
        status_icon = "PASS" if r["passed"] else "FAIL"
        print(f"[{status_icon}] {r['id']}: expected={r['expected']}  actual={r['actual']}")
        if not r["passed"]:
            print(f"        -> {r['guardrail_note']}")
        if r["passed"]:
            passed_count += 1
    print()
    print(f"Score: {passed_count}/{len(results)} ({100*passed_count//len(results)}%)")
    return results

if __name__ == "__main__":
    run_evals()
