# Graph Enrichment Package

This directory contains the graph architecture approach for comparing data enrichment strategies.

- `ARCHITECTURE.md`: graph model, evidence rules, conflict handling, Tavily boundary, and expected counts.
- `build_security_graph.py`: deterministic builder that converts the cleaned corpus into graph artifacts.
- `external_facts.example.json`: optional Tavily-style external fact input.
- `SAMPLE_QUERIES.cypher`: Neo4j queries for comparing answers, conflicts, unresolved questions, VAPT findings, and contract obligations.
- `out/`: generated artifacts, if committed or produced locally.

Build and validate:

```bash
python3 graph/build_security_graph.py
python3 tools/validate_security_graph.py
```

The generated `graph/out/neo4j_import.cypher` file can be pasted into Neo4j Browser or run through `cypher-shell`.
