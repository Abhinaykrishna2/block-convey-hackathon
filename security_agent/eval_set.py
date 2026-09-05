"""
Eval set for the Regodit AI Security Analyst agent.

Each entry is a REAL question - either straight from the 66-item
vendor questionnaire matrix, or (for the C-prefixed cases) phrased
from a contradiction in the teammate's MASTER_CORPUS_INDEX.md
contradiction-resolution matrix - with a GROUND TRUTH label that
was verified by hand-reading the actual source documents. Running
agent_loop.process_question() against these and comparing to
expected_status is the eval.

Quality over quantity: a handful of hand-checked cases you trust
completely beats 66 guesses. Currently 10 cases; add more from the
remaining questionnaire items and the two unexploited contradictions
(C3 legal-entity-name, C7 VAPT/SLA - already partially covered by
Q65/Q66) as they get verified by hand.
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
        "expected_status": "ask_user",
        "expected_answer_gist": None,
        "ground_truth_source": "VAPT Report 01.docx (findings table, 20/20 rows = Open) vs Regodit_vulnerability_and_patch_management_policy_v1.0.docx (remediation SLA: 7 days Critical, 30 days High)",
        "notes": "Revised from 'answered'/No: a point-in-time 'Open' status snapshot doesn't by itself confirm findings are UNremediated at the time of the questionnaire response, since policy gives 7/30-day SLA windows to close them. The agent shouldn't assume breach-of-SLA (or compliance) from the table alone - it must ask engineering for current status rather than answer flatly from a snapshot. See MASTER_CORPUS_INDEX.md C7.",
    },
    {
        "id": "Q6",
        "question": "Will you be using any contractors or sub-contractors to complete the engagement with Regodit?",
        "expected_status": "ask_user",
        "expected_answer_gist": None,
        "ground_truth_source": None,
        "notes": "This is a fact about THIS specific engagement/vendor relationship, not something Regodit's own internal policies would state. Correct behavior is to ask, not guess.",
    },

    # --- Contradiction cases below, sourced from teammate's
    # MASTER_CORPUS_INDEX.md "Master Contradictions & Conflict
    # Resolution Matrix" (section 2). IDs match the matrix's own
    # C-identifiers, not the 66-item questionnaire numbering. ---

    {
        "id": "C1",
        "question": "Will Regodit data be stored on site, in a data center, or by a third party?",
        "expected_status": "conflict",
        "expected_answer_gist": None,
        "ground_truth_source": "Regodit_information_security_policy_v1.0.docx (Sec 8 & 12: 'operates no on-premises servers or data centers... 100% AWS') vs Asset_Inventory_Regodit.xlsx (Row 10: 'Dell PowerEdge R740 (on-prem backup) ... Located in HQ server room')",
        "notes": "Policy claims cloud-only; the asset inventory lists real on-prem hardware designated for backups. Agent must surface both and ask whether active customer data ever touches the on-prem box, not flatten to a clean 'cloud-only' answer.",
    },
    {
        "id": "C2",
        "question": "Does your organization operate a centralized SIEM for security event logging?",
        "expected_status": "conflict",
        "expected_answer_gist": None,
        "ground_truth_source": "network-segmentation-diagram.png / admin-access-logging-diagram.png (depict a 'Centralized logging: SIEM, alerting, retention' pipeline) vs Regodit_information_security_policy_v1.0.docx Sec 11 ('does not currently operate a dedicated SIEM; centralized log analytics is a planned improvement... logs shipped to object storage, ~1 year retention')",
        "notes": "Architecture diagrams show a target-state SIEM; the policy text says none exists yet and describes the actual cloud-native (CloudWatch/S3) setup. network_architecture_diagrams.pdf p.2 even self-labels as an 'illustrative template' - a real test of whether the agent trusts a diagram over the governing policy text.",
    },
    {
        "id": "C4",
        "question": "When an employee or contractor departs, is their access to production systems revoked immediately?",
        "expected_status": "conflict",
        "expected_answer_gist": None,
        "ground_truth_source": "Regodit_hr_policy_v1.0.docx (mandates immediate revocation of system/email/cloud accounts on exit) vs Access_Review_Records.xlsx (contractor M. Delgado's laptop wiped 08/30/2026 per Asset_Inventory_Regodit.xlsx, but the 09/04/2026 review still shows an active AWS Admin role, flagged 'Access Justified: N | Action needed: Revoke access')",
        "notes": "Policy promises immediate revocation; the real access-review record shows a 5-day live gap that only got caught by a periodic review, not by the offboarding process itself. Agent should flag the documented lag as evidence the control doesn't always fire on time, not answer a flat 'Yes'.",
    },
    {
        "id": "C5",
        "question": "How many employees does the company currently have, and when was it incorporated?",
        "expected_status": "conflict",
        "expected_answer_gist": None,
        "ground_truth_source": "Regodit AI_SOC2_Type_II_Report_Test.docx Sec 3.1 ('incorporation in June 2025... grown to a team of twelve (12) personnel') vs Sec 3.1.2 of the SAME document ('Since its incorporation in August 2024, the company has grown to 9 personnel')",
        "notes": "The contradiction is INTERNAL to a single source document, not cross-document - tests whether the agent catches an inconsistency within one file instead of only diffing across two. Both numbers should be surfaced and the agent should ask for current headcount rather than pick one.",
    },
    {
        "id": "C6",
        "question": "Do you have a documented, finalized Secure Development Lifecycle (SDLC) policy in place?",
        "expected_status": "answered",
        "expected_answer_gist": "Yes - core SDLC controls (PR peer review in GitHub, separate prod/non-prod environments, CTO/CEO/CPO approval before production deploys) are active and enforced under Regodit_information_security_policy_v1.0.docx Sec 13, even though the standalone SDLC document is an unfilled template.",
        "ground_truth_source": "Secure Development Lifecycle Document 01.docx (unfinalized template, still has <Company Name>/<Policy owner> placeholders) vs Regodit_information_security_policy_v1.0.docx Sec 13 (live, enforced controls)",
        "notes": "Source-authenticity test: naive retrieval that surfaces the empty placeholder template first could wrongly answer 'No' or flag a spurious conflict. The correct read is that the governing policy is authoritative and already-enforced; the template's draft status doesn't override it. Distinguishing an unexecuted draft from a governing policy is the point of this case.",
    },
]

if __name__ == "__main__":
    for c in EVAL_CASES:
        print(f"{c['id']}: expect '{c['expected_status']}' -> {c['question'][:70]}")
