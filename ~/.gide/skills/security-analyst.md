# Project: AI Security Analyst

## Goal
A chatbot that completes an enterprise security questionnaire by investigating a
company's own documents, and asking the user only when the documents don't answer.

## THE GOLDEN RULE — enforced in code, not by prompt
An answer may be marked "verified" ONLY if it carries at least one real evidence ID.
If `evidence_ids` is empty, code MUST downgrade the status. The LLM never decides this.
Never fabricate an answer. Unknown is a valid, correct output.

## Four statuses
- `verified`      — supported by company documents (must cite evidence)
- `user_confirmed`— user supplied it in conversation
- `conflict`      — sources disagree; needs user resolution
- `unknown`       — no evidence, user hasn't answered

## Evidence ID format (non-negotiable)
`<filename>:L<start>-L<end>` e.g. `security-policy.md:L45-L52`
Citations must resolve to exact lines so the UI can link to them.

## Architecture rules
- Retrieval, citation, and status classification: deterministic Python. No LLM.
- LLM only: phrasing answers, noticing that two snippets disagree, writing follow-ups.
- All LLM calls return STRICT JSON. Parse failure = retry once, then mark `unknown`.

## Stack
Python 3.11, FastAPI, rank_bm25 for retrieval, SQLite for the profile,
one static HTML page with vanilla JS. No React, no vector DB.

## Files
corpus.py  retriever.py  verdict.py  profile.py  questionnaire.py
prism_client.py  main.py  static/index.html

## Style
Small functions, type hints, no clever abstractions. Every module runnable standalone.
