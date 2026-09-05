"""
External Standards & Authority Validation Engine for Regodit AI Security Analyst.

Implements live Python external checks (e.g. NIST SP 800-63B, OWASP Top 10, NIST TLS Guidance)
outlined in graph/ARCHITECTURE.md as ExternalFact nodes.

Boundary Principle:
  External checks SUPPLEMENT internal evidence for regulatory & standards benchmarking,
  but NEVER override, replace, or fabricate internal company evidence.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_FACTS_PATH = ROOT / "graph" / "out" / "external_facts.tavily.json"
TAVILY_SEARCH_URL = "https://api.tavily.com/search"

# Built-in authoritative standards library (serves as grounded fallback & baseline)
STANDARDS_LIBRARY = {
    "mfa": {
        "standard": "NIST SP 800-63B",
        "title": "NIST Special Publication 800-63B: Digital Identity Guidelines - Authentication & Lifecycle Management",
        "url": "https://pages.nist.gov/800-63-4/sp800-63b.html",
        "external_node_id": "external:nist-mfa-authenticator-assurance-1",
        "provider": "nist.gov",
        "use_case": "standards_validation",
        "benchmark_summary": (
            "NIST SP 800-63B Section 5.1 distinguishes between Authenticator Assurance Level 2 (AAL2, requiring "
            "multi-factor with OTP/TOTP or out-of-band authenticators) and Authenticator Assurance Level 3 "
            "(AAL3, requiring phishing-resistant cryptographic hardware authenticators such as FIDO2/WebAuthn or PIV). "
            "Authenticators that rely on manual OTP entry are not phishing-resistant under Section 5.1.4."
        ),
        "relevance_keywords": ["mfa", "multi-factor", "otp", "replay-resistant", "authenticat", "2fa", "two-factor"],
    },
    "tls": {
        "standard": "NIST SP 800-52 Rev. 2 & FIPS 140-3",
        "title": "NIST Guidelines for the Selection, Configuration, and Use of TLS Implementations",
        "url": "https://csrc.nist.gov/publications/detail/sp/800-52/rev-2/final",
        "external_node_id": "external:tls-current-guidance-1",
        "provider": "csrc.nist.gov",
        "use_case": "standards_validation",
        "benchmark_summary": (
            "NIST SP 800-52 Rev. 2 mandates TLS 1.2 and urges migration to TLS 1.3. Explicitly deprecates SSL 2.0, "
            "SSL 3.0, TLS 1.0, and TLS 1.1 due to vulnerability to POODLE, BEAST, and cipher downgrade attacks. "
            "Requires FIPS-approved cryptographic cipher suites (AES-GCM, ECDHE)."
        ),
        "relevance_keywords": ["tls", "encrypt", "transit", "cipher", "ssl", "cryptograph"],
    },
    "owasp_web": {
        "standard": "OWASP Top 10:2021",
        "title": "OWASP Top 10 Web Application Security Risks",
        "url": "https://owasp.org/www-project-top-ten",
        "external_node_id": "external:owasp-top-10-web-application-risks-1",
        "provider": "owasp.org",
        "use_case": "standards_validation",
        "benchmark_summary": (
            "OWASP Top 10 categories A01:2021 (Broken Access Control) and A07:2021 (Identification and Authentication Failures) "
            "highlight missing access enforcement, missing MFA on user portals, and credential stuffing vulnerabilities. "
            "Mandates secure defaults, automated session invalidation, and mandatory multi-factor authentication."
        ),
        "relevance_keywords": ["owasp", "web app", "vulnerability", "vapt", "missing auth", "penetration test"],
    },
    "owasp_llm": {
        "standard": "OWASP Top 10 for LLM Applications 2025",
        "title": "OWASP Top 10 for Large Language Model Applications",
        "url": "https://owasp.org/www-project-top-10-for-large-language-model-applications",
        "external_node_id": "external:prompt-injection-remediation-context-1",
        "provider": "owasp.org",
        "use_case": "vapt_remediation_context",
        "benchmark_summary": (
            "OWASP LLM01:2025 (Prompt Injection) addresses threats where untrusted inputs manipulate LLM execution context. "
            "Remediation requires strict input sanitization, context boundary isolation, output encoding, and deterministic "
            "guardrail verification before action execution."
        ),
        "relevance_keywords": ["prompt injection", "llm", "ai agent", "genai", "adversarial"],
    },
    "cloud_aws": {
        "standard": "CIS AWS Foundations Benchmark v3.0.0",
        "title": "CIS Amazon Web Services Foundations Benchmark",
        "url": "https://www.cisecurity.org/benchmark/amazon_web_services",
        "external_node_id": "external:aws-cloud-security-compliance-1",
        "provider": "cisecurity.org",
        "use_case": "vendor_trust_validation",
        "benchmark_summary": (
            "CIS AWS Section 1 (Identity and Access Management) requires hardware MFA for the AWS root account, "
            "MFA for all IAM users with console access, credential rotation every 90 days, and CloudTrail enabled in all regions."
        ),
        "relevance_keywords": ["aws", "cloud storage", "bucket", "s3", "iam", "cloudwatch"],
    },
}


def _load_cached_external_facts() -> Dict[str, Any]:
    if EXTERNAL_FACTS_PATH.exists():
        try:
            with open(EXTERNAL_FACTS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"facts": []}


CACHED_FACTS = _load_cached_external_facts()


def query_live_tavily(query: str, api_key: str, domains: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
    """Perform live external web check using Tavily Search API if key is available."""
    if not api_key:
        return None
    body = {
        "query": query,
        "search_depth": "basic",
        "max_results": 2,
        "include_answer": "basic",
        "include_domains": domains or ["nist.gov", "owasp.org", "csrc.nist.gov"],
    }
    req = urllib.request.Request(
        TAVILY_SEARCH_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "regodit-security-analyst/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("results", [])
            if results:
                top = results[0]
                return {
                    "title": top.get("title", ""),
                    "url": top.get("url", ""),
                    "summary": top.get("content", "")[:350],
                    "score": top.get("score"),
                }
    except Exception:
        pass
    return None


def perform_external_standards_check(
    question: str,
    control_intent: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Live Python call in the agent loop for external checks (e.g. NIST SP 800-63B).
    
    Identifies if the control targets an external compliance benchmark (MFA, TLS, OWASP, AWS).
    Queries live Tavily API if configured, otherwise enriches via authoritative ExternalFact library.
    """
    q_norm = question.lower()
    intent_norm = (control_intent or "").lower()

    # Find matching standard domain
    matched_key = None
    for key, spec in STANDARDS_LIBRARY.items():
        if any(kw in q_norm or kw in intent_norm for kw in spec["relevance_keywords"]):
            matched_key = key
            break

    if not matched_key:
        return None

    spec = STANDARDS_LIBRARY[matched_key]
    key_env = api_key or os.environ.get("TAVILY_API_KEY")

    live_hit = None
    if key_env:
        domains = ["pages.nist.gov", "nist.gov"] if "nist" in spec["provider"] else ["owasp.org"]
        live_hit = query_live_tavily(f"{spec['standard']} requirements", key_env, domains)

    # Check cached ExternalFact nodes from graph/out/external_facts.tavily.json
    node_id = spec["external_node_id"]
    cached_node = next((f for f in CACHED_FACTS.get("facts", []) if f.get("id") == node_id.replace("external:", "")), None)

    summary = (
        (live_hit.get("summary") if live_hit else None)
        or (cached_node.get("summary") if cached_node else None)
        or spec["benchmark_summary"]
    )
    url = (live_hit.get("url") if live_hit else None) or (cached_node.get("url") if cached_node else None) or spec["url"]
    title = (live_hit.get("title") if live_hit else None) or (cached_node.get("title") if cached_node else None) or spec["title"]

    return {
        "standard": spec["standard"],
        "title": title,
        "url": url,
        "external_node_id": node_id,
        "provider": spec["provider"],
        "use_case": spec["use_case"],
        "benchmark_summary": summary.strip(),
        "isolation_rule": "supplement_only_never_override_internal_evidence",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "live_check_executed": bool(live_hit),
    }


if __name__ == "__main__":
    print("Testing external standards check (MFA -> NIST SP 800-63B)...")
    res = perform_external_standards_check("Does your organization require replay-resistant authentication mechanisms such as OTP or MFA?")
    print(json.dumps(res, indent=2))
