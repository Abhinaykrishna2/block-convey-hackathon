"""
Ingestion stub: chunks all policy/report/contract docx files into
(source, chunk_id, text) records. This is a STUB for Mathan's agent
to build/test against before the real ingestion pipeline (owned by
teammate) is ready. Swap out load_chunks() later for the real thing —
keep the same return shape: list of dicts with keys source, chunk_id, text.
"""
import docx
import glob
import json
import os

def chunk_docx(path, min_len=40):
    """Split a docx into paragraph-level chunks, merging short fragments
    into the previous chunk so we don't end up with tons of 3-word chunks."""
    d = docx.Document(path)
    chunks = []
    buffer = ""
    for p in d.paragraphs:
        text = p.text.strip()
        if not text:
            continue
        buffer += (" " if buffer else "") + text
        if len(buffer) >= min_len:
            chunks.append(buffer)
            buffer = ""
    if buffer:
        chunks.append(buffer)
    return chunks

def load_chunks():
    records = []
    docx_files = glob.glob("**/*.docx", recursive=True)
    for path in docx_files:
        source = os.path.basename(path)
        try:
            chunks = chunk_docx(path)
        except Exception as e:
            print(f"skip {path}: {e}")
            continue
        for i, text in enumerate(chunks):
            records.append({
                "source": source,
                "chunk_id": f"{source}::{i}",
                "text": text
            })
    return records

if __name__ == "__main__":
    records = load_chunks()
    print(f"Total chunks: {len(records)}")
    # save for reuse
    with open("chunks.json", "w") as f:
        json.dump(records, f, indent=2)
    # sanity: show a couple chunks from the access control policy
    for r in records:
        if "access_control" in r["source"]:
            print(r["chunk_id"], "->", r["text"][:150])
