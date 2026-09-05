#!/usr/bin/env python3
"""Validate generated security graph artifacts."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GRAPH = ROOT / "graph" / "out" / "security_graph.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate security graph output")
    parser.add_argument("--graph", type=Path, default=DEFAULT_GRAPH)
    args = parser.parse_args()
    payload = json.loads(args.graph.read_text(encoding="utf-8"))
    nodes = payload["nodes"]
    relationships = payload["relationships"]
    by_id = {node["id"]: node for node in nodes}
    counts = Counter(label for node in nodes for label in node["labels"])
    rel_counts = Counter(rel["type"] for rel in relationships)

    require(payload["metadata"]["source_count"] == 26, "expected 26 sources")
    require(payload["metadata"]["curated_document_count"] == 28, "expected 28 curated docs")
    require(payload["metadata"]["question_count"] == 66, "expected 66 questionnaire questions")
    require(counts["Source"] == 26, "Source node count must be 26")
    require(counts["QuestionnaireQuestion"] == 66, "QuestionnaireQuestion count must be 66")
    require(counts["Conflict"] == 7, "Conflict node count must be 7")
    require(counts["ControlArea"] >= 20, "expected full control taxonomy")
    require(counts["EvidenceBlock"] > 100, "expected atomic evidence blocks")
    require(counts["Claim"] >= 20, "expected normalized claims")
    require(counts["AssessmentFinding"] >= 3, "expected assessment findings")
    require(counts["ContractObligation"] >= 3, "expected contract obligations")
    require(counts["ActionItem"] >= 7, "expected conflict/action items")

    require(rel_counts["FROM_SOURCE"] > 100, "evidence must link to source")
    require(rel_counts["SUPPORTED_BY"] > 20, "claims/findings/obligations must cite evidence")
    require(rel_counts["ASKS_ABOUT"] >= 66, "questions must map to controls")
    require(rel_counts["ANSWERS"] > 20, "claims must answer questions")
    require(rel_counts["CONTRADICTS"] >= 14, "known conflicts must link contradictory claims")
    require(rel_counts["REQUIRES"] >= 7, "conflicts/questions must require action")

    for conflict_id in [f"CONFLICT-{idx:03d}" for idx in range(1, 8)]:
        require(conflict_id in by_id, f"missing {conflict_id}")
        require(
            any(rel["start"] == conflict_id and rel["type"] == "REQUIRES" for rel in relationships),
            f"{conflict_id} must require an action",
        )

    q66 = by_id["question:66.0"]["properties"]
    require(q66["decision_state"] == "ANSWER_WITH_CONFLICT", "Q66 must not be clean yes/no")
    q22 = by_id["question:22.0"]["properties"]
    require(q22["decision_state"] == "ANSWER_WITH_CONFLICT", "Q22 must reflect on-prem/cloud conflict")
    q52 = by_id["question:52.0"]["properties"]
    require(q52["decision_state"] == "ASK_USER", "malformed Q52 must ask user")

    template_actions = [
        node
        for node in nodes
        if "ActionItem" in node["labels"]
        and "placeholder" in node["properties"].get("description", "").lower()
    ]
    require(template_actions, "template/placeholder docs must create action items")

    external_nodes = [node for node in nodes if "ExternalFact" in node["labels"]]
    for node in external_nodes:
        props = node["properties"]
        require(props.get("source") == "external", "ExternalFact source must be external")
        require(
            props.get("isolation_rule") == "supplement_only_never_override_internal_evidence",
            "ExternalFact isolation rule missing",
        )
    for rel in relationships:
        if rel["type"] == "SUPPLEMENTS":
            require(
                "ExternalFact" in by_id[rel["start"]]["labels"],
                "Only ExternalFact nodes may SUPPLEMENTS internal graph nodes",
            )

    print("PASS: security graph validates")
    print("Node counts:", dict(sorted(counts.items())))
    print("Relationship counts:", dict(sorted(rel_counts.items())))
    print("Decision counts:", payload["metadata"]["decision_counts"])


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


if __name__ == "__main__":
    main()
