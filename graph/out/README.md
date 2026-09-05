# Security Graph Output

Generated artifacts for importing the enriched security corpus into Neo4j.

## Files

- `security_graph.json`: portable graph payload with nodes, relationships, and metadata.
- `nodes.jsonl` / `relationships.jsonl`: line-delimited graph records for agents and tests.
- `nodes.csv` / `relationships.csv`: compact interchange files.
- `neo4j_import.cypher`: self-contained Cypher import script. Run it in `cypher-shell` or Neo4j Browser.

## Counts

- Sources: 26
- Curated documents: 28
- Questionnaire questions: 66
- Nodes: 9646
- Relationships: 10523

## External Data Rule

Tavily results are optional and must be loaded as `ExternalFact` nodes only. They may `SUPPLEMENTS` internal claims, findings, or obligations, but must not overwrite internal `Claim` or `EvidenceBlock` records.
