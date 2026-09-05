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

## Snapshot Freshness

This is a static point-in-time corpus snapshot. Rebuild after evidence or operational state changes; it does not query live systems.

## Action Resolutions

Action-item status is loaded from `graph/action_resolutions.json`. Resolution metadata records who closed an item, when, and supporting evidence. Closing an action item does not silently resolve an underlying source contradiction.

## External Data Rule

External enrichment is optional and must be loaded as `ExternalFact` nodes only. Each node retains its declared provider. It may `SUPPLEMENTS` internal claims, findings, or obligations, but must not overwrite internal `Claim` or `EvidenceBlock` records.
