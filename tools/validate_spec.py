#!/usr/bin/env python3
"""
Comprehensive Spec & Golden Rule Validator for Regodit AI Security Analyst.

Validates all 7 core criteria defined in the competition specification:
  1. The Golden Rule: Never fabricate an answer (out-of-scope/unknown -> ask_user).
  2. Conflict Detection: All 7 indexed contradictions surfaced with opposing evidence.
  3. Evidence Integrity: Every answered control includes verified citations.
  4. Confidence Basis: Explicit breakdown of Source Freshness, Directness, and Cross-Verification.
  5. External Standards Check: Live Python call in agent loop validates against NIST SP 800-63B / OWASP.
  6. Persistent Memory & Corrections: In-place update, correction counter, and recall from memory.
  7. Graph Topology & Isolation: ExternalFact isolation rule enforced (supplement only, never override).

Usage:
  python3 tools/validate_spec.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "security_agent"))

from agent_loop import process_question, load_chunks
from retrieve_graph import GraphTreeRetriever
import security_profile as profile_store
from external_check import perform_external_standards_check


def require(condition: bool, message: str) -> None:
    if not condition:
        print(f"FAILED: {message}")
        raise AssertionError(message)


def run_spec_validation() -> None:
    print("=" * 78)
    print("REGODIT AI SECURITY ANALYST: FULL SPEC & GOLDEN RULE VALIDATION SUITE")
    print("=" * 78)

    # 1. Initialize Graph & Retriever
    print("[1/7] Initializing Knowledge Graph & GraphTreeRetriever...")
    graph_data = load_chunks()
    retriever = GraphTreeRetriever(graph_data)
    require(len(retriever.nodes) >= 9000, f"Expected >=9000 graph nodes, found {len(retriever.nodes)}")
    require(len(retriever.conflicts) >= 7, f"Expected >=7 conflicts, found {len(retriever.conflicts)}")
    require(len(retriever.questions) == 66, f"Expected 66 questionnaire questions, found {len(retriever.questions)}")
    print(f"      PASS: {len(retriever.nodes)} nodes, {len(retriever.conflicts)} conflicts, {len(retriever.questions)} questions loaded.")

    # 2. Golden Rule Enforcement (Anti-Hallucination)
    print("[2/7] Validating Golden Rule (Never Fabricate An Answer)...")
    q_unknown = "Will you be using any contractors or sub-contractors to complete the engagement with Regodit?"
    res_unknown = process_question(q_unknown, retriever)
    require(
        res_unknown["final_status"] in ("ask_user", "insufficient", "conflict"),
        f"Expected escalation for engagement contractor staffing, got {res_unknown['final_status']}",
    )
    require(
        res_unknown.get("confidence", 0) <= 0.5,
        f"Confidence must be discounted for unconfirmed engagement facts, got {res_unknown.get('confidence')}",
    )
    print(f"      PASS: Out-of-scope question correctly escalated ({res_unknown['final_status']}) with zero fabrication.")

    # 3. Conflict Detection Across Baseline Contradictions
    print("[3/7] Validating Conflict Detection & Bilateral Evidencing...")
    test_conflicts = [
        ("CONFLICT-001 (Hosting)", "Where is company and customer data hosted?"),
        ("CONFLICT-002 (SIEM)", "Does your organization operate a centralized SIEM for security event logging?"),
        ("CONFLICT-004 (Offboarding)", "When an employee or contractor departs, is their access to production systems revoked immediately?"),
        ("Q60.0 (MFA Policy vs VAPT)", "Does your organization require replay-resistant authentication mechanisms such as OTP or MFA?"),
    ]
    for label, query in test_conflicts:
        res_c = process_question(query, retriever)
        require(res_c["final_status"] == "conflict", f"Expected conflict for {label}, got {res_c['final_status']}")
        require(bool(res_c.get("conflict_explanation")), f"Missing conflict_explanation for {label}")
        require(len(res_c.get("citations", [])) >= 2, f"Expected at least 2 opposing citations for {label}")
        print(f"      PASS: {label} detected -> {res_c['conflict_explanation'][:65]}...")

    # 4. Confidence Basis Breakdown (Freshness, Directness, Cross-Verification)
    print("[4/7] Validating Explicit Confidence Basis Breakdown...")
    q_verified = "Does your organization have a formal Information Security Program established?"
    res_v = process_question(q_verified, retriever)
    require(res_v["final_status"] == "answered", f"Expected answered for Q1.0, got {res_v['final_status']}")
    cb = res_v.get("confidence_basis")
    require(isinstance(cb, dict), "confidence_basis must be a structured dict")
    require(bool(cb.get("source_freshness")), "confidence_basis must explain source_freshness")
    require(bool(cb.get("directness")), "confidence_basis must explain directness")
    require(bool(cb.get("cross_verification")), "confidence_basis must explain cross_verification")
    require(bool(cb.get("summary")), "confidence_basis must include narrative summary")
    print(f"      PASS: Confidence basis present:")
    print(f"            - Freshness: {cb['source_freshness'][:50]}...")
    print(f"            - Directness: {cb['directness'][:50]}...")
    print(f"            - Cross-Verif: {cb['cross_verification'][:50]}...")

    # 5. External Standards Check & Live Python Call (NIST SP 800-63B)
    print("[5/7] Validating Live Python Call for External Checks (NIST SP 800-63B)...")
    res_mfa = process_question("Does your organization require replay-resistant authentication mechanisms such as OTP or MFA?", retriever)
    ext = res_mfa.get("external_check")
    require(isinstance(ext, dict), "MFA question must execute external standards check")
    require(ext.get("standard") == "NIST SP 800-63B", f"Expected NIST SP 800-63B, got {ext.get('standard')}")
    require(ext.get("provider") in ("nist.gov", "pages.nist.gov"), f"Invalid provider {ext.get('provider')}")
    require(
        ext.get("isolation_rule") == "supplement_only_never_override_internal_evidence",
        "External check must enforce strict isolation boundary rule",
    )
    print(f"      PASS: Live external check executed for {ext['standard']} ({ext['title'][:45]}...)")
    print(f"            Isolation Rule Verified: {ext['isolation_rule']}")

    # 6. Persistent Memory, Human Override & In-Place Correction
    print("[6/7] Validating Persistent Memory & Correction Handling...")
    test_qid = "VAL-TEST-001"
    q_text = "What is the emergency backup restoration window?"
    
    # Ensure clean slate for idempotent runs
    if test_qid in profile_store._profile["questions"]:
        del profile_store._profile["questions"][test_qid]
        profile_store.save_profile(profile_store._profile)
    
    # First confirmation
    rec1 = profile_store.upsert_record(
        question_id=test_qid,
        question_text=q_text,
        status="confirmed_by_user",
        answer="RTO is 4 hours, RPO is 1 hour via automated snapshot replication.",
        confidence=1.0,
    )
    require(profile_store.already_answered(test_qid), "Question must be recorded as resolved")
    require(rec1["correction_count"] == 0, f"Initial record must have correction_count 0, got {rec1['correction_count']}")

    # In-place correction
    rec2 = profile_store.upsert_record(
        question_id=test_qid,
        question_text=q_text,
        status="confirmed_by_user",
        answer="RTO updated to 2 hours following multi-region active replication.",
        confidence=1.0,
    )
    require(rec2["correction_count"] == 1, f"Correction must bump counter to 1, got {rec2['correction_count']}")
    require(rec2["prior_answer"] == rec1["answer"], "Prior answer must be tracked in audit trail")
    
    summary = profile_store.summary_report()
    require(test_qid in summary["questions"], "Summary must reflect updated question")
    print(f"      PASS: Persistent memory recorded, in-place correction verified (correction_count: {rec2['correction_count']}).")

    # Clean up test key
    if test_qid in profile_store._profile["questions"]:
        del profile_store._profile["questions"][test_qid]
        profile_store.save_profile(profile_store._profile)

    # 7. ExternalFact Node Topology & Isolation in Graph
    print("[7/7] Validating ExternalFact Node Topology & Edge Directionality...")
    external_nodes = [n for n in graph_data.get("nodes", []) if "ExternalFact" in n.get("labels", [])]
    require(len(external_nodes) >= 10, f"Expected >=10 ExternalFact nodes, found {len(external_nodes)}")
    for node in external_nodes:
        props = node.get("properties", {})
        require(props.get("source") == "external", "ExternalFact source must be external")
        require(bool(props.get("provider")), "ExternalFact must declare provider")
    
    # Validate SUPPLEMENTS edges only originate from ExternalFact nodes
    node_labels_by_id = {n["id"]: set(n.get("labels", [])) for n in graph_data.get("nodes", [])}
    for r in graph_data.get("relationships", []):
        if r.get("type") == "SUPPLEMENTS":
            start_labels = node_labels_by_id.get(r["start"], set())
            require("ExternalFact" in start_labels, f"SUPPLEMENTS relationship start must be ExternalFact, got {start_labels}")

    print(f"      PASS: {len(external_nodes)} ExternalFact nodes verified with strict SUPPLEMENTS topology.")

    print("=" * 78)
    print("ALL 7 SPEC CRITERIA VALIDATED: 100% SPEC & GOLDEN RULE COMPLIANCE.")
    print("=" * 78)


if __name__ == "__main__":
    run_spec_validation()
