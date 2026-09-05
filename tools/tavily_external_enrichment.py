#!/usr/bin/env python3
"""Collect Tavily external facts for the security graph.

The output is intentionally separate from internal evidence. It can be merged
with graph/build_security_graph.py using --external-facts, where each result is
stored as an ExternalFact node with a SUPPLEMENTS edge to an existing claim or
finding.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "graph" / "out" / "external_facts.tavily.json"
TAVILY_SEARCH_URL = "https://api.tavily.com/search"


TAVILY_CASES = [
    {
        "id": "nist-mfa-authenticator-assurance",
        "external_use_case": "standards_validation",
        "query": "NIST SP 800-63B authenticator assurance levels multi-factor authentication phishing resistant",
        "supplements": "claim:mfa:core_systems",
        "target_type": "Claim",
        "include_domains": ["pages.nist.gov", "nist.gov"],
    },
    {
        "id": "owasp-top-10-web-application-risks",
        "external_use_case": "standards_validation",
        "query": "OWASP Top 10 web application security risks official",
        "supplements": "claim:sdlc:live_controls",
        "target_type": "Claim",
        "include_domains": ["owasp.org"],
    },
    {
        "id": "tls-current-guidance",
        "external_use_case": "standards_validation",
        "query": "NIST TLS 1.2 TLS 1.3 security guidance deprecated protocols official",
        "supplements": "claim:encryption:in_transit",
        "target_type": "Claim",
        "include_domains": ["nist.gov", "csrc.nist.gov"],
    },
    {
        "id": "aws-cloud-security-compliance",
        "external_use_case": "vendor_trust_validation",
        "query": "AWS cloud security compliance encryption access controls official",
        "supplements": "claim:data:aws_storage",
        "target_type": "Claim",
        "include_domains": ["aws.amazon.com", "docs.aws.amazon.com"],
    },
    {
        "id": "github-security-controls",
        "external_use_case": "vendor_trust_validation",
        "query": "GitHub Enterprise security features MFA branch protection audit logs official",
        "supplements": "claim:sdlc:live_controls",
        "target_type": "Claim",
        "include_domains": ["docs.github.com", "github.com"],
    },
    {
        "id": "google-workspace-mfa-security",
        "external_use_case": "vendor_trust_validation",
        "query": "Google Workspace security multi-factor authentication admin controls official",
        "supplements": "claim:mfa:core_systems",
        "target_type": "Claim",
        "include_domains": ["support.google.com", "workspace.google.com"],
    },
    {
        "id": "missing-auth-remediation-context",
        "external_use_case": "vapt_remediation_context",
        "query": "OWASP missing authentication access control remediation guidance official",
        "supplements": "finding:vapt:missing_auth",
        "target_type": "AssessmentFinding",
        "include_domains": ["owasp.org"],
    },
    {
        "id": "prompt-injection-remediation-context",
        "external_use_case": "vapt_remediation_context",
        "query": "OWASP Top 10 for LLM Applications prompt injection mitigation official",
        "supplements": "finding:vapt:prompt_injection",
        "target_type": "AssessmentFinding",
        "include_domains": ["owasp.org"],
    },
]


def main() -> None:
    args = parse_args()
    if args.list_cases:
        print(json.dumps({"cases": TAVILY_CASES}, indent=2, sort_keys=True))
        return

    load_env_file(args.env_file)
    api_key = args.api_key or os.environ.get("TAVILY_API_KEY")
    if not api_key and not args.dry_run:
        raise SystemExit("Missing Tavily API key. Set TAVILY_API_KEY or pass --api-key.")

    selected = select_cases(args.cases)
    facts: list[dict[str, Any]] = []
    for case in selected:
        if args.dry_run:
            facts.append(dry_run_fact(case))
            continue
        response = tavily_search(api_key or "", case, args.max_results, args.search_depth)
        facts.extend(facts_from_response(case, response, args.max_results))
        time.sleep(args.delay)

    payload = {
        "provider": "tavily",
        "source": "external",
        "retrieved_at": now_iso(),
        "policy": "supplement_only_never_override_internal_evidence",
        "facts": facts,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {len(facts)} Tavily external facts to {args.output}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect Tavily external facts for graph enrichment")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--api-key", default=None, help="Tavily API key. Prefer TAVILY_API_KEY env var.")
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env.local")
    parser.add_argument("--cases", nargs="*", default=None, help="Optional case IDs to run.")
    parser.add_argument("--max-results", type=int, default=2)
    parser.add_argument("--search-depth", choices=["basic", "advanced", "fast", "ultra-fast"], default="basic")
    parser.add_argument("--delay", type=float, default=0.2, help="Delay between Tavily calls.")
    parser.add_argument("--dry-run", action="store_true", help="Write placeholder facts without calling Tavily.")
    parser.add_argument("--list-cases", action="store_true", help="Print available Tavily cases and exit.")
    return parser.parse_args()


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def select_cases(case_ids: list[str] | None) -> list[dict[str, Any]]:
    if not case_ids:
        return TAVILY_CASES
    by_id = {case["id"]: case for case in TAVILY_CASES}
    missing = [case_id for case_id in case_ids if case_id not in by_id]
    if missing:
        raise SystemExit(f"Unknown Tavily case IDs: {', '.join(missing)}")
    return [by_id[case_id] for case_id in case_ids]


def tavily_search(api_key: str, case: dict[str, Any], max_results: int, search_depth: str) -> dict[str, Any]:
    body = {
        "query": case["query"],
        "search_depth": search_depth,
        "max_results": max_results,
        "include_answer": "basic",
        "include_raw_content": False,
        "include_domains": case.get("include_domains", []),
    }
    request = urllib.request.Request(
        TAVILY_SEARCH_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "black-convey-hackathon-graph-enrichment/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Tavily request failed for {case['id']}: HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"Tavily request failed for {case['id']}: {error}") from error


def facts_from_response(case: dict[str, Any], response: dict[str, Any], max_results: int) -> list[dict[str, Any]]:
    facts = []
    for rank, result in enumerate(response.get("results", [])[:max_results], start=1):
        facts.append(
            {
                "id": f"{case['id']}-{rank}",
                "query": response.get("query") or case["query"],
                "external_use_case": case["external_use_case"],
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "retrieved_at": now_iso(),
                "summary": result.get("content", ""),
                "supplements": case["supplements"],
                "target_type": case["target_type"],
                "result_rank": rank,
                "score": result.get("score", ""),
                "domain_filter": case.get("include_domains", []),
            }
        )
    return facts


def dry_run_fact(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": f"{case['id']}-dry-run",
        "query": case["query"],
        "external_use_case": case["external_use_case"],
        "title": "Dry-run Tavily placeholder",
        "url": "https://example.com/tavily-dry-run",
        "retrieved_at": now_iso(),
        "summary": "Dry-run placeholder. Replace by running without --dry-run after setting TAVILY_API_KEY.",
        "supplements": case["supplements"],
        "target_type": case["target_type"],
        "result_rank": 1,
        "score": "",
        "domain_filter": case.get("include_domains", []),
    }


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    main()
