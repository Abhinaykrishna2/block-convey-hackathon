"""
Eval set for the Regodit AI Security Analyst agent.

Each entry is a REAL question from the 66-item matrix, with a
GROUND TRUTH label that Mathan verified by hand-reading the actual
source documents. Running agent_loop.process_question() against
these and comparing to expected_status is the eval.

This is intentionally small (5 cases) to start - add more from the
other 61 questions as you verify them by hand. Quality over
quantity: a handful of hand-checked cases you trust completely
beats 66 guesses.
"""

EVAL_CASES = [
    {
        "id": "Q1",
        "question": "Does your organization have a formal Information Security Program established?",
        "expected_status": "answered",
        "expected_answer_gist": "Yes - evidenced by the documented Information Security Policy (defines scope, roles, responsibilities across the org).",
        "ground_truth_source": "Regodit_information_security_policy_v1.0.docx",
        "notes": "Real risk: naive retrieval may grab an unrelated HR training clause instead of this policy's own scope statement. Good test of whether reasoning picks the RIGHT evidence, not just top-ranked.",
    },
    {
        "id": "Q60",
        "question": "Does your organization require replay-resistant authentication mechanisms such as OTP or MFA?",
        "expected_status": "conflict",
        "expected_answer_gist": None,
        "ground_truth_source": "Regodit_password_and_secrets_policy_v1.0.docx (says MFA required) vs VAPT Report 01.docx (recommends adding MFA to a customer-facing app)",
        "notes": "THE key conflict case. Requires wide enough retrieval (top_k) to see both sides - see our earlier top_k=6 vs top_k=12 finding.",
    },
    {
        "id": "Q65",
        "question": "Does your organization conduct penetration testing at least annually?",
        "expected_status": "answered",
        "expected_answer_gist": "Yes - stated in Info Security Policy and Vulnerability & Patch Management Policy, AND backed by an actual VAPT report on file (dated Oct 2025).",
        "ground_truth_source": "Regodit_information_security_policy_v1.0.docx, Regodit_vulnerability_and_patch_management_policy_v1.0.docx, VAPT Report 01.docx",
        "notes": "Strong positive case - policy claim AND real evidence agree. Should be high confidence.",
    },
    {
        "id": "Q66",
        "question": "Have the findings from the most recent test been remediated?",
        "expected_status": "answered",
        "expected_answer_gist": "No - all 20 findings in the VAPT report show status 'Open'. None remediated.",
        "ground_truth_source": "VAPT Report 01.docx (findings table, 20/20 rows = Open)",
        "notes": "Requires synthesizing across an entire table, not matching one sentence. Good test of whether the agent actually reads all the evidence instead of stopping at the first match.",
    },
    {
        "id": "Q6",
        "question": "Will you be using any contractors or sub-contractors to complete the engagement with Regodit?",
        "expected_status": "ask_user",
        "expected_answer_gist": None,
        "ground_truth_source": None,
        "notes": "This is a fact about THIS specific engagement/vendor relationship, not something Regodit's own internal policies would state. Correct behavior is to ask, not guess.",
    },
]

if __name__ == "__main__":
    for c in EVAL_CASES:
        print(f"{c['id']}: expect '{c['expected_status']}' -> {c['question'][:70]}")
