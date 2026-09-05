"""
Adapter scaffold for the teammate's GRAPH/TREE retrieval backend.

Same job as retrieve_v2.py (the TF-IDF stub) - just a different
internal implementation. Give this file to your teammate: they fill
in _load_graph() and the traversal logic inside retrieve(), and as
long as retrieve() honors the contract in retriever_base.py, nothing
in agent_loop.py / conversation_loop.py / eval_runner.py needs to
change to use it.

SWAPPING IT IN (once it's ready):
  In agent_loop.py, conversation_loop.py, and eval_runner.py, change:
      from retrieve_v2 import load_chunks, Retriever
  to:
      from retrieve_graph import load_chunks, GraphTreeRetriever as Retriever
  That's the only change needed anywhere.

A toy, runnable example is included at the bottom (__main__) using a
tiny hand-built graph, so this file is testable TODAY, before the real
graph-building pipeline exists - it proves the adapter shape works
before it's wired to real data.
"""
import json
import os

from retriever_base import validate_retrieval_results

DEFAULT_GRAPH_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graph.json")


def _load_graph(path=DEFAULT_GRAPH_PATH):
    """
    TODO (teammate): load whatever your graph/tree build step produces.
    Shape is up to you internally - nodes with parent/child edges,
    a networkx graph pickled to disk, whatever. This function is the
    only place that needs to know the real format.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No graph found at {path}. Run your graph-building pipeline first, "
            f"or point _load_graph() at wherever it writes output."
        )
    with open(path) as f:
        return json.load(f)


def load_chunks(path=DEFAULT_GRAPH_PATH):
    """Kept for symmetry with retrieve_v2.load_chunks() so callers that
    do `chunks = load_chunks(); retriever = Retriever(chunks)` don't
    need an if/else - just returns whatever _load_graph() gives back."""
    return _load_graph(path)


class GraphTreeRetriever:
    """
    TODO (teammate): implement retrieve() to walk your graph/tree for
    the query and return the best-matching nodes as evidence, in the
    exact shape retriever_base.py requires.

    Suggested approach, adapt as needed:
      1. Find entry point(s) into the graph relevant to the query
         (e.g. embed the query, find nearest node(s); or keyword-match
         into a topic/section node).
      2. Traverse outward (parent/child/sibling edges) to collect
         candidate leaf nodes - this is where a graph should beat flat
         TF-IDF: it can pull in a RELATED section from a different
         document (e.g. a policy clause AND the pentest finding that
         contradicts it) even if their wording doesn't overlap much.
      3. Score each candidate (semantic similarity, edge distance,
         whatever) and normalize so HIGHER SCORE = MORE RELEVANT
         (invert if your natural metric is a distance).
      4. Map each candidate node to {chunk_id, source, text, score}.
      5. Sort best-first, slice to top_k, validate, return.
    """

    def __init__(self, graph_data):
        self.graph_data = graph_data

    def retrieve(self, query, top_k=12):
        raise NotImplementedError(
            "TODO (teammate): implement graph/tree traversal here. "
            "See the toy example in this file's __main__ block for the "
            "expected shape of the return value."
        )


if __name__ == "__main__":
    # Toy, runnable example - a tiny 3-node graph, so this adapter shape
    # is provable today without the real graph pipeline existing yet.
    # This is NOT what the real implementation should look like - it's
    # just proof that "graph in, contract-shaped list out" works.

    toy_graph = {
        "nodes": [
            {"id": "policy::mfa_clause", "source": "password_policy.docx",
             "text": "MFA is required across all core systems.", "topic": "mfa"},
            {"id": "pentest::finding_12", "source": "vapt_report.docx",
             "text": "Recommend implementing MFA on the customer-facing web app.", "topic": "mfa"},
            {"id": "policy::unrelated_clause", "source": "hr_policy.docx",
             "text": "Employees must complete annual training.", "topic": "training"},
        ]
    }

    class ToyGraphRetriever(GraphTreeRetriever):
        """Minimal working traversal: keyword-match into 'topic', return
        every node sharing that topic. Just enough to prove the contract -
        real version should do real graph traversal + real scoring."""

        def retrieve(self, query, top_k=12):
            query_lower = query.lower()
            matches = [n for n in self.graph_data["nodes"] if n["topic"] in query_lower]
            results = [
                {
                    "chunk_id": n["id"],
                    "source": n["source"],
                    "text": n["text"],
                    "score": 0.9,  # toy: flat score, real version should vary by relevance
                }
                for n in matches
            ][:top_k]
            return validate_retrieval_results(results, query=query)

    retriever = ToyGraphRetriever(toy_graph)
    query = "Does your organization require MFA?"
    results = retriever.retrieve(query)
    print(f"Query: {query}\n")
    for r in results:
        print(f"[{r['score']}] {r['source']} :: {r['chunk_id']}")
        print("   ", r["text"])
    print(f"\n{len(results)} result(s) - shape validated OK.")
