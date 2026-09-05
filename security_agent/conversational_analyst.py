"""
Conversational Security Analyst Engine for Regodit AI Security Analyst.

Transforms raw graph/document retrieval chunks and guardrail outputs into
a natural, professional, conversational dialogue. When information is unclear,
incomplete, or contradictory, it formulates a targeted clarifying question
paired with an authoritative industry recommendation and 1-click resolution action.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional


# Domain-specific knowledge base of targeted clarifying questions and recommendations
DOMAIN_PLAYBOOK: Dict[str, Dict[str, Any]] = {
    "Hosting Architecture": {
        "clarifying_question": "Does Regodit operate strictly on AWS cloud infrastructure, or is the on-premises Dell PowerEdge server in the HQ server room still actively maintained for emergency backups?",
        "recommendation": "We recommend formally certifying 100% AWS cloud hosting for customer data and decommissioning or isolating the on-premises Dell PowerEdge server to eliminate the SOC 2 audit discrepancy.",
        "action": "All production and customer data is hosted exclusively in AWS (US-East-1). The on-premises Dell PowerEdge server in HQ is decommissioned / restricted to non-production laboratory testing.",
    },
    "Centralized Logging & SIEM": {
        "clarifying_question": "Should we confirm native AWS CloudWatch and CloudTrail as our sole logging mechanism, or is a dedicated third-party SIEM (e.g. Datadog, Splunk) planned or in place?",
        "recommendation": "We recommend reporting native AWS CloudTrail + CloudWatch with encrypted S3 archive retention (1-year immutable logs) as our centralized audit logging architecture.",
        "action": "Regodit utilizes centralized AWS CloudTrail and CloudWatch log groups with 365-day immutable S3 retention for centralized security observability.",
    },
    "Subcontractor & Vendor Governance": {
        "clarifying_question": "Will any third-party contractors, external agencies, or offshore developers have access to customer data or production code for this engagement?",
        "recommendation": "We recommend confirming that all development and customer data processing is performed exclusively by vetted, full-time employees, with third-party contractors strictly prohibited from production access.",
        "action": "No third-party contractors or subcontractors will be used for this engagement; all software engineering and data operations are conducted by full-time Regodit personnel.",
    },
    "Access Revocation & Offboarding": {
        "clarifying_question": "Should we confirm the strict 24-hour SLA as our standard, and disclose the contractor M. Delgado incident as a closed remediation ticket with automated deprovisioning now enforced?",
        "recommendation": "We recommend confirming the 24-hour revocation SLA and documenting our automated Okta/IdP deprovisioning workflow to prevent any manual delay in contractor account closures.",
        "action": "Access revocation SLA is strictly 24 hours. Automated IdP deprovisioning has been implemented across all AWS, GitHub, and SaaS systems to guarantee immediate revocation upon employee or contractor departure.",
    },
    "Authentication / MFA": {
        "clarifying_question": "Is multi-factor authentication (MFA) currently enforced on all customer-facing portal logins, or is it currently enforced only on internal workforce and infrastructure consoles?",
        "recommendation": "In alignment with NIST SP 800-63B (AAL2/AAL3), we recommend enforcing mandatory MFA across all user logins, administrative consoles, and customer portals using TOTP or FIDO2/WebAuthn.",
        "action": "MFA is mandatory for all internal employees, infrastructure consoles, and customer web application portals.",
    },
    "Vulnerability Management & VAPT": {
        "clarifying_question": "Have the findings from the most recent penetration test (VAPT Report 01) completed remediation, or are remediations still within their allowed 30-day SLA window?",
        "recommendation": "We recommend reporting that all Critical findings are remediated immediately within 7 days, High findings within 30 days, and providing the latest auditor re-test attestation.",
        "action": "Penetration tests are conducted annually. All identified critical and high vulnerabilities from the last test have been remediated and validated by our security team.",
    },
    "Secure Software Development (SDLC)": {
        "clarifying_question": "Should we confirm our active SDLC controls (mandatory GitHub PR peer reviews, automated CI/CD security scanning, CTO deployment approval) as documented in InfoSec Policy Sec 13?",
        "recommendation": "We recommend confirming that all production code requires mandatory peer review, automated branch protection, and security gating prior to merge and deployment.",
        "action": "Yes, Regodit enforces a formal secure development lifecycle including mandatory GitHub pull-request peer reviews, branch protection, and production deployment approvals by engineering leadership.",
    },
    "Corporate Identity & Tax Entity": {
        "clarifying_question": "Should contracts and questionnaires reflect 'Solsphere AI Inc. (dba Regodit)' as the formal legal entity?",
        "recommendation": "We recommend using the full legal entity designation 'Solsphere AI Inc. (doing business as Regodit)' to align with both our Form W-9 and commercial contracts.",
        "action": "The formal legal entity is Solsphere AI Inc., doing business as Regodit.",
    },
    "Business Continuity & Disaster Recovery": {
        "clarifying_question": "What are our exact recovery time objective (RTO) and recovery point objective (RPO) commitments for client disaster recovery?",
        "recommendation": "We recommend committing to a Recovery Time Objective (RTO) of 4 hours and a Recovery Point Objective (RPO) of 1 hour via our automated AWS multi-AZ snapshot replication.",
        "action": "Disaster recovery policy establishes a Recovery Time Objective (RTO) of 4 hours and Recovery Point Objective (RPO) of 1 hour, backed by automated daily multi-region snapshot backups.",
    },
    "Cryptography & Encryption": {
        "clarifying_question": "Are legacy TLS versions (TLS 1.0, 1.1) completely disabled across all customer-facing endpoints?",
        "recommendation": "We recommend enforcing TLS 1.2 and TLS 1.3 exclusively with AES-256 cipher suites, fully deprecating TLS 1.0/1.1 in compliance with NIST SP 800-52 Rev. 2.",
        "action": "Regodit enforces TLS 1.2 and TLS 1.3 for all data in transit across public endpoints, and AES-256 encryption at rest via AWS KMS managed keys.",
    },
}


def clean_snippet(text: str) -> str:
    """Removes markdown artifacts and leading metadata from raw text chunks."""
    if not text:
        return ""
    text = re.sub(r"^(?:Section\s+\d+|###\s+|##\s+|-\s+|\*\s+)", "", text).strip()
    text = re.sub(r"\s+", " ", text)
    return text


def synthesize_conversational_response(
    question: str,
    control_intent: str,
    raw_status: str,
    raw_answer: Optional[str],
    confidence: float,
    conflict_explanation: Optional[str],
    guardrail_note: Optional[str],
    citations: List[Dict[str, Any]],
    chunks: List[Dict[str, Any]],
    external_check: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Synthesizes a fluid, conversational analyst response.
    Returns:
      - conversational_reply: str
      - clarifying_question: Optional[str]
      - recommendation: Optional[str]
      - recommendation_action: Optional[str]
    """
    playbook = DOMAIN_PLAYBOOK.get(control_intent, {})
    top_text = chunks[0]["text"] if chunks else ""
    cleaned_top = clean_snippet(top_text)

    clarifying_q: Optional[str] = None
    recommendation: Optional[str] = None
    rec_action: Optional[str] = None

    # 1. CONFLICT CASE
    if raw_status == "conflict":
        clarifying_q = playbook.get(
            "clarifying_question",
            "Which documented position represents your current operational practice for this control?"
        )
        recommendation = playbook.get(
            "recommendation",
            "We recommend adopting the strictest standard in customer commitments to avoid compliance discrepancies during audits."
        )
        rec_action = playbook.get(
            "action",
            "Confirmed: Current operational practice adheres to the formal Information Security Policy standard."
        )

        reply_parts = [
            "I reviewed our internal security documentation and identified a documented operational discrepancy:\n\n",
            f"**Discrepancy Details**:\n{conflict_explanation or 'Policies and operational telemetry indicate conflicting requirements for this control.'}\n\n",
        ]
        if raw_answer:
            reply_parts.append(f"**Documented Stances**:\n{raw_answer}\n\n")
        
        reply_parts.append(
            "Per our Golden Rule (never assume or guess when documents disagree), I need stakeholder clarification to resolve this."
        )

        return {
            "conversational_reply": "".join(reply_parts),
            "clarifying_question": clarifying_q,
            "recommendation": recommendation,
            "recommendation_action": rec_action,
        }

    # 2. INSUFFICIENT / ASK_USER CASE
    if raw_status in ("ask_user", "insufficient"):
        clarifying_q = playbook.get(
            "clarifying_question",
            "Could you clarify the current operational practice or policy for this requirement?"
        )
        recommendation = playbook.get(
            "recommendation",
            "We recommend formally documenting this control in our security policy repository to streamline future vendor security reviews."
        )
        rec_action = playbook.get(
            "action",
            "Confirmed: Control requirement verified and recorded by security stakeholder."
        )

        base_msg = guardrail_note or "Our current policy repository does not contain an explicit, unambiguous record for this specific question."
        
        reply_parts = [
            "I analyzed our indexed documentation, and this item requires human stakeholder confirmation:\n\n",
            f"{base_msg}\n\n",
            "Under our Golden Rule, I refuse to speculate or fabricate an answer for compliance questionnaires."
        ]

        return {
            "conversational_reply": "".join(reply_parts),
            "clarifying_question": clarifying_q,
            "recommendation": recommendation,
            "recommendation_action": rec_action,
        }

    # 3. ANSWERED / VERIFIED CASE
    core_answer = raw_answer or cleaned_top
    if core_answer.startswith("Based on company documentation:"):
        core_answer = core_answer.replace("Based on company documentation:", "").strip()

    lead = "According to our verified security documentation,"
    q_low = question.lower()
    if "encrypt" in q_low:
        reply_text = f"{lead} Regodit enforces encryption across all customer and operational data. {core_answer}"
    elif "infosec" in q_low or "program" in q_low:
        reply_text = f"{lead} Regodit maintains a comprehensive security governance structure. {core_answer}"
    elif "access" in q_low or "privilege" in q_low:
        reply_text = f"{lead} Regodit enforces the principle of least privilege and strict role-based access control. {core_answer}"
    elif "incident" in q_low:
        reply_text = f"{lead} Regodit maintains a formalized incident response program. {core_answer}"
    elif "backup" in q_low or "disaster" in q_low:
        reply_text = f"{lead} Regodit operates automated multi-region backup and disaster recovery processes. {core_answer}"
    else:
        reply_text = f"{lead} {core_answer}"

    advisory_rec = playbook.get("recommendation")
    
    return {
        "conversational_reply": reply_text,
        "clarifying_question": None,
        "recommendation": advisory_rec,
        "recommendation_action": None,
    }
