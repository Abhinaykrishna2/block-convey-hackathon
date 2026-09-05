"""
Retrieval stub v2: TF-IDF + cosine similarity instead of raw keyword
overlap. Still not a real embedding model, but much better at
downweighting generic words ("access", "systems", "company") that
show up everywhere and drown out the actually relevant chunk.

Honors the shared contract in retriever_base.py (chunk_id/source/text/
score, best-first) - see retrieve_graph.py for the alternate graph/tree
backend that honors the same contract.
"""
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from retriever_base import validate_retrieval_results

def load_chunks(path="chunks.json"):
    with open(path) as f:
        return json.load(f)

class Retriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.texts = [c["text"] for c in chunks]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(self.texts)

    def retrieve(self, query, top_k=5):
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.matrix)[0]
        ranked_idx = sims.argsort()[::-1][:top_k]
        results = []
        for i in ranked_idx:
            if sims[i] <= 0:
                continue
            results.append({**self.chunks[i], "score": round(float(sims[i]), 4)})
        return validate_retrieval_results(results, query=query)

if __name__ == "__main__":
    chunks = load_chunks()
    r = Retriever(chunks)
    query = "Does your organization require replay-resistant authentication mechanisms such as OTP or MFA?"
    results = r.retrieve(query, top_k=8)
    print(f"Query: {query}\n")
    for res in results:
        print(f"[{res['score']}] {res['source']} :: {res['chunk_id']}")
        print("   ", res["text"][:200])
        print()
