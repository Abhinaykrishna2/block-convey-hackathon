#!/usr/bin/env python3
"""Regression tests for graph resolution state and external-fact provenance."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from graph.build_security_graph import DEFAULT_CORPUS, SecurityGraphBuilder  # noqa: E402


class SecurityGraphBuilderTests(unittest.TestCase):
    def test_resolution_store_and_external_provider_are_preserved(self) -> None:
        baseline = SecurityGraphBuilder(DEFAULT_CORPUS, None, None).build()
        action = next(node for node in baseline["nodes"] if "ActionItem" in node["labels"])
        action_id = action["id"]

        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            resolutions = temp / "action_resolutions.json"
            resolutions.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "action_items": {
                            action_id: {
                                "status": "resolved",
                                "resolved_at": "2026-09-05T14:30:00Z",
                                "resolved_by": "security-team@example.com",
                                "resolution_evidence": ["ticket:SEC-123"],
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            external_facts = temp / "external_facts.json"
            external_facts.write_text(
                json.dumps(
                    {
                        "provider": "nist_api",
                        "facts": [
                            {
                                "id": "provider-provenance-test",
                                "title": "NIST context",
                                "url": "https://example.com/nist",
                                "supplements": "claim:mfa:core_systems",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            payload = SecurityGraphBuilder(DEFAULT_CORPUS, external_facts, resolutions).build()

        nodes = {node["id"]: node for node in payload["nodes"]}
        props = nodes[action_id]["properties"]
        self.assertEqual(props["status"], "resolved")
        self.assertEqual(props["status_source"], "resolution_file")
        self.assertEqual(props["resolved_at"], "2026-09-05T14:30:00Z")
        self.assertEqual(nodes["CONFLICT-001"]["properties"]["status"], "unresolved")
        self.assertEqual(nodes["external:provider-provenance-test"]["properties"]["provider"], "nist_api")


if __name__ == "__main__":
    unittest.main()
