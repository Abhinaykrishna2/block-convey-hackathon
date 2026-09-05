# Graph Enrichment Package

This directory contains the graph architecture approach for comparing data enrichment strategies.

- `ARCHITECTURE.md`: graph model, evidence rules, conflict handling, Tavily boundary, and expected counts.
- `build_security_graph.py`: deterministic builder that converts the cleaned corpus into graph artifacts.
- `external_facts.example.json`: optional Tavily-style external fact input.
- `action_resolutions.json`: versioned state store for human-confirmed action-item closure.
- `SAMPLE_QUERIES.cypher`: Neo4j queries for comparing answers, conflicts, unresolved questions, VAPT findings, and contract obligations.
- `out/`: generated artifacts, if committed or produced locally.
- `../tools/tavily_external_enrichment.py`: optional Tavily collector for standards, vendor trust pages, and VAPT remediation context.

Build and validate:

```bash
python3 graph/build_security_graph.py
python3 tools/validate_security_graph.py
```

Action resolutions use stable `ActionItem` IDs from the generated graph. Copy the schema from
`action_resolutions.example.json`, replace its placeholder ID, and rebuild. Resolving an action item
does not remove the source conflict that originally created it.

Run Tavily enrichment:

```bash
printf 'TAVILY_API_KEY=tvly-...\n' > .env.local
python3 tools/tavily_external_enrichment.py
python3 graph/build_security_graph.py --external-facts graph/out/external_facts.tavily.json
python3 tools/validate_security_graph.py
```

The generated `graph/out/neo4j_import.cypher` file can be pasted into Neo4j Browser or run through `cypher-shell`.
