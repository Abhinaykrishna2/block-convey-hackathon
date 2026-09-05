"""
General Knowledge & Conversational Intelligence Engine for Sentinel.
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional
import urllib.request


SECURITY_KEYWORDS = {
    "security", "policy", "policies", "compliance", "questionnaire", "audit", "audits",
    "soc", "soc2", "iso", "nist", "fips", "hipaa", "gdpr", "ccpa", "fedramp", "cis", "pci", "dss",
    "encrypt", "encryption", "tls", "ssl", "aes", "kms", "cipher", "ciphers", "sha", "rsa",
    "at rest", "in transit", "certificate", "cryptographic",
    "host", "hosted", "hosting", "cloud", "aws", "azure", "gcp", "server", "servers",
    "datacenter", "data center", "database", "rds", "s3", "redshift", "on-prem", "on-premise",
    "dell", "poweredge", "infrastructure", "multi-az", "us-east-1", "storage", "environment",
    "mfa", "2fa", "otp", "totp", "fido", "webauthn", "replay-resistant", "authenticat",
    "password", "passwords", "credential", "credentials", "sso", "saml", "okta", "iam",
    "access", "privilege", "least privilege", "rbac", "admin", "console", "login",
    "offboard", "offboarding", "onboard", "deprovision", "revok", "delgado",
    "contractor", "contractors", "subcontractor", "subcontractors", "sub-contractor",
    "vendor", "vendors", "third-party", "third party", "background check", "nda", "dpa",
    "employee", "personnel", "workforce",
    "siem", "log", "logs", "logging", "audit trail", "monitor", "monitoring",
    "cloudtrail", "cloudwatch", "datadog", "splunk", "observability", "alert", "alerting",
    "vapt", "pentest", "penetration", "vulnerability", "vulnerabilities", "finding", "findings",
    "cve", "cvss", "patch", "patching", "remediat", "sla", "scan", "scans",
    "bcp", "disaster", "recovery", "dr plan", "rto", "rpo", "backup", "backups", "snapshot",
    "sdlc", "secure code", "secure coding", "code review", "peer review", "git", "github",
    "pull request", "branch protection", "ci/cd", "pipeline", "deploy", "deployment",
    "w-9", "w9", "solsphere", "regodit", "headcount", "incorporation", "legal entity",
    "retention", "destruction", "disposal", "incident", "breach", "firewall", "router", "vpn",
}

WORLD_CAPITALS: Dict[str, str] = {
    "france": "Paris",
    "germany": "Berlin",
    "united kingdom": "London",
    "uk": "London",
    "england": "London",
    "italy": "Rome",
    "spain": "Madrid",
    "canada": "Ottawa",
    "japan": "Tokyo",
    "china": "Beijing",
    "india": "New Delhi",
    "australia": "Canberra",
    "brazil": "Brasília",
    "russia": "Moscow",
    "united states": "Washington, D.C.",
    "usa": "Washington, D.C.",
    "us": "Washington, D.C.",
    "america": "Washington, D.C.",
    "mexico": "Mexico City",
    "netherlands": "Amsterdam",
    "switzerland": "Bern",
    "sweden": "Stockholm",
    "norway": "Oslo",
    "denmark": "Copenhagen",
    "finland": "Helsinki",
    "ireland": "Dublin",
    "portugal": "Lisbon",
    "greece": "Athens",
    "turkey": "Ankara",
    "egypt": "Cairo",
    "south africa": "Pretoria (administrative), Cape Town (legislative), Bloemfontein (judicial)",
    "nigeria": "Abuja",
    "kenya": "Nairobi",
    "argentina": "Buenos Aires",
    "chile": "Santiago",
    "colombia": "Bogotá",
    "peru": "Lima",
    "new zealand": "Wellington",
    "singapore": "Singapore",
    "south korea": "Seoul",
    "indonesia": "Jakarta",
    "malaysia": "Kuala Lumpur",
    "thailand": "Bangkok",
    "vietnam": "Hanoi",
    "philippines": "Manila",
    "saudi arabia": "Riyadh",
    "uae": "Abu Dhabi",
    "united arab emirates": "Abu Dhabi",
    "israel": "Jerusalem",
    "poland": "Warsaw",
    "austria": "Vienna",
    "belgium": "Brussels",
    "czech republic": "Prague",
    "czechia": "Prague",
    "hungary": "Budapest",
    "romania": "Bucharest",
    "ukraine": "Kyiv",
    "pakistan": "Islamabad",
    "bangladesh": "Dhaka",
}

GENERAL_CONCEPTS: Dict[str, str] = {
    "photosynthesis": "Photosynthesis is the biological process used by plants, algae, and certain bacteria to convert light energy (typically from the sun) into chemical energy stored in glucose, releasing oxygen as a byproduct.",
    "machine learning": "Machine learning is a subfield of artificial intelligence focused on building algorithms and statistical models that learn patterns and make predictions or decisions directly from data without being explicitly programmed.",
    "artificial intelligence": "Artificial intelligence (AI) refers to systems or machines that simulate human cognitive functions such as learning, reasoning, problem-solving, perception, and language understanding.",
    "dna": "DNA (deoxyribonucleic acid) is the molecule that carries the genetic instructions for the development, functioning, growth, and reproduction of all known organisms and many viruses.",
    "speed of light": "The speed of light in a vacuum is exactly 299,792,458 meters per second (approximately 300,000 km/s or 186,282 miles per second).",
    "gravity": "Gravity is the fundamental natural phenomenon by which all things with mass or energy—including planets, stars, galaxies, and even light—are attracted toward one another.",
    "internet": "The internet is a globally connected system of computer networks that uses the Internet Protocol Suite (TCP/IP) to link billions of devices worldwide.",
    "cloud computing": "Cloud computing is the on-demand delivery of computing services—including servers, storage, databases, networking, software, and analytics—over the internet with pay-as-you-go pricing.",
}


def is_security_domain_query(message: str, retriever=None) -> bool:
    m_low = message.strip().lower()

    if re.search(r"\b(?:question|item|control)\s*#?\s*[0-9]{1,2}\b", m_low) or re.search(r"\bq[0-9]{1,2}\b", m_low):
        return True

    if retriever and hasattr(retriever, "_match_question"):
        try:
            matched = retriever._match_question(message)
            if matched:
                return True
        except Exception:
            pass

    words = set(re.findall(r"\b[a-z0-9\-\_]{2,}\b", m_low))
    if any(k in words or any(k in w for w in words) for k in SECURITY_KEYWORDS):
        return True

    security_phrases = [
        "at rest", "in transit", "data center", "customer data", "company data",
        "third party", "vendor review", "access control", "disaster recovery",
        "code review", "pull request", "penetration test", "audit trail"
    ]
    if any(phrase in m_low for phrase in security_phrases):
        return True

    return False


def _get_api_key() -> Optional[str]:
    key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_KEY")
    if key:
        return key.strip()
    for p in [
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.join(os.path.dirname(__file__), "..", ".env"),
    ]:
        if os.path.exists(p):
            with open(p) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("OPENROUTER_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip(''')
                    if line.startswith("OPENROUTER_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip(''')
    return None


def call_live_llm_general(message: str) -> Optional[str]:
    api_key = _get_api_key()
    if not api_key:
        return None

    models = [
        os.environ.get("OPENROUTER_MODEL", "z-ai/glm-5.3"),
        "z-ai/glm-5.3-flash",
        "z-ai/glm-5.2:free",
        "openrouter/free",
    ]

    system_prompt = (
        "You are Sentinel, an intelligent AI Security Analyst for Regodit. "
        "The user is asking a general knowledge or conversational question outside the security domain. "
        "Answer their question intelligently, accurately, and concisely. "
        "Do NOT mention or cite internal security documents, policies, or questionnaire controls. "
        "At the end of your answer, include a brief polite one-sentence note that while you can answer general questions, "
        "your core specialization is Regodit's security compliance, cloud architecture, and vendor questionnaires."
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Sentinel AI Security Analyst",
    }

    for model in models:
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
                "temperature": 0.3,
            }
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "").strip()
        except Exception:
            continue
    return None


def handle_general_knowledge_query(message: str) -> Optional[Dict[str, Any]]:
    m_clean = message.strip()
    m_low = m_clean.lower().strip("?!. ")

    # 1. Math / Calculation Queries
    math_pattern = r"^\s*(?:what\s+is\s+)?([0-9\.\s\+\-\*/\(\)\^%]+?)\s*\??\s*$"
    m_math = re.match(math_pattern, m_clean, re.IGNORECASE)
    if m_math:
        candidate_expr = m_math.group(1).strip()
        if any(op in candidate_expr for op in ["+", "-", "*", "/", "^", "%"]) and any(c.isdigit() for c in candidate_expr):
            if not re.search(r"[a-zA-Z_]", candidate_expr):
                try:
                    calc_expr = candidate_expr.replace("^", "**")
                    val = eval(calc_expr, {"__builtins__": None}, {})
                    if isinstance(val, float) and val.is_integer():
                        val = int(val)
                    return {
                        "reply": (
                            f"**{candidate_expr} = {val}**\n\n"
                            "*(Note: As Regodit's AI Security Analyst, my primary focus is evaluating security controls, verifying compliance questionnaires, and analyzing our infrastructure posture. Let me know if you have questions about our security policies!)*"
                        ),
                        "status": "answered",
                        "confidence": 1.0,
                        "confidenceBasis": {
                            "source_freshness": "N/A: General mathematical calculation.",
                            "directness": "Direct deterministic arithmetic calculation.",
                            "cross_verification": "Mathematical identity.",
                            "summary": "Standard mathematical result (not derived from security documentation)."
                        },
                        "externalCheck": None,
                        "citations": [],
                        "graphTrace": {
                            "logs": [
                                f"received arithmetic query: '{candidate_expr}'",
                                f"computed result: {val}",
                                "Golden Rule: accurate calculation without fabricating security documentation citations"
                            ],
                            "nodes": [
                                {"id": "q", "label": candidate_expr, "type": "query", "layer": 0},
                                {"id": "calc", "label": f"Arithmetic: {val}", "type": "control", "layer": 1}
                            ],
                            "edges": [{"from": "q", "to": "calc", "rel": "EVALUATED"}]
                        },
                        "followUp": None,
                        "clarifyingQuestion": None,
                        "recommendation": None,
                        "recommendationAction": None,
                        "questionId": None,
                    }
                except Exception:
                    pass

    # 2. Capital City Queries (e.g. "What is the capital of France?", "capital of Germany")
    cap_match = re.search(r"\bcapital\s+(?:city\s+)?(?:of\s+)?([a-zA-Z\s]+)", m_low)
    if cap_match:
        country_query = cap_match.group(1).strip()
        for country, capital in WORLD_CAPITALS.items():
            if country in country_query or country_query in country:
                country_title = country.title()
                return {
                    "reply": (
                        f"The capital of {country_title} is **{capital}**.\n\n"
                        "*(Note: As Regodit's AI Security Analyst, my primary focus is evaluating security controls, verifying vendor compliance questionnaires, and analyzing our infrastructure posture. Feel free to ask questions about our cloud infrastructure, encryption, access controls, or audit readiness!)*"
                    ),
                    "status": "answered",
                    "confidence": 1.0,
                    "confidenceBasis": {
                        "source_freshness": "Authoritative world geography.",
                        "directness": "Direct factual response to general knowledge inquiry.",
                        "cross_verification": "World capitals index.",
                        "summary": "General world knowledge question answered directly without querying corporate security policies."
                    },
                    "externalCheck": None,
                    "citations": [],
                    "graphTrace": {
                        "logs": [
                            f"query classified as geographical general knowledge: '{country_title}'",
                            f"resolved capital: {capital}",
                            "bypassed corporate security graph retrieval to prevent false citations"
                        ],
                        "nodes": [
                            {"id": "q", "label": m_clean[:40], "type": "query", "layer": 0},
                            {"id": "gk", "label": f"World Knowledge: Capital of {country_title}", "type": "control", "layer": 1}
                        ],
                        "edges": [{"from": "q", "to": "gk", "rel": "RESOLVED_AS_GENERAL_KNOWLEDGE"}]
                    },
                    "followUp": None,
                    "clarifyingQuestion": None,
                    "recommendation": None,
                    "recommendationAction": None,
                    "questionId": None,
                }

    # 3. Jokes / Humor
    if any(w in m_low for w in ["joke", "funny", "make me laugh"]):
        return {
            "reply": (
                "Here is a security joke for you:\n\n"
                "**Why do security engineers prefer dark mode?**\n"
                "*Because light attracts bugs!* 🐛\n\n"
                "*(Whenever you are ready, I'm here to assist with vendor questionnaires, policy verification, or architecture reviews!)*"
            ),
            "status": "answered",
            "confidence": 1.0,
            "confidenceBasis": {
                "source_freshness": "Humor database.",
                "directness": "Direct conversational response.",
                "cross_verification": "Internal analyst humor.",
                "summary": "Conversational humor response."
            },
            "externalCheck": None,
            "citations": [],
            "graphTrace": {
                "logs": ["received joke request", "responded with cybersecurity humor"],
                "nodes": [
                    {"id": "q", "label": m_clean[:40], "type": "query", "layer": 0},
                    {"id": "humor", "label": "Conversational Humor", "type": "control", "layer": 1}
                ],
                "edges": [{"from": "q", "to": "humor", "rel": "HUMOR"}]
            },
            "followUp": None,
            "clarifyingQuestion": None,
            "recommendation": None,
            "recommendationAction": None,
            "questionId": None,
        }

    # 4. Try live LLM for general knowledge if API key is configured
    live_answer = call_live_llm_general(m_clean)
    if live_answer:
        return {
            "reply": live_answer,
            "status": "answered",
            "confidence": 1.0,
            "confidenceBasis": {
                "source_freshness": "Live LLM general intelligence.",
                "directness": "Direct general knowledge response.",
                "cross_verification": "Foundation model pre-training.",
                "summary": "General inquiry answered directly without querying corporate security policies."
            },
            "externalCheck": None,
            "citations": [],
            "graphTrace": {
                "logs": [
                    "query classified as general knowledge / out-of-scope for corporate security",
                    "bypassed corporate security graph retrieval to prevent false citations",
                    "resolved via live LLM intelligence"
                ],
                "nodes": [
                    {"id": "q", "label": m_clean[:40], "type": "query", "layer": 0},
                    {"id": "llm-gk", "label": "Live LLM General Intelligence", "type": "control", "layer": 1}
                ],
                "edges": [{"from": "q", "to": "llm-gk", "rel": "RESOLVED_AS_GENERAL_KNOWLEDGE"}]
            },
            "followUp": None,
            "clarifyingQuestion": None,
            "recommendation": None,
            "recommendationAction": None,
            "questionId": None,
        }

    # 5. Check definitions of common concepts
    for concept, definition in GENERAL_CONCEPTS.items():
        if concept in m_low:
            return {
                "reply": (
                    f"**{concept.title()}**:\n\n{definition}\n\n"
                    "*(Note: As Regodit's AI Security Analyst, my primary focus is evaluating security controls, verifying vendor compliance questionnaires, and analyzing our infrastructure posture. Feel free to ask questions about our cloud infrastructure, encryption, access controls, or audit readiness!)*"
                ),
                "status": "answered",
                "confidence": 1.0,
                "confidenceBasis": {
                    "source_freshness": "General scientific / technical encyclopedia.",
                    "directness": "Direct definition response.",
                    "cross_verification": "Standard conceptual definitions.",
                    "summary": "General concept defined directly without querying corporate security policies."
                },
                "externalCheck": None,
                "citations": [],
                "graphTrace": {
                    "logs": [
                        f"query classified as general conceptual inquiry: '{concept}'",
                        "bypassed corporate security graph retrieval to prevent false citations"
                    ],
                    "nodes": [
                        {"id": "q", "label": m_clean[:40], "type": "query", "layer": 0},
                        {"id": "def", "label": f"General Definition: {concept.title()}", "type": "control", "layer": 1}
                    ],
                    "edges": [{"from": "q", "to": "def", "rel": "RESOLVED_AS_GENERAL_KNOWLEDGE"}]
                },
                "followUp": None,
                "clarifyingQuestion": None,
                "recommendation": None,
                "recommendationAction": None,
                "questionId": None,
            }

    # 6. General Intelligent Fallback for other non-security questions
    return {
        "reply": (
            f"You asked: *\"{m_clean}\"*\n\n"
            "As an autonomous **AI Security Analyst for Regodit**, I am specialized in analyzing our technical architecture, verifying vendor compliance questionnaires (SOC 2, ISO 27001, NIST SP 800-53/63B), and surfacing internal policy contradictions.\n\n"
            "This question falls outside of our corporate security and IT documentation, so under our **Golden Rule (never fabricate answers)**, I do not generate speculative security answers for it.\n\n"
            "**Here are topics I can help you evaluate:**\n"
            "- **Cloud Hosting Architecture & Infrastructure** (AWS services, on-prem backup assets)\n"
            "- **Data Encryption Standards** (TLS 1.2/1.3, AES-256 KMS at rest)\n"
            "- **Authentication & MFA Enforcement** (TOTP, FIDO2, replay-resistant authentication)\n"
            "- **Logging, Audit Trails & SIEM** (CloudTrail, CloudWatch, centralized retention)\n"
            "- **Subcontractor Governance & Access Deprovisioning SLAs**\n"
            "- **Penetration Testing (VAPT) & Vulnerability Remediation**"
        ),
        "status": "answered",
        "confidence": 1.0,
        "confidenceBasis": {
            "source_freshness": "Sentinel assistant capabilities profile.",
            "directness": "Direct scope clarification.",
            "cross_verification": "Golden Rule compliance policy.",
            "summary": "General out-of-scope query recognized and clarified without citing corporate security documents."
        },
        "externalCheck": None,
        "citations": [],
        "graphTrace": {
            "logs": [
                "query recognized as outside security compliance domain",
                "bypassed corporate security graph retrieval to prevent false citations",
                "Golden Rule enforced: explained scope and offered security assistance"
            ],
            "nodes": [
                {"id": "q", "label": m_clean[:40], "type": "query", "layer": 0},
                {"id": "scope", "label": "Scope Clarification (Outside Security Domain)", "type": "control", "layer": 1}
            ],
            "edges": [{"from": "q", "to": "scope", "rel": "CLARIFIED_SCOPE"}]
        },
        "followUp": None,
        "clarifyingQuestion": None,
        "recommendation": None,
        "recommendationAction": None,
        "questionId": None,
    }
