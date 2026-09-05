# Neo4j Security Evidence Graph Architecture

This package defines a graph-first enrichment layer for the cleaned Regodit security corpus. The goal is to let an AI security analyst answer questionnaire rows with citations, surface contradictions, and generate targeted follow-up questions instead of guessing.

## Why A Graph

The corpus has several different evidence types that should not be flattened into one answer string:

- Policies say what Regodit requires.
- Assessment reports say what auditors or testers observed.
- Contracts say what Regodit is obligated to do.
- Infrastructure records show operational reality.
- Internal contradictions show where the agent must ask or escalate.

A property graph keeps those distinctions explicit. The agent can walk from a questionnaire question to a control area, from the control area to claims, from each claim to immutable evidence blocks, and from conflicting claims to the action item needed to resolve the issue.

## Node Types

- `Source`: file-level provenance from `evidence/source_manifest.json`.
- `DocumentControl`: document metadata such as owner, approver, version, effective date, classification, and placeholder status.
- `EvidenceBlock`: atomic quote or table row with immutable locator and source path.
- `Claim`: normalized factual assertion extracted from one or more evidence blocks.
- `ControlArea`: stable security taxonomy such as MFA, backups, encryption, production access, and offboarding.
- `QuestionnaireQuestion`: one of the 66 vendor questionnaire rows.
- `AssessmentFinding`: VAPT or SOC 2 finding, observation, severity, or remediation status.
- `ContractObligation`: contractual obligation around confidentiality, breach notice, data return, deletion, or security standards.
- `Conflict`: contradiction or unresolved ambiguity from the master corpus index and deterministic rules.
- `ActionItem`: human follow-up, remediation, template cleanup, or confirmation needed. Its `open` or
  `resolved` status is loaded from the versioned action-resolution store and records closure provenance.
- `ExternalFact`: optional external evidence from Tavily, isolated from internal evidence.

## Relationship Types

- `(EvidenceBlock)-[:FROM_SOURCE]->(Source)`
- `(DocumentControl)-[:DESCRIBES]->(Source)`
- `(Claim)-[:SUPPORTED_BY]->(EvidenceBlock)`
- `(Claim)-[:MAPS_TO]->(ControlArea)`
- `(QuestionnaireQuestion)-[:ASKS_ABOUT]->(ControlArea)`
- `(Claim)-[:ANSWERS]->(QuestionnaireQuestion)`
- `(Claim)-[:CONTRADICTS]->(Claim)`
- `(Conflict)-[:INVOLVES]->(Claim)`
- `(Conflict)-[:REQUIRES]->(ActionItem)`
- `(AssessmentFinding)-[:VIOLATES_OR_WEAKENS]->(ControlArea)`
- `(ContractObligation)-[:REQUIRES_CONTROL]->(ControlArea)`
- `(ExternalFact)-[:SUPPLEMENTS]->(Claim | AssessmentFinding | ContractObligation)`

## Decision States

Each questionnaire row receives a deterministic decision state:

- `ANSWER_VERIFIED`: enough internal evidence exists to answer with citations.
- `ANSWER_WITH_CONFLICT`: internal evidence supports an answer but conflicting evidence must be shown.
- `ASK_USER`: the answer needs specific human confirmation.
- `ESCALATE`: higher-authority review is required.
- `UNKNOWN`: no adequate evidence path exists yet.

Every usable answer should include supporting `EvidenceBlock` IDs and source locators. A clean yes/no answer without evidence is intentionally treated as incomplete.

## Conflict Handling

Known contradictions are loaded from `corpus_text/00_INDEX/master_corpus_index.json`, including the `agent_guidance` field. That guidance is playbook metadata, not raw evidence. It tells the agent what clarification or escalation to perform when the conflict appears.

Additional deterministic conflict checks should be layered in when new data sources are added, for example:

- Policy says cloud-only, but asset inventory shows an on-prem backup server.
- Policy says immediate offboarding, but access review shows active contractor admin access.
- Diagram shows SIEM, but policy says no dedicated SIEM.
- VAPT report has unresolved findings and no remediation completion evidence.

## Tavily Boundary

Tavily should only enrich external context. It should never replace or overwrite internal evidence.

Good Tavily uses:

- Current references for standards such as NIST SP 800-63B, OWASP Top 10, SOC 2 TSC, and TLS guidance.
- CVE/vendor remediation context for VAPT findings.
- Public vendor trust pages for AWS, GitHub, Google Workspace, and subprocessors.
- External breach/news signals for named vendors.
- Public legal/company facts where internal records conflict.

External results must be stored as `ExternalFact` nodes with retrieval date, URL, declared provider, and
`source = external`. They may supplement an internal claim but never replace it.

## Snapshot And Resolution State

The graph is a static point-in-time corpus snapshot. Rebuild it whenever corpus evidence or operational
state changes; it does not query live systems during normal graph construction. A human may close an
action item through `graph/action_resolutions.json`, recording `resolved_at`, `resolved_by`, a note, and
supporting evidence. That closure changes only the action item: an underlying contradiction remains visible
until the corpus itself documents its resolution.

## Build

From the repository root:

```bash
python3 graph/build_security_graph.py
python3 tools/validate_security_graph.py
```

Generated artifacts are written to `graph/out/`:

- `security_graph.json`
- `nodes.jsonl`
- `relationships.jsonl`
- `nodes.csv`
- `relationships.csv`
- `neo4j_import.cypher`

Optional external enrichment:

```bash
printf 'TAVILY_API_KEY=tvly-...\n' > .env.local
python3 tools/tavily_external_enrichment.py
python3 graph/build_security_graph.py --external-facts graph/out/external_facts.tavily.json
python3 tools/validate_security_graph.py
```

The Tavily collector currently targets high-signal cases: NIST MFA guidance, OWASP web application risks, TLS guidance, AWS/GitHub/Google public trust material, and remediation context for missing authentication and prompt injection findings.

## Expected Counts

Current expected output:

- 26 source files
- 28 curated corpus documents
- 66 questionnaire questions
- At least 7 known conflicts, preserving the baseline while allowing new detections
- 21 control areas

The validator asserts the key counts and checks that conflicts, citations, questionnaire mappings, action items, and external-fact isolation behave as expected.
