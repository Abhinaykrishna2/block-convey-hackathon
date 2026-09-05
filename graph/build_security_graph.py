#!/usr/bin/env python3
"""Build a Neo4j-ready security evidence graph from the cleaned corpus.

The graph is generated from the curated corpus, questionnaire JSON, source
manifest, and master index under data/black-convey-hackathon. It does not call
external services and does not mutate the raw corpus.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT
DEFAULT_OUTPUT = ROOT / "graph" / "out"


CONTROL_AREAS = [
    ("governance", "Governance", ["program", "policy", "leadership", "oversight"]),
    ("vendor_risk", "Third-Party Risk Management", ["vendor", "subcontractor", "third-party"]),
    ("security_training", "Security Awareness Training", ["training", "awareness", "onboarding"]),
    ("privacy", "Privacy", ["privacy", "personal data", "dpa", "pii", "phi"]),
    ("data_storage", "Customer Data Storage", ["customer data", "aws", "rds", "s3", "dynamodb", "data center"]),
    ("encryption_at_rest", "Encryption At Rest", ["at rest", "aes-256", "kms", "encrypted at rest"]),
    ("encryption_in_transit", "Encryption In Transit", ["in transit", "tls", "https"]),
    ("physical_security", "Physical Security", ["physical", "office", "data center", "visitor"]),
    ("web_app_security", "Web Application Security", ["web application", "ssl", "tls certificate", "authentication"]),
    ("secure_coding", "Secure Coding", ["secure development", "code review", "sdlc", "branch protection"]),
    ("vulnerability_management", "Vulnerability Management", ["vulnerability", "scan", "vapt", "patch"]),
    ("backup_recovery", "Backup And Recovery", ["backup", "snapshot", "rpo", "rto", "restore"]),
    ("incident_response", "Incident Response", ["incident", "breach", "security event", "notification"]),
    ("network_security", "Network And Endpoint Security", ["network", "endpoint", "firewall", "waf", "vpn"]),
    ("asset_management", "Asset Management", ["asset", "inventory", "software", "hardware"]),
    ("access_control", "Access Control", ["access", "rbac", "least privilege", "review"]),
    ("mfa", "MFA", ["mfa", "multi-factor", "2fa", "otp", "replay-resistant"]),
    ("production_access", "Production Access", ["production access", "aws production", "admin", "bastion"]),
    ("offboarding", "Offboarding", ["offboarding", "termination", "revocation", "deprovision"]),
    ("legal_identity", "Legal Identity", ["w-9", "legal name", "dba", "entity"]),
    ("logging_monitoring", "Logging And Monitoring", ["logging", "siem", "cloudwatch", "audit trail"]),
]


QUESTION_RANGES = [
    (1, 5, ["governance"]),
    (6, 10, ["vendor_risk"]),
    (11, 13, ["security_training"]),
    (14, 18, ["privacy"]),
    (19, 24, ["data_storage", "encryption_at_rest", "encryption_in_transit"]),
    (25, 29, ["physical_security"]),
    (30, 35, ["web_app_security"]),
    (36, 37, ["secure_coding"]),
    (38, 40, ["vulnerability_management"]),
    (41, 42, ["backup_recovery"]),
    (43, 49, ["incident_response", "logging_monitoring"]),
    (50, 54, ["network_security", "production_access"]),
    (55, 62, ["asset_management", "access_control", "mfa"]),
    (63, 66, ["governance", "vulnerability_management"]),
]


UNKNOWN_QUESTIONS = {
    "3.0": "No public information security policy URL or copy is present.",
    "6.0": "Engagement-specific contractor/subcontractor usage is not confirmed.",
    "15.0": "Engagement-specific sensitive data access is not confirmed.",
    "26.0": "Physical access to Client XYZ locations is not confirmed.",
    "27.0": "Acceptance of Client XYZ visitor-management terms is not confirmed.",
    "28.0": "Asset tracking for assets brought onto Client XYZ sites is not confirmed.",
    "35.0": "Customer-facing SSO offering and implementation date are not confirmed.",
    "44.0": "Wireless network monitoring is not confirmed.",
    "46.0": "Incident response test cadence is not confirmed.",
    "48.0": "Security events in the last five years are not confirmed.",
    "49.0": "Outsourced security function usage is not confirmed.",
    "50.0": "Antivirus/EDR product coverage is not fully confirmed.",
    "51.0": "Client XYZ network access is not confirmed.",
    "52.0": "The questionnaire source contains a malformed Q52 entry.",
    "53.0": "Client XYZ-specific authorized personnel list is not present.",
    "61.0": "NIST compliance of external authenticators is not explicitly confirmed.",
}


CONFLICT_QUESTIONS = {
    "19.0": ["CONFLICT-001"],
    "22.0": ["CONFLICT-001"],
    "24.0": ["CONFLICT-002"],
    "36.0": ["CONFLICT-006"],
    "37.0": ["CONFLICT-006"],
    "41.0": ["CONFLICT-001"],
    "43.0": ["CONFLICT-002"],
    "53.0": ["CONFLICT-004"],
    "58.0": ["CONFLICT-004"],
    "59.0": ["CONFLICT-004"],
    "66.0": ["CONFLICT-007"],
}


CLAIM_SEEDS = [
    {
        "id": "claim:mfa:core_systems",
        "subject": "MFA",
        "predicate": "is_enforced_for",
        "object": "core systems, cloud infrastructure consoles, identity/email provider, and source-code platform",
        "control_areas": ["mfa", "access_control", "production_access"],
        "polarity": "positive",
        "confidence": 0.94,
        "terms": ["multi-factor authentication is enforced across all core systems"],
        "source_hint": "access_control_policy",
    },
    {
        "id": "claim:mfa:admin_path",
        "subject": "MFA",
        "predicate": "protects",
        "object": "privileged administrative access through VPN and bastion host",
        "control_areas": ["mfa", "production_access", "network_security"],
        "polarity": "positive",
        "confidence": 0.9,
        "terms": ["mfa-verified login", "vpn gateway", "bastion host"],
    },
    {
        "id": "claim:data:aws_storage",
        "subject": "Customer data",
        "predicate": "is_stored_in",
        "object": "AWS-managed RDS, Redshift, S3, MSK, and related data-tier services",
        "control_areas": ["data_storage"],
        "polarity": "positive",
        "confidence": 0.88,
        "terms": ["Amazon RDS", "Amazon S3", "customer data"],
    },
    {
        "id": "claim:infra:cloud_only_policy",
        "subject": "Infrastructure footprint",
        "predicate": "claims_no_on_premises_servers",
        "object": "company operates no on-premises servers or data centers",
        "control_areas": ["data_storage", "network_security", "backup_recovery"],
        "polarity": "positive",
        "confidence": 0.82,
        "terms": ["operates no on-premises servers or data centers"],
    },
    {
        "id": "claim:infra:on_prem_backup_asset",
        "subject": "Infrastructure footprint",
        "predicate": "observes_on_premises_asset",
        "object": "Dell PowerEdge R740 on-prem backup server in HQ server room",
        "control_areas": ["data_storage", "backup_recovery", "asset_management"],
        "polarity": "conflicting",
        "confidence": 0.92,
        "terms": ["Dell PowerEdge R740", "on-prem backup"],
    },
    {
        "id": "claim:encryption:at_rest",
        "subject": "Sensitive data",
        "predicate": "is_encrypted_at_rest_with",
        "object": "AES-256 and AWS-managed encryption keys",
        "control_areas": ["encryption_at_rest", "data_storage"],
        "polarity": "positive",
        "confidence": 0.95,
        "terms": ["encrypted at rest using AES-256"],
    },
    {
        "id": "claim:encryption:in_transit",
        "subject": "Sensitive data",
        "predicate": "is_encrypted_in_transit_with",
        "object": "TLS 1.3, with TLS 1.2 allowed only where a required system lacks TLS 1.3 support",
        "control_areas": ["encryption_in_transit", "network_security"],
        "polarity": "positive",
        "confidence": 0.92,
        "terms": ["TLS 1.3", "TLS 1.2 permitted"],
    },
    {
        "id": "claim:backup:daily_automated",
        "subject": "Production databases",
        "predicate": "use",
        "object": "automated daily backups with point-in-time recovery and rolling 35-day database backup window",
        "control_areas": ["backup_recovery"],
        "polarity": "positive",
        "confidence": 0.9,
        "terms": ["Automated daily backups", "Rolling 35 days"],
    },
    {
        "id": "claim:backup:no_restore_test",
        "subject": "Restore testing",
        "predicate": "has_not_yet_been_performed",
        "object": "restore or recovery test",
        "control_areas": ["backup_recovery"],
        "polarity": "gap",
        "confidence": 0.84,
        "terms": ["no restore", "recovery test"],
    },
    {
        "id": "claim:vuln:annual_testing",
        "subject": "Vulnerability testing",
        "predicate": "is_commissioned_at_least",
        "object": "annually and after major product or infrastructure changes",
        "control_areas": ["vulnerability_management"],
        "polarity": "positive",
        "confidence": 0.88,
        "terms": ["commissioned at least annually"],
    },
    {
        "id": "claim:vuln:sla",
        "subject": "Vulnerability remediation",
        "predicate": "uses_sla",
        "object": "Critical within 7 days, High within 30 days, Medium within 90 days, Low best effort",
        "control_areas": ["vulnerability_management"],
        "polarity": "positive",
        "confidence": 0.9,
        "terms": ["Critical | Within 7 days", "High | Within 30 days"],
    },
    {
        "id": "claim:prod_access:restricted",
        "subject": "Production access",
        "predicate": "is_restricted_to",
        "object": "CTO standing access and need-based temporary grants approved by leadership",
        "control_areas": ["production_access", "access_control"],
        "polarity": "positive",
        "confidence": 0.86,
        "terms": ["Standing production access is limited to the Chief Technology Officer"],
    },
    {
        "id": "claim:prod_access:review_actions",
        "subject": "AWS production access review",
        "predicate": "observes_unjustified_access",
        "object": "S. Wong revoke, T. Nguyen change to Viewer, M. Delgado revoke access",
        "control_areas": ["production_access", "access_control", "offboarding"],
        "polarity": "conflicting",
        "confidence": 0.96,
        "terms": ["Revoke access", "M. Delgado"],
    },
    {
        "id": "claim:offboarding:prompt_revocation",
        "subject": "Offboarding",
        "predicate": "requires",
        "object": "prompt access revocation through internal channel with CTO accountable for completion",
        "control_areas": ["offboarding", "access_control"],
        "polarity": "positive",
        "confidence": 0.9,
        "terms": ["On termination or offboarding, access is revoked promptly"],
    },
    {
        "id": "claim:logging:no_dedicated_siem",
        "subject": "Logging",
        "predicate": "does_not_currently_use",
        "object": "dedicated SIEM; centralized log analytics is planned",
        "control_areas": ["logging_monitoring", "network_security"],
        "polarity": "negative",
        "confidence": 0.88,
        "terms": ["does not currently operate a dedicated SIEM"],
    },
    {
        "id": "claim:logging:diagram_siem",
        "subject": "Logging diagram",
        "predicate": "depicts",
        "object": "centralized SIEM, alerting, and retention",
        "control_areas": ["logging_monitoring", "network_security"],
        "polarity": "conflicting",
        "confidence": 0.75,
        "terms": ["Centralized logging", "SIEM"],
    },
    {
        "id": "claim:hr:background_checks",
        "subject": "Personnel",
        "predicate": "undergo",
        "object": "background checks through a third-party verification provider",
        "control_areas": ["governance", "security_training"],
        "polarity": "positive",
        "confidence": 0.86,
        "terms": ["Background checks are conducted for all personnel"],
    },
    {
        "id": "claim:sdlc:template",
        "subject": "Standalone SDLC document",
        "predicate": "is_template_with_placeholders",
        "object": "unexecuted template language requiring company-specific completion",
        "control_areas": ["secure_coding"],
        "polarity": "gap",
        "confidence": 0.92,
        "terms": ["Regodit policy template instructions", "<Company Name>"],
    },
    {
        "id": "claim:sdlc:live_controls",
        "subject": "Development controls",
        "predicate": "require",
        "object": "GitHub pull-request peer review and production deployment approvals",
        "control_areas": ["secure_coding", "web_app_security"],
        "polarity": "positive",
        "confidence": 0.88,
        "terms": ["pull-request peer reviews", "production deployment"],
    },
    {
        "id": "claim:legal:solsphere_dba_regodit",
        "subject": "Legal identity",
        "predicate": "is",
        "object": "Solsphere AI Inc (dba Regodit)",
        "control_areas": ["legal_identity", "governance"],
        "polarity": "positive",
        "confidence": 0.9,
        "terms": ["Solsphere AI Inc", "dba Regodit"],
    },
]


FINDING_SEEDS = [
    {
        "id": "finding:vapt:summary",
        "title": "VAPT discovered 20 vulnerabilities",
        "severity": "HIGH",
        "finding_type": "vapt_summary",
        "description": "Latest VAPT identified 20 vulnerabilities across web apps, APIs, AI chatbot, XSS, sensitive URL parameters, token lifetime, dependency, and header issues.",
        "control_areas": ["vulnerability_management", "web_app_security"],
        "terms": ["Twenty distinct vulnerabilities were discovered"],
    },
    {
        "id": "finding:vapt:missing_auth",
        "title": "Missing authentication throughout the application",
        "severity": "HIGH",
        "cvss": "8.1",
        "finding_type": "vapt_vulnerability",
        "description": "Application endpoints and functionality can be accessed without verifying identity.",
        "control_areas": ["web_app_security", "access_control"],
        "terms": ["001: Missing Authentication", "CVSS Score: 8.1"],
    },
    {
        "id": "finding:vapt:prompt_injection",
        "title": "AI chatbot security control bypass via prompt manipulation",
        "severity": "MEDIUM",
        "cvss": "6.5",
        "finding_type": "vapt_vulnerability",
        "description": "Prompt manipulation can bypass intended restrictions and may expose sensitive information or unauthorized functionality.",
        "control_areas": ["web_app_security", "vulnerability_management"],
        "terms": ["LLM01", "CVSS Score: 6.5"],
    },
]


OBLIGATION_RULES = [
    ("obligation:confidentiality", "Confidentiality obligations", ["Confidentiality"], ["privacy", "data_storage"]),
    ("obligation:breach_notice", "Breach or security incident notification", ["breach", "notify"], ["incident_response"]),
    ("obligation:data_return", "Secure data return or export", ["download or export file", "Company Data"], ["privacy", "data_storage"]),
    ("obligation:data_deletion", "Data deletion or destruction", ["delete", "destroy"], ["privacy", "data_storage"]),
    ("obligation:security_standards", "Industry security practice requirements", ["industry best practices", "encryption", "firewalls"], ["governance", "encryption_at_rest"]),
    ("obligation:termination", "Termination and transition obligations", ["Termination"], ["vendor_risk", "privacy"]),
]


def main() -> None:
    args = parse_args()
    graph = SecurityGraphBuilder(args.corpus, args.external_facts)
    payload = graph.build()
    write_outputs(payload, args.output)
    print_summary(payload, args.output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build security enrichment graph artifacts")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--external-facts",
        type=Path,
        default=None,
        help="Optional Tavily result JSON file; stored as isolated ExternalFact nodes.",
    )
    return parser.parse_args()


class SecurityGraphBuilder:
    def __init__(self, corpus_root: Path, external_facts_path: Path | None) -> None:
        self.corpus_root = corpus_root
        self.external_facts_path = external_facts_path
        self.nodes: dict[str, dict[str, Any]] = {}
        self.relationships: list[dict[str, Any]] = []
        self.relationship_keys: set[tuple[str, str, str]] = set()
        self.blocks: list[dict[str, Any]] = []
        self.blocks_by_text: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.source_to_blocks: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.claims_by_area: dict[str, list[str]] = defaultdict(list)
        self.conflicts_by_area: dict[str, list[str]] = defaultdict(list)
        self.action_items_by_area: dict[str, list[str]] = defaultdict(list)
        self.index = load_json(corpus_root / "corpus_text/00_INDEX/master_corpus_index.json")
        self.manifest = load_json(corpus_root / "evidence/source_manifest.json")
        self.questionnaire = load_json(corpus_root / "evidence/questionnaire.json")
        self.documents_by_source = {
            document["source"]: document for document in self.index.get("documents", [])
        }

    def build(self) -> dict[str, Any]:
        self.load_markdown_blocks()
        self.add_control_areas()
        self.add_sources_and_document_controls()
        self.add_evidence_blocks()
        self.add_seed_claims()
        self.add_assessment_findings()
        self.add_contract_obligations()
        self.add_conflicts()
        self.add_questionnaire_questions()
        self.add_external_facts()
        return {
            "metadata": self.metadata(),
            "nodes": list(self.nodes.values()),
            "relationships": self.relationships,
        }

    def metadata(self) -> dict[str, Any]:
        node_counts = Counter()
        for node in self.nodes.values():
            for label in node["labels"]:
                node_counts[label] += 1
        rel_counts = Counter(rel["type"] for rel in self.relationships)
        decision_counts = Counter(
            node["properties"].get("decision_state")
            for node in self.nodes.values()
            if "QuestionnaireQuestion" in node["labels"]
        )
        return {
            "corpus_title": self.index.get("corpus_title"),
            "generated_from": self.corpus_root.as_posix(),
            "source_count": len(self.manifest["sources"]),
            "curated_document_count": len(self.index.get("documents", [])),
            "question_count": len(self.questionnaire["questions"]),
            "node_counts": dict(sorted(node_counts.items())),
            "relationship_counts": dict(sorted(rel_counts.items())),
            "decision_counts": dict(sorted(decision_counts.items())),
            "external_fact_policy": "Tavily results are stored only as ExternalFact nodes and never overwrite internal claims.",
        }

    def load_markdown_blocks(self) -> None:
        for path in sorted((self.corpus_root / "corpus_text").rglob("*.md")):
            self.blocks.extend(parse_markdown_blocks(path, self.corpus_root))
        for block in self.blocks:
            self.blocks_by_text[normalize(block["text"])].append(block)
            self.source_to_blocks[block["source"]].append(block)

    def add_control_areas(self) -> None:
        for area_id, name, keywords in CONTROL_AREAS:
            self.add_node(
                "control:" + area_id,
                ["ControlArea"],
                {"id": "control:" + area_id, "key": area_id, "name": name, "keywords": keywords},
            )

    def add_sources_and_document_controls(self) -> None:
        for source in self.manifest["sources"]:
            source_path = source["path"]
            document = self.documents_by_source.get(source_path, {})
            authority = authority_class(source_path, document)
            props = {
                "id": source_id(source_path),
                "path": source_path,
                "sha256": source["sha256"],
                "format": source["format"],
                "bytes": source["bytes"],
                "folder_category": folder_category(source_path),
                "authority_class": authority,
                "title": document.get("title") or Path(source_path).stem.replace("_", " "),
                "document_class": document.get("class", ""),
                "summary": document.get("summary", ""),
                "curated_relative_path": document.get("relative_path", ""),
                "topics_covered": document.get("topics_covered", []),
            }
            self.add_node(source_id(source_path), ["Source"], props)

        for document in self.index.get("documents", []):
            source_path = document["source"]
            if not source_path.startswith("Hackathon/"):
                continue
            fields = self.extract_document_control(source_path)
            has_placeholders = has_placeholder_text(self.source_to_blocks.get(source_path, []), document)
            dc_id = stable_id("docctl", source_path)
            self.add_node(
                dc_id,
                ["DocumentControl"],
                {
                    "id": dc_id,
                    "source_path": source_path,
                    "title": fields.get("Document Title") or document.get("title", ""),
                    "owner": fields.get("Document Owner") or fields.get("Policy owner") or "",
                    "approver": fields.get("Approved By") or fields.get("Approver") or "",
                    "version": fields.get("Version") or "",
                    "effective_date": fields.get("Effective Date") or fields.get("Effective date") or "",
                    "review_cycle": fields.get("Review Cycle") or fields.get("Review frequency") or "",
                    "classification": fields.get("Classification") or "",
                    "applies_to": fields.get("Applies To") or "",
                    "placeholder_status": "has_placeholders" if has_placeholders else "complete_or_not_detected",
                    "authority_class": authority_class(source_path, document),
                },
            )
            self.add_relationship(dc_id, "DOCUMENT_CONTROL_FOR", source_id(source_path))
            if has_placeholders:
                action_id = stable_id("action", source_path, "metadata_placeholder")
                self.add_action_item(
                    action_id,
                    "Complete placeholder or unsigned document metadata",
                    "MEDIUM",
                    "Document contains placeholders, unsigned status, or template language that needs owner confirmation.",
                    ["governance"],
                )
                self.add_relationship(dc_id, "REQUIRES", action_id)

    def extract_document_control(self, source_path: str) -> dict[str, str]:
        blocks = self.source_to_blocks.get(source_path, [])
        fields = {}
        field_names = {
            "Document Title",
            "Document Owner",
            "Approved By",
            "Classification",
            "Effective Date",
            "Review Cycle",
            "Applies To",
            "Policy owner",
            "Approver",
            "Version",
            "Effective date",
            "Review frequency",
        }
        for idx, block in enumerate(blocks[:-1]):
            text = block["text"].strip()
            if text in field_names:
                fields[text] = blocks[idx + 1]["text"].strip()
        return fields

    def add_evidence_blocks(self) -> None:
        for block in self.blocks:
            if not block["source"].startswith("Hackathon/"):
                continue
            evidence_id = evidence_id_for(block["id"])
            self.add_node(
                evidence_id,
                ["EvidenceBlock"],
                {
                    "id": evidence_id,
                    "evidence_key": block["id"],
                    "source_path": block["source"],
                    "locator": block["locator"],
                    "quote": block["text"],
                    "quote_sha256": sha256(block["text"]),
                    "markdown_path": block["markdown_path"],
                    "position": block.get("position", ""),
                    "source_authority_class": authority_class(
                        block["source"], self.documents_by_source.get(block["source"], {})
                    ),
                },
            )
            self.add_relationship(evidence_id, "FROM_SOURCE", source_id(block["source"]))

    def add_seed_claims(self) -> None:
        for seed in CLAIM_SEEDS:
            evidence_blocks = self.find_evidence(seed["terms"], seed.get("source_hint"))
            claim_id = seed["id"]
            self.add_node(
                claim_id,
                ["Claim"],
                {
                    "id": claim_id,
                    "subject": seed["subject"],
                    "predicate": seed["predicate"],
                    "object": seed["object"],
                    "polarity": seed["polarity"],
                    "confidence": seed["confidence"],
                    "authority_class": dominant_authority(evidence_blocks),
                    "answer_text": f'{seed["subject"]} {seed["predicate"].replace("_", " ")} {seed["object"]}.',
                    "evidence_count": len(evidence_blocks),
                },
            )
            for area in seed["control_areas"]:
                self.link_claim_to_area(claim_id, area)
            for block in evidence_blocks:
                self.add_relationship(claim_id, "SUPPORTED_BY", evidence_id_for(block["id"]))

    def find_evidence(self, terms: list[str], source_hint: str | None = None, limit: int = 8) -> list[dict[str, Any]]:
        scored = []
        lowered_terms = [normalize(term) for term in terms]
        for block in self.blocks:
            if source_hint and source_hint not in normalize(block["markdown_path"] + " " + block["source"]):
                continue
            haystack = normalize(block["text"])
            score = sum(1 for term in lowered_terms if term and term in haystack)
            if score:
                scored.append((score, len(block["text"]), block))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return [block for _, _, block in scored[:limit]]

    def link_claim_to_area(self, claim_id: str, area: str) -> None:
        area_id = "control:" + area
        if area_id in self.nodes:
            self.claims_by_area[area].append(claim_id)
            self.add_relationship(claim_id, "MAPS_TO", area_id)

    def add_assessment_findings(self) -> None:
        for seed in FINDING_SEEDS:
            evidence_blocks = self.find_evidence(seed["terms"], limit=5)
            self.add_node(
                seed["id"],
                ["AssessmentFinding"],
                {
                    "id": seed["id"],
                    "title": seed["title"],
                    "severity": seed["severity"],
                    "cvss": seed.get("cvss", ""),
                    "finding_type": seed["finding_type"],
                    "description": seed["description"],
                    "source_authority_class": "assessment_report",
                    "remediation_status": "needs_confirmation",
                },
            )
            for area in seed["control_areas"]:
                self.add_relationship(seed["id"], "VIOLATES_OR_WEAKENS", "control:" + area)
            for block in evidence_blocks:
                self.add_relationship(seed["id"], "SUPPORTED_BY", evidence_id_for(block["id"]))

    def add_contract_obligations(self) -> None:
        contract_blocks = [
            block
            for block in self.blocks
            if "/04_CONTRACTS_AGREEMENTS/" in block["markdown_path"]
            or "4. Contracts_agreements" in block["source"]
        ]
        for obligation_id, title, terms, areas in OBLIGATION_RULES:
            evidence_blocks = [
                block
                for block in contract_blocks
                if all(normalize(term) in normalize(block["text"]) for term in terms[:1])
            ][:6]
            if not evidence_blocks:
                continue
            self.add_node(
                obligation_id,
                ["ContractObligation"],
                {
                    "id": obligation_id,
                    "title": title,
                    "obligation_type": obligation_id.split(":", 1)[1],
                    "description": evidence_blocks[0]["text"][:700],
                    "authority_class": "contract_obligation",
                },
            )
            for area in areas:
                self.add_relationship(obligation_id, "REQUIRES_CONTROL", "control:" + area)
            for block in evidence_blocks:
                self.add_relationship(obligation_id, "SUPPORTED_BY", evidence_id_for(block["id"]))

    def add_conflicts(self) -> None:
        for conflict in self.index.get("contradictions_and_investigation_playbook", []):
            conflict_id = conflict["id"]
            areas = infer_areas(conflict["topic"] + " " + conflict["description"])
            self.add_node(
                conflict_id,
                ["Conflict"],
                {
                    "id": conflict_id,
                    "topic": conflict["topic"],
                    "severity": conflict["severity"],
                    "description": conflict["description"],
                    "status": "unresolved",
                    "agent_guidance": conflict["agent_guidance"],
                },
            )
            for area in areas:
                self.conflicts_by_area[area].append(conflict_id)
            claim_a = stable_id("claim", conflict_id, "a")
            claim_b = stable_id("claim", conflict_id, "b")
            for claim_id, side in [(claim_a, "evidence_a"), (claim_b, "evidence_b")]:
                text = conflict.get(side, "")
                self.add_node(
                    claim_id,
                    ["Claim"],
                    {
                        "id": claim_id,
                        "subject": conflict["topic"],
                        "predicate": "conflict_side",
                        "object": text,
                        "polarity": "conflicting",
                        "confidence": 0.8,
                        "authority_class": "mixed",
                        "answer_text": text,
                    },
                )
                for area in areas:
                    self.link_claim_to_area(claim_id, area)
                for block in self.find_evidence(extract_search_terms(text), limit=4):
                    self.add_relationship(claim_id, "SUPPORTED_BY", evidence_id_for(block["id"]))
                self.add_relationship(conflict_id, "INVOLVES", claim_id)
            self.add_relationship(claim_a, "CONTRADICTS", claim_b)
            self.add_relationship(claim_b, "CONTRADICTS", claim_a)
            action_id = stable_id("action", conflict_id)
            self.add_action_item(
                action_id,
                f"Resolve {conflict['topic']}",
                conflict["severity"],
                conflict["agent_guidance"],
                areas,
            )
            self.add_relationship(conflict_id, "REQUIRES", action_id)

    def add_questionnaire_questions(self) -> None:
        for question in self.questionnaire["questions"]:
            qid = question["id"]
            areas = question_control_areas(qid, question["question"])
            decision_state, reason = self.question_decision(qid, areas)
            question_id = "question:" + qid
            self.add_node(
                question_id,
                ["QuestionnaireQuestion"],
                {
                    "id": question_id,
                    "question_id": qid,
                    "row": question["row"],
                    "source_cell": question["source_cell"],
                    "question": question["question"],
                    "existing_response": question.get("existing_response", ""),
                    "additional_info": question.get("additional_info", ""),
                    "wording_status": question.get("wording_status", ""),
                    "decision_state": decision_state,
                    "decision_reason": reason,
                    "mapped_control_areas": areas,
                    "source_file": self.questionnaire["source_file"],
                    "source_sheet": self.questionnaire["source_sheet"],
                },
            )
            for area in areas:
                self.add_relationship(question_id, "ASKS_ABOUT", "control:" + area)
                for claim_id in self.claims_by_area.get(area, [])[:8]:
                    self.add_relationship(claim_id, "ANSWERS", question_id)
            if decision_state in {"ASK_USER", "UNKNOWN", "ANSWER_WITH_CONFLICT", "ESCALATE"}:
                action_id = stable_id("action", "question", qid)
                self.add_action_item(
                    action_id,
                    f"Confirm questionnaire item {qid}",
                    "HIGH" if decision_state in {"ANSWER_WITH_CONFLICT", "ESCALATE"} else "MEDIUM",
                    reason,
                    areas,
                )
                self.add_relationship(question_id, "REQUIRES", action_id)
            for conflict_id in CONFLICT_QUESTIONS.get(qid, []):
                if conflict_id in self.nodes:
                    self.add_relationship(question_id, "HAS_CONFLICT", conflict_id)

    def question_decision(self, qid: str, areas: list[str]) -> tuple[str, str]:
        if qid == "66.0":
            return (
                "ANSWER_WITH_CONFLICT",
                "Latest VAPT has findings, but completion of remediation is not evidenced and requires engineering confirmation.",
            )
        if qid in CONFLICT_QUESTIONS:
            return (
                "ANSWER_WITH_CONFLICT",
                "Question maps to an indexed conflict; answer must disclose the conflict and request clarification.",
            )
        if qid in UNKNOWN_QUESTIONS:
            return ("ASK_USER", UNKNOWN_QUESTIONS[qid])
        if not any(self.claims_by_area.get(area) for area in areas):
            return ("UNKNOWN", "No internal claim currently supports a complete answer.")
        return ("ANSWER_VERIFIED", "Internal evidence supports an answer with citations.")

    def add_external_facts(self) -> None:
        if not self.external_facts_path or not self.external_facts_path.exists():
            return
        payload = load_json(self.external_facts_path)
        facts = payload if isinstance(payload, list) else payload.get("facts", [])
        for fact in facts:
            fact_id = fact.get("id") or stable_id("external", fact.get("url", ""), fact.get("title", ""))
            node_id = "external:" + fact_id
            props = {
                "id": node_id,
                "provider": "tavily",
                "source": "external",
                "external_use_case": fact.get("external_use_case", ""),
                "title": fact.get("title", ""),
                "url": fact.get("url", ""),
                "retrieved_at": fact.get("retrieved_at", ""),
                "summary": fact.get("summary", ""),
                "query": fact.get("query", ""),
                "result_rank": fact.get("result_rank", ""),
                "score": fact.get("score", ""),
                "target_type": fact.get("target_type", ""),
                "domain_filter": fact.get("domain_filter", []),
                "isolation_rule": "supplement_only_never_override_internal_evidence",
            }
            self.add_node(node_id, ["ExternalFact"], props)
            target = fact.get("supplements")
            if target and target in self.nodes:
                self.add_relationship(node_id, "SUPPLEMENTS", target)

    def add_action_item(
        self, action_id: str, title: str, severity: str, description: str, areas: list[str]
    ) -> None:
        self.add_node(
            action_id,
            ["ActionItem"],
            {
                "id": action_id,
                "title": title,
                "severity": severity,
                "description": description,
                "status": "open",
                "mapped_control_areas": areas,
            },
        )
        for area in areas:
            self.action_items_by_area[area].append(action_id)
            if "control:" + area in self.nodes:
                self.add_relationship(action_id, "MAPS_TO", "control:" + area)

    def add_node(self, node_id: str, labels: list[str], properties: dict[str, Any]) -> None:
        current = self.nodes.get(node_id)
        if current:
            current["labels"] = sorted(set(current["labels"]) | set(labels))
            current["properties"].update(properties)
            return
        properties = sanitize_props({**properties, "id": node_id})
        self.nodes[node_id] = {"id": node_id, "labels": sorted(set(labels)), "properties": properties}

    def add_relationship(
        self, start_id: str, rel_type: str, end_id: str, properties: dict[str, Any] | None = None
    ) -> None:
        if start_id not in self.nodes or end_id not in self.nodes:
            return
        key = (start_id, rel_type, end_id)
        if key in self.relationship_keys:
            return
        self.relationship_keys.add(key)
        self.relationships.append(
            {
                "start": start_id,
                "type": rel_type,
                "end": end_id,
                "properties": sanitize_props(properties or {}),
            }
        )


def parse_markdown_blocks(path: Path, corpus_root: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    source_match = re.search(r"^Source:\s+`([^`]+)`", text, re.M)
    source = source_match.group(1) if source_match else ""
    blocks = []
    pattern = re.compile(r"<!-- evidence:([a-f0-9]+) source:([^>]+)-->\n", re.I)
    matches = list(pattern.finditer(text))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        raw_body = text[start:end].strip()
        body_lines = []
        for line in raw_body.splitlines():
            if line.startswith("Source hyperlinks:") or line.startswith("Source cell comment:"):
                break
            body_lines.append(line)
        quote = "\n".join(body_lines).strip()
        if not quote:
            continue
        locator = match.group(2).strip()
        blocks.append(
            {
                "id": match.group(1),
                "source": source,
                "locator": locator,
                "text": quote,
                "markdown_path": path.relative_to(corpus_root).as_posix(),
                "position": f"block:{index + 1}",
            }
        )
    return blocks


def write_outputs(payload: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    graph_json = output_dir / "security_graph.json"
    graph_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    write_jsonl(output_dir / "nodes.jsonl", payload["nodes"])
    write_jsonl(output_dir / "relationships.jsonl", payload["relationships"])
    write_csv(output_dir / "nodes.csv", payload["nodes"], ["id", "labels", "properties"])
    write_csv(output_dir / "relationships.csv", payload["relationships"], ["start", "type", "end", "properties"])
    (output_dir / "neo4j_import.cypher").write_text(generate_cypher(payload), encoding="utf-8")
    (output_dir / "README.md").write_text(output_readme(payload), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def generate_cypher(payload: dict[str, Any]) -> str:
    lines = [
        "// Neo4j import for PrismAccess security enrichment graph",
        "// Generated from cleaned corpus. External facts are supplement-only.",
        "CREATE CONSTRAINT prism_node_id IF NOT EXISTS FOR (n:GraphNode) REQUIRE n.id IS UNIQUE;",
        "",
    ]
    for node in payload["nodes"]:
        labels = ":".join(["GraphNode"] + [safe_label(label) for label in node["labels"]])
        lines.append(f"MERGE (n:{labels} {{id: {cypher_value(node['id'])}}})")
        assignments = []
        for key, value in sorted(node["properties"].items()):
            assignments.append(f"n.{cypher_prop(key)} = {cypher_value(value)}")
        lines.append("SET " + ", ".join(assignments) + ";")
    lines.append("")
    for rel in payload["relationships"]:
        lines.append(f"MATCH (a:GraphNode {{id: {cypher_value(rel['start'])}}})")
        lines.append(f"MATCH (b:GraphNode {{id: {cypher_value(rel['end'])}}})")
        lines.append(f"MERGE (a)-[r:{safe_rel_type(rel['type'])}]->(b)")
        if rel["properties"]:
            assignments = [
                f"r.{cypher_prop(key)} = {cypher_value(value)}"
                for key, value in sorted(rel["properties"].items())
            ]
            lines.append("SET " + ", ".join(assignments) + ";")
        else:
            lines[-1] += ";"
    return "\n".join(lines) + "\n"


def output_readme(payload: dict[str, Any]) -> str:
    meta = payload["metadata"]
    return f"""# Security Graph Output

