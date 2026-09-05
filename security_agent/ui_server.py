"""
Lightweight UI Web Server for Regodit AI Security Analyst.
Serves the Cytoscape graph visualizer from ui/ and handles dynamic queries
via the GraphTreeRetriever & guardrailed agent_loop.

Run:
  python3 security_agent/ui_server.py [port]
"""
from __future__ import annotations

import http.server
import json
import os
import socketserver
import sys
from typing import Any, Dict

try:
    from agent_loop import process_question, load_chunks
    from retrieve_graph import GraphTreeRetriever as Retriever
except ImportError:
    from security_agent.agent_loop import process_question, load_chunks
    from security_agent.retrieve_graph import GraphTreeRetriever as Retriever

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
UI_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ui"))

graph = load_chunks()
retriever = Retriever(graph)


def extract_subgraph(q_text: str, res: Dict[str, Any]) -> Dict[str, Any]:
    matched_q = retriever._match_question(q_text)
    sub_nodes = []
    sub_edges = []
    node_ids = set()

    def add_node(n):
        if n["id"] not in node_ids:
            node_ids.add(n["id"])
            sub_nodes.append({
                "id": n["id"],
                "label": n.get("labels", ["Unknown"])[0],
                "properties": n.get("properties", {}),
            })

    def add_edge(r):
        sub_edges.append({
            "source": r["start"],
            "target": r["end"],
            "type": r["type"],
        })

    if matched_q:
        add_node(matched_q)
        qid = matched_q["id"]
        for r in retriever.out_rels.get(qid, []):
            end_node = retriever.nodes.get(r["end"])
            if end_node:
                add_node(end_node)
                add_edge(r)
                if r["type"] == "HAS_CONFLICT":
                    for cr in retriever.out_rels.get(r["end"], []):
                        c_end = retriever.nodes.get(cr["end"])
                        if c_end:
                            add_node(c_end)
                            add_edge(cr)
        for r in retriever.in_rels.get(qid, []):
            start_node = retriever.nodes.get(r["start"])
            if start_node and r["type"] == "ANSWERS":
                add_node(start_node)
                add_edge(r)

    return {
        "result": res,
        "subgraph": {
            "nodes": sub_nodes,
            "edges": sub_edges,
        },
    }


class SecurityUIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=UI_DIR, **kwargs)

    def do_POST(self):
        if self.path == "/api/query":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                q_text = data.get("question", "")
                result = process_question(q_text, retriever, top_k=12)
                payload = extract_subgraph(q_text, result)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(payload).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


if __name__ == "__main__":
    print(f"Starting Regodit AI Security Analyst UI Server on http://localhost:{PORT}")
    print(f"Serving web directory: {UI_DIR}")
    with socketserver.TCPServer(("", PORT), SecurityUIHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down server.")
