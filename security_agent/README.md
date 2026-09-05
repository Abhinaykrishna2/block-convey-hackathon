# Regodit AI Security Analyst — Agent + Guardrails + Evals

Mathan's part of the Money Talks / Regodit track build.

## Setup
```
pip install python-docx openpyxl scikit-learn --break-system-packages
```
Put the extracted policy/report/contract docx files in the same folder
(or update the glob path in chunk_docs.py), then:

```
python3 chunk_docs.py       # builds chunks.json from real docs
python3 retrieve_v2.py      # sanity-check retrieval on a sample query
python3 eval_runner.py      # run the eval scorecard
python3 conversation_loop.py  # run the full multi-turn demo
```

## Files, in the order you'd read them
1. **chunk_docs.py** — splits docx files into paragraph-level chunks
2. **retrieve_v2.py** — TF-IDF retrieval STUB (swap for teammate's real
   ingestion/embedding pipeline — same return shape: list of
   {chunk_id, source, text, score})
3. **agent_loop.py** — the core decision loop: retrieve → LLM reasoning
   → guardrail enforcement → answered/conflict/ask_user. Contains the
   DECISION_PROMPT_TEMPLATE to send to Claude, and call_llm() is a
   stub to wire up with a real API key on hackathon day (see TODO
   comment inside).
4. **security_profile.py** — persistent state store ("remember
   everything", no duplicate questions, corrections update in place)
5. **conversation_loop.py** — full multi-turn flow per question,
   including the vague-answer → follow-up loop (evaluate_user_reply()
   is also a mock — TODO comment marks where to plug in the real LLM)
6. **eval_set.py / eval_runner.py** — hand-verified ground-truth test
   cases + a pass/fail scorecard runner

## TODO before the hackathon
- Wire call_llm() in agent_loop.py to real Anthropic API
- Wire evaluate_user_reply() in conversation_loop.py to real API too
- Point chunk_docs.py at wherever the REAL provided docs land on the day
- Confirm top_k (currently 12) is wide enough once real embeddings replace TF-IDF
