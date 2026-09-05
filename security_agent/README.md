# Security Agent

Backend for the Regodit AI Security Analyst. The agent answers vendor
security questions by investigating evidence first, asking the user only
when the documents cannot answer, and never fabricating.

## Modules

- retriever_base.py: the retrieval contract. Any backend must return
  (chunk_id, source, text, score), ranked best-first, higher score means
  more relevant.
- retrieve_graph.py: GraphTreeRetriever, the production backend. Traverses
  the security evidence graph (graph/out/security_graph.json) across
  questions, control areas, conflicts, claims, and evidence blocks.
- agent_loop.py: the decision loop plus guardrails. Produces one of
  ANSWERED, CONFLICT, ASK_USER, or FOLLOW_UP. Every LLM verdict passes
  enforce_guardrails() before becoming final. Traces each question to
  PRISM as a trajectory.
- security_profile.py: persistent security profile in security_profile.json.
  Stores verified, user confirmed, and unknown answers with citations,
  avoids duplicate questions, supports corrections.
- conversation_loop.py: interactive CLI chat with conflict resolution and
  follow-up drilling (for example: backups exist, but how often, and are
  they automated).
- run_66_benchmark.py: audits the full 66 question questionnaire, exports
  evidence/questionnaire_audit_results_66.json, flushes PRISM trajectories.
- eval_runner.py + eval_set.py: small eval harness for targeted test cases.
- ui_server.py: serves ui/ (Cytoscape graph visualizer) and exposes a query
  endpoint backed by the retriever and the guardrailed agent.

## Decision Flow

retrieve(question) -> evidence chunks -> LLM proposes verdict ->
enforce_guardrails() verifies citations and conflict handling ->
final status with answer, citations, confidence, and guardrail note.

The guardrail is what makes the system defensible: the LLM proposes,
the guardrail disposes. No citation means no answer.

## Benchmark

Latest run: 38 answered, 11 conflict, 17 ask_user, 0 fabricated,
across all 66 questions with PRISM tracing enabled.
