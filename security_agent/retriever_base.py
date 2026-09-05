"""
The retrieval contract - the ONE thing agent_loop.py / conversation_loop.py
/ eval_runner.py actually depend on. Doesn't matter if the backend is
TF-IDF (retrieve_v2.py), your teammate's graph/tree traversal, or real
embeddings later - as long as it honors this shape, nothing downstream
needs to change.

CONTRACT
--------
Any retriever must expose:

    retriever.retrieve(query: str, top_k: int = 12) -> list[dict]

Each dict in the returned list MUST have these keys:

    chunk_id : str    - stable identifier you can cite back to a human
                         (a paragraph index, a graph node id, a path
                         through a tree - anything stable and unique)
    source   : str    - the source document's filename (or equivalent)
    text     : str    - the actual passage/evidence text
    score    : float  - HIGHER = MORE RELEVANT (0.0-1.0ish). If your
                         backend naturally produces a "lower is better"
                         distance/depth score, invert or normalize it
                         before returning - don't change the meaning of
                         score here, or CONFIDENCE_FLOOR and the
                         insufficient-evidence check in agent_loop.py
                         will silently misbehave.

Results should be returned ranked best-first (highest score first) -
process_question() just takes chunks[0] as "the top hit" without
re-sorting.

Use validate_retrieval_results() below at the end of your retrieve()
implementation while building it - it raises immediately with a clear
message if the shape is wrong, instead of agent_loop.py failing later
with a confusing KeyError three files away.
"""

REQUIRED_KEYS = {"chunk_id", "source", "text", "score"}


def validate_retrieval_results(results, query=None):
    """
    Call this at the end of any retrieve() implementation:

        def retrieve(self, query, top_k=12):
            results = [...build your results...]
            validate_retrieval_results(results, query=query)
            return results

    Raises AssertionError with a specific, actionable message on any
    shape mismatch. Returns the results unchanged on success (so you
    can also do `return validate_retrieval_results(results)`).
    """
    context = f" (query={query!r})" if query else ""

    assert isinstance(results, list), (
        f"retrieve() must return a list, got {type(results).__name__}{context}"
    )

    for i, r in enumerate(results):
        assert isinstance(r, dict), (
            f"retrieve() result[{i}] must be a dict, got {type(r).__name__}{context}"
        )
        missing = REQUIRED_KEYS - r.keys()
        assert not missing, (
            f"retrieve() result[{i}] is missing required key(s) {missing}{context}. "
            f"Got keys: {list(r.keys())}"
        )
        assert isinstance(r["chunk_id"], str) and r["chunk_id"], (
            f"retrieve() result[{i}]['chunk_id'] must be a non-empty string{context}"
        )
        assert isinstance(r["source"], str) and r["source"], (
            f"retrieve() result[{i}]['source'] must be a non-empty string{context}"
        )
        assert isinstance(r["text"], str) and r["text"], (
            f"retrieve() result[{i}]['text'] must be a non-empty string{context}"
        )
        assert isinstance(r["score"], (int, float)), (
            f"retrieve() result[{i}]['score'] must be a number, got {type(r['score']).__name__}{context}"
        )

    # ranked best-first check (warn via assertion only if clearly violated -
    # allow ties/near-ties, just catch an obviously unsorted list)
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True), (
        f"retrieve() results must be sorted best-first (highest score first){context}. "
        f"Got scores in this order: {scores}"
    )

    return results