Generated artifacts for importing the enriched security corpus into Neo4j.

## Files

- `security_graph.json`: portable graph payload with nodes, relationships, and metadata.
- `nodes.jsonl` / `relationships.jsonl`: line-delimited graph records for agents and tests.
- `nodes.csv` / `relationships.csv`: compact interchange files.
- `neo4j_import.cypher`: self-contained Cypher import script. Run it in `cypher-shell` or Neo4j Browser.

## Counts

- Sources: {meta["source_count"]}
- Curated documents: {meta["curated_document_count"]}
- Questionnaire questions: {meta["question_count"]}
- Nodes: {len(payload["nodes"])}
- Relationships: {len(payload["relationships"])}

## External Data Rule

Tavily results are optional and must be loaded as `ExternalFact` nodes only. They may `SUPPLEMENTS` internal claims, findings, or obligations, but must not overwrite internal `Claim` or `EvidenceBlock` records.
"""


def print_summary(payload: dict[str, Any], output_dir: Path) -> None:
    meta = payload["metadata"]
    print(f"Wrote security graph to {output_dir}")
    print(f"Sources: {meta['source_count']}")
    print(f"Curated docs: {meta['curated_document_count']}")
    print(f"Questionnaire questions: {meta['question_count']}")
    print(f"Nodes: {len(payload['nodes'])}")
    print(f"Relationships: {len(payload['relationships'])}")
    print(f"Decision counts: {meta['decision_counts']}")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def source_id(path: str) -> str:
    return "source:" + path


def evidence_id_for(key: str) -> str:
    return "evidence:" + key


def stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{digest}"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize(value: Any) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", str(value).lower())).strip()


def folder_category(path: str) -> str:
    parts = Path(path).parts
    if len(parts) >= 2 and parts[0] == "Hackathon":
        return parts[1]
    return parts[0] if parts else ""


def authority_class(source_path: str, document: dict[str, Any]) -> str:
    haystack = normalize(" ".join([source_path, document.get("class", ""), document.get("title", "")]))
    if "access review" in haystack or "asset inventory" in haystack or "bcp dr plan" in haystack:
        return "operational_record"
    if "vapt" in haystack or "soc2" in haystack or "soc 2" in haystack or "assessment report" in haystack:
        return "assessment_report"
    if "contracts agreements" in haystack or "agreement" in haystack or "contract" in haystack:
        return "contract_obligation"
    if "diagram" in haystack or source_path.endswith(".png"):
        return "diagram_reference"
    if "template" in haystack or "w 9" in haystack or "unsigned" in haystack:
        return "template_or_draft"
    if "company policies" in haystack:
        if "modify" in haystack or "incomplete" in haystack:
            return "policy_with_incomplete_metadata"
        return "adopted_policy"
    return "source_document"


def has_placeholder_text(blocks: list[dict[str, Any]], document: dict[str, Any]) -> bool:
    text = normalize(" ".join([document.get("summary", ""), document.get("class", "")]))
    raw = "\n".join(block["text"] for block in blocks[:120])
    return any(token in raw for token in ["[MODIFY", "<Company Name>", "<Policy owner>", "To be completed"]) or any(
        phrase in text for phrase in ["template", "unsigned", "incomplete"]
    )


def dominant_authority(blocks: list[dict[str, Any]]) -> str:
    if not blocks:
        return "unmapped"
    counts = Counter(
        authority_class(block["source"], {}) for block in blocks if block.get("source", "").startswith("Hackathon/")
    )
    if not counts:
        return "unmapped"
    return counts.most_common(1)[0][0]


def infer_areas(text: str) -> list[str]:
    normalized = normalize(text)
    areas = []
    for area_id, _name, keywords in CONTROL_AREAS:
        if any(normalize(keyword) in normalized for keyword in keywords):
            areas.append(area_id)
    if not areas:
        areas = ["governance"]
    return areas


def extract_search_terms(text: str) -> list[str]:
    quoted = re.findall(r"'([^']{8,120})'", text)
    if quoted:
        return quoted[:3]
    words = [word for word in re.findall(r"[A-Za-z][A-Za-z0-9-]{3,}", text) if len(word) > 5]
    return [" ".join(words[:4])] if words else [text[:80]]


def question_control_areas(qid: str, question: str) -> list[str]:
    try:
        number = int(float(qid))
    except ValueError:
        number = 0
    areas: list[str] = []
    for start, end, mapped in QUESTION_RANGES:
        if start <= number <= end:
            areas.extend(mapped)
    areas.extend(infer_areas(question))
    return sorted(set(areas))


def sanitize_props(properties: dict[str, Any]) -> dict[str, Any]:
    clean = {}
    for key, value in properties.items():
        if value is None:
            clean[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            clean[key] = value
        elif isinstance(value, list):
            clean[key] = [str(item) for item in value]
        else:
            clean[key] = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return clean


def csv_value(value: Any) -> str:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return "" if value is None else str(value)


def safe_label(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "", value)


def safe_rel_type(value: str) -> str:
    return re.sub(r"[^A-Z0-9_]", "", value.upper())


def cypher_prop(key: str) -> str:
    return "`" + key.replace("`", "``") + "`"


def cypher_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(cypher_value(str(item)) for item in value) + "]"
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


if __name__ == "__main__":
    main()
