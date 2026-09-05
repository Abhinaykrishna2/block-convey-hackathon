"""Knowledge graph construction for the Regodit Security Analyst corpus.

Nodes: claims (evidence-backed statements), entities, documents, questions.
Edges: claim->document (source), claim->entity, claim->question (relevance),
question->topic, claim<->claim (potential conflicts via shared entity + opposite polarity).

Design notes (ponytail: graph is a thin index over blocks.jsonl — every node
carries its source locator; no duplication of source text beyond what BM25 needs).

Output: knowledge_graph.json + kg_index.jsonl (one line per claim, BM25-ready)
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BLOCKS = ROOT / "evidence" / "blocks.jsonl"
QUESTIONNAIRE = ROOT / "evidence" / "questionnaire.json"
OUT = ROOT / "evidence" / "knowledge_graph.json"
OUT_IDX = ROOT / "evidence" / "kg_index.jsonl"

# ------------------------------------------------------------------ entities --
# Seed entity vocabulary from the corpus domain. Extended by regex extraction.
ENTITY_PATTERNS = [
    ("Person",       r"\b(?:[A-Z]\. ){2}[A-Z][a-zA-Z'-]+(?:,? (?:Admin|Editor|Viewer|Lead|Contractor|Support))?\b"),
    ("System",       r"\b(?:AWS(?: Production Console| CloudTrail| IAM| KMS| S3| RDS| DynamoDB)?|GitHub|Google Workspace|VPN|Bastion host|SIEM|CloudWatch|EKS|VPC|CDN\+WAF?|Meraki MX67|Dell PowerEdge R740)\b"),
    ("Control",      r"\b(?:MFA|multi-factor authentication|SSO|single sign-on|encryption at rest|TLS|AES-256|least privilege|separation of duties|segregation of duties|access review|background verification|BGV|vulnerability scan(?:ning)?|penetration test(?:ing)?|backup|backups|restore test|recovery test|restore|recovery objectives|incident response|security awareness training|NDA|offboarding|deprovisioning|revocation|revoke access|data classification|secure disposal|logging|monitoring)\b"),
    ("Standard",     r"\b(?:SOC 2(?: Type [I1I]+[Ii]*)?|ISO 27001|NIST(?: 800-63B?)?|GDPR|CCPA|SOX|CVSS)\b"),
    ("Data element", r"\b(?:customer data|PII|personal data|PHI|sensitive data|production data|logs?|backups?|source code|encryption keys?|secrets?)\b"),
    ("Location",     r"\b(?:AWS US regions?|multiple Availability Zones|Multi-AZ|HQ server room|on-premise|cloud|United States|offshore)\b"),
    ("Timeline",     r"\b(?:annual(?:ly)?|quarterly|monthly|daily|immediate(?:ly)?|within \d+ days?|\d+\s*(?:hour|day|month|year)s?)\b|\bRPO\b|\bRTO\b"),
    ("Vendor",       r"\b(?:Regodit|Solsphere(?: AI Inc)?|Client XYZ)\b"),
]

COMPILED = [(name, re.compile(rx)) for name, rx in ENTITY_PATTERNS]

TOPIC_KEYWORDS = {
    "Governance": ["information security program", "security policy", "leadership", "role descriptions", "escalation"],
    "Third-Party Risk Management": ["third-party", "vendor", "subcontractor", "supply chain", "contract"],
    "Security Awareness & Training": ["awareness training", "training", "onboarding training"],
    "Privacy": ["privacy", "PII", "personal data", "retention schedule", "disposal"],
    "Data Security": ["encryption", "at rest", "in transit", "TLS", "AES", "data center", "stored"],
    "Physical Security": ["physical", "onsite", "office", "visitor", "device", "badge"],
    "Web Application Security": ["web application", "SSL", "TLS certificate", "SSO", "application security"],
    "Secure Coding": ["secure development", "SDLC", "code review", "coding"],
    "Vulnerability Management": ["vulnerability", "scan", "patch", "CVSS", "penetration test", "remediation"],
    "Business Continuity & Disaster Recovery": ["backup", "disaster recovery", "BCP", "DR", "RTO", "RPO", "restore", "business continuity"],
    "Incident Response": ["incident", "breach", "security event", "response plan", "notify"],
    "Network & Endpoint Security": ["network", "firewall", "endpoint", "antivirus", "VPN", "segmentation", "SIEM", "logging", "monitoring", "on-premise", "servers"],
    "Asset Management": ["asset", "inventory", "access control", "least privilege", "RBAC", "access review", "MFA", "offboarding", "deprovisioning"],
    "Risk Assessment": ["risk assessment", "risk register", "critical assets", "prioritize"],
    "Data Security": ["encryption", "at rest", "in transit", "TLS", "AES", "data center", "stored", "SIEM", "on-premise", "servers", "customer data"],
}

# polarity families for conflict detection: assertion -> negation/absence markers
# a claim is ASSERTIVE if it affirms a control exists/operates; ABSENCE if it
# records lack, gap, planned-but-not-done, or an unresolved action.
CONFLICT_PAIRS = [
    (r"\b(?:is|are|was|were)\b.{0,30}\b(?:mandatory|enforced|required|in place|performed|completed|maintained|automated|active|enabled|immediate(?:ly)?)\b"
     r"|\b(?:must|shall|requires?)\b"
     r"|\ball (?:users|personnel|systems|employees|contractors)\b"
     r"|\b(?:automated|daily|annual|quarterly|monthly) [a-z]+(?:ing)?\b",
     r"\bno\b|\bnot\b|\bwithout\b|\bmissing\b|\bplanned\b|\bdoes not\b|\bdoesn't\b|\bhas yet\b|\bnot yet\b|\bnever\b|\blag\b|\bgap\b|\bexception\b|\bflagged\b|\baction needed\b|\bN/A\b|\bunverified\b|\bnot been performed\b|\bfailing\b|\bopen\b"),
]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", " ", s).strip()


def node_id(prefix: str, key: str) -> str:
    return f"{prefix}:{hashlib.sha256(key.encode()).hexdigest()[:12]}"


def extract_entities(text: str) -> list[tuple[str, str]]:
    found = []
    seen = set()
    for name, rx in COMPILED:
        for m in rx.finditer(text):
            val = norm(m.group(0))
            k = (name, val)
            if k not in seen:
                seen.add(k)
                found.append(k)
    return found


def classify_topic(text: str) -> str | None:
    t = text.lower()
    best, best_score = None, 0
    for topic, kws in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in kws if kw in t)
        if score > best_score:
            best, best_score = topic, score
    return best


def is_claim_worthy(b: dict) -> bool:
    """A block becomes a claim node if it has meaningful text and isn't sheet plumbing."""
    if b["kind"] not in ("word_paragraph", "pdf_page_text"):
        # spreadsheet cells: keep only non-empty, non-formula-bearing text cells
        if b["kind"] == "spreadsheet_cell":
            t = (b.get("text") or "").strip()
            if not t or len(t) < 4:
                return False
            if b.get("source", "").endswith("Questionnaire_Clean.xlsx"):
                return False  # the questionnaire is questions, not evidence claims
            return True
        return b["kind"] != "worksheet_metadata"
    t = b["text"].strip()
    return len(t) >= 40  # paragraphs need substance


def build():
    blocks = [json.loads(l) for l in open(BLOCKS)]
    questionnaire = json.load(open(QUESTIONNAIRE))["questions"]

    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    def add_node(nid: str, **props):
        if nid in nodes:
            nodes[nid].update({k: v for k, v in props.items() if k not in nodes[nid] or not nodes[nid].get(k)})
        else:
            nodes[nid] = {"id": nid, **props}

    # -- document nodes
    for src in sorted({b["source"] for b in blocks}):
        add_node(node_id("doc", src), type="document", source=src,
                 role=next(b["document_role"] for b in blocks if b["source"] == src))

    # -- question nodes
    for q in questionnaire:
        qid = str(q["id"]).replace(".0", "")
        topic = classify_topic(q["question"]) or "Uncategorized"
        add_node(node_id("q", qid), type="question", qid=qid, text=q["question"],
                 topic=topic, source_cell=q["source_cell"],
                 wording_status=q.get("wording_status", "source_direct"))
        edges.append({"from": node_id("q", qid), "to": node_id("topic", topic), "rel": "in_topic"})
        add_node(node_id("topic", topic), type="topic", name=topic)

    # -- claim nodes from evidence blocks
    claim_count = 0
    for b in blocks:
        if not is_claim_worthy(b):
            continue
        text = norm(b["text"])
        if not text:
            continue
        cid = b["id"]  # block id IS the claim id — locator preserved
        topic = classify_topic(text)
        entities = extract_entities(text)
        add_node(cid, type="claim", text=text[:600], source=b["source"],
                 locator=b["locator"], role=b["document_role"], kind=b["kind"],
                 topic=topic, sheet=b.get("sheet"), cell=b.get("cell"),
                 table=b.get("table"), row=b.get("row"))
        edges.append({"from": cid, "to": node_id("doc", b["source"]), "rel": "from_document"})
        if topic:
            edges.append({"from": cid, "to": node_id("topic", topic), "rel": "in_topic"})
        for etype, eval_ in entities:
            eid = node_id("ent", f"{etype}|{eval_}")
            add_node(eid, type="entity", etype=etype, name=eval_)
            edges.append({"from": cid, "to": eid, "rel": "mentions"})
        claim_count += 1

    # -- question→claim candidate edges: claim topic matches question topic, OR claim mentions
    #    entities whose name appears in the question text
    q_by_id = {n["qid"]: n for n in nodes.values() if n["type"] == "question"}
    for q in q_by_id.values():
        ql = q["text"].lower()
        for n in nodes.values():
            if n["type"] != "claim":
                continue
            if q.get("topic") and n.get("topic") == q["topic"]:
                edges.append({"from": q["id"], "to": n["id"], "rel": "candidate_evidence", "via": "topic"})
                continue
        # entity-name hits
        for n in nodes.values():
            if n["type"] == "entity" and n["name"].lower() in ql:
                # link question -> entity -> claims handled implicitly; add explicit edge
                edges.append({"from": q["id"], "to": n["id"], "rel": "asks_about"})

    # -- claims from curated visual transcriptions (diagrams/attestations whose
    #    evidence lives in corpus_text mds, not machine-extractable text)
    visual_md = {
        "network_segmentation_architecture.md": "diagram_or_reference_requires_confirmation",
        "privileged_admin_access_and_logging.md": "diagram_or_reference_requires_confirmation",
        "network_architecture_reference_diagrams.md": "diagram_or_reference_requires_confirmation",
        "soc2_auditor_attestation_and_badges.md": "mixed_document_requires_confirmation",
        "risk_matrix_heatmap_and_ranges.md": "questionnaire_template",
    }
    for md_name, role in visual_md.items():
        for sub in (ROOT / "corpus_text").rglob(md_name):
            for l in sub.read_text().split("\n"):
                l = l.strip()
                if not l or l.startswith(("#", "<!--", "Source", "- **Source", "Document role", "---", "- **Evidence status")):
                    continue
                if l.startswith("|"):
                    if l.count("|") >= 2:
                        txt = norm(l.split("|")[-2].strip())
                    else:
                        continue
                else:
                    txt = norm(l.lstrip("- ").strip("`"))
                if len(txt) < 8:
                    continue
                cid = node_id("vclaim", sub.name + l)
                topic = classify_topic(txt)
                add_node(cid, type="claim", text=txt[:600],
                         source=f"corpus_text/{sub.parent.name}/{sub.name}",
                         locator=md_name, role=role, kind="visual_transcription", topic=topic)
                edges.append({"from": cid, "to": node_id("doc", f"corpus_text/{sub.parent.name}/{sub.name}"),
                              "rel": "from_document"})
                if topic:
                    edges.append({"from": cid, "to": node_id("topic", topic), "rel": "in_topic"})
                for etype, eval_ in extract_entities(txt):
                    eid = node_id("ent", f"{etype}|{eval_}")
                    add_node(eid, type="entity", etype=etype, name=eval_)
                    edges.append({"from": cid, "to": eid, "rel": "mentions"})
                claim_count += 1
            add_node(node_id("doc", f"corpus_text/{sub.parent.name}/{sub.name}"), type="document",
                     source=f"corpus_text/{sub.parent.name}/{sub.name}", role=role)

    # -- conflict edges: claims in same topic with opposing polarity
    conf = 0
    claims = [n for n in nodes.values() if n["type"] == "claim"]
    ent_of_claim: dict[str, set[str]] = {}
    for e in edges:
        if e["rel"] == "mentions":
            tgt = nodes.get(e["to"])
            if tgt:
                ent_of_claim.setdefault(e["from"], set()).add(tgt["name"])
    pos_rx, neg_rx = (re.compile(rx) for rx in CONFLICT_PAIRS[0])
    # -- conflict edges: curated contradictions (from master index, verified by
    # the forensic audit) + conservative same-entity cross-role polarity pairs.
    conf = 0
    claims = [n for n in nodes.values() if n["type"] == "claim"]
    ent_of_claim: dict[str, set[str]] = {}
    for e in edges:
        if e["rel"] == "mentions":
            tgt = nodes.get(e["to"])
            if tgt:
                ent_of_claim.setdefault(e["from"], set()).add(tgt["name"])
    pos_rx, neg_rx = (re.compile(rx) for rx in CONFLICT_PAIRS[0])

    def pol(c):
        t = c["text"].lower()
        p, n = bool(pos_rx.search(t)), bool(neg_rx.search(t))
        P, A = p and not n, n and not p
        if P == A:
            A, P = n, False
        return P, A

    def find(phrase):
        return [c for c in claims if phrase.lower() in c["text"].lower()]

    CURATED = [
        ("no on-premise", "Dell PowerEdge R740"),                      # C1 cloud-only vs on-prem server
        ("dedicated SIEM", "SIEM, alerting"),                          # C2 SIEM vs cloud-native logging
        ("Solsphere AI Inc", "dba"),                                   # C3 legal identity
        ("Revoke access", "revoked promptly"),                          # C4 offboarding lag
        ("no restore or recovery test", "Automated daily backups"),    # C4b backups untested
    ]
    for pa, pb in CURATED:
        for a in find(pa):
            for b in find(pb):
                if a["id"] == b["id"]:
                    continue
                edges.append({"from": a["id"], "to": b["id"], "rel": "potential_conflict",
                              "curated": True, "cross_role": a["role"] != b["role"]})
                conf += 1

    # conservative automatic layer: cross-role, opposing polarity, SHARED entity only
    for i, a in enumerate(claims):
        a_pol, a_abs = pol(a)
        if not (a_pol or a_abs):
            continue
        ea = ent_of_claim.get(a["id"], set())
        if not ea:
            continue
        for b2 in claims[i + 1:]:
            if a["role"] == b2["role"]:
                continue
            b_pol, b_abs = pol(b2)
            if a_pol == b_pol and a_abs == b_abs:
                continue
            eb = ent_of_claim.get(b2["id"], set())
            if ea & eb:
                edges.append({"from": a["id"], "to": b2["id"], "rel": "potential_conflict",
                              "cross_role": True})
                conf += 1

    kg = {
        "meta": {"nodes": len(nodes), "edges": len(edges), "claims": claim_count,
                 "conflict_edges": conf,
                 "note": "claims carry source locators into blocks.jsonl; entity/topic edges drive retrieval"},
        "nodes": list(nodes.values()),
        "edges": edges,
    }
    OUT.write_text(json.dumps(kg, indent=1))
    # flat BM25-ready index: claim lines with enriched context
    with open(OUT_IDX, "w") as f:
        for c in claims:
            ents = sorted(ent_of_claim.get(c["id"], []))
            line = {"id": c["id"], "text": c["text"], "source": c["source"],
                    "locator": c["locator"], "role": c["role"], "topic": c.get("topic"),
                    "entities": ents}
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
    print(f"KG: {len(nodes)} nodes, {len(edges)} edges, {claim_count} claims, {conf} potential-conflict edges")
    print(f"-> {OUT}\n-> {OUT_IDX}")




if __name__ == "__main__":
    build()
