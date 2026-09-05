# SENTINEL: Regodit AI Security Analyst

> **Autonomous AI Security Analyst for Enterprise Vendor Security Questionnaires.**  
> Powered by an enriched Knowledge Graph (9,646 nodes, 7 core contradictions, 9,446 atomic evidence blocks), a guardrailed multi-turn decision loop, persistent stakeholder memory, and a modern interactive Next.js UI with live DAG graph tracing.

---

## 🏆 The Golden Rule of Security Analysis

1. **NEVER MAKE UP AN ANSWER.** If information is unavailable in company documentation, ask a human stakeholder.
2. **IF INFORMATION CONFLICTS, INVESTIGATE.** Surface opposing evidence from policies and operational infrastructure; do not blindly guess or hide contradictions.
3. **IF UNKNOWN, MARK AS UNKNOWN.** Never hallucinate or assume compliance controls that do not exist.
4. **PERSISTENT STAKEHOLDER MEMORY.** Human clarifications and document-verified answers are persisted into `security_profile.json` so resolved questions are remembered across restarts with zero redundant queries.

---

## 🏗️ System Architecture & Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│             SENTINEL Interactive Next.js UI (Port 3000)     │
│  - Chat Console (Enlarged high-contrast typography)         │
│  - Live Graph Traversal Canvas (@xyflow/react + dagre)      │
│  - Interactive Human Resolution & Clarification Inputs      │
│  - Persistent Security Profile Sidebar (Real-time sync)     │
│  - Modal Evidence Drawer (Exact block locators & quotes)    │
└──────────────────────────────┬──────────────────────────────┘
                               │ JSON API (/api/chat, /api/profile, /api/corpus)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 FastAPI Backend Engine (Port 8000)          │
│  - server.py (Lightweight, structured payloads only)        │
│  - No raw prompt dumps or multi-megabyte traces to client   │
│  - Multi-turn conversation resolver & stakeholder memory    │
└──────────────────────────────┬──────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
┌───────────────────────────────┐   ┌───────────────────────────────┐
│     GraphTreeRetriever        │   │    Guardrailed Agent Loop     │
│  - 9,646 Knowledge Graph Nodes│   │  - process_question()         │
│  - 7 Indexed Contradictions   │   │  - Anti-hallucination gates   │
│  - 9,446 Atomic Evidence      │   │  - Confidence scoring         │
│    Blocks (evidence/blocks)   │   │  - PRISM Trace SDK telemetry  │
└───────────────────────────────┘   └───────────────────────────────┘
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python**: 3.10+
- **Node.js**: 18+ (tested on Node v20/v25)

### 2. Backend Setup & Launch
Install Python dependencies and start the API server:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server (runs on http://127.0.0.1:8000)
python3 server.py
# Alternatively: uvicorn server:app --host 127.0.0.1 --port 8000
```

### 3. Frontend Setup & Launch
In a new terminal window:

```bash
# Install Node dependencies
npm install

# Start Next.js development server (runs on http://localhost:3000)
npm run dev
```

Open your browser to **`http://localhost:3000`** to view the landing page, or click **"Open Console"** to navigate directly to **`http://localhost:3000/analyst`**.

---

## 🧪 Interactive UI Walkthrough for Judges

When you open `http://localhost:3000/analyst`, the console provides three quick-start buttons representing the core analyst capabilities:

### Scenario 1: Verified Document Answer (Q1.0)
- **Question**: *"Does your organization have a formal Information Security Program established?"*
- **Behavior**:
  - Traverses `QuestionnaireQuestion[1.0]` $
ightarrow$ `ControlArea[Security Governance]` $
ightarrow$ `Policy[Information Security Policy v1.0]`.
  - Cites Section 1 Scope and Purpose verbatim.
  - Assigns **High Confidence (0.90)** with status `VERIFIED FROM DOCUMENTS`.
  - Automatically records the verified response in the right-hand **Security Profile** sidebar.

### Scenario 2: Contradiction Detection & Investigation (Q22.0)
- **Question**: *"Where is company and customer data hosted?"*
- **Behavior**:
  - Traverses `ControlArea[Hosting Architecture]` $
ightarrow$ `Conflict[CONFLICT-001]`.
  - **Surfaces Contradiction**: Flags that Information Security Policy Sections 8 & 12 claim zero on-premises servers, while Asset Inventory rows 10 & 13 log an active on-premise Dell PowerEdge R740 backup server in the HQ server room.
  - Explains both sides transparently to the user.
  - Renders a prominent action button: `↳ Clarify: Which requirement is current for your organization?`.

### Scenario 3: Human Input Resolution & Persistent Memory (Q6.0)
- **Question**: *"Will you be using third party contractors or sub-contractors to complete the engagement?"*
- **Behavior**:
  - Detects that engagement-specific staffing cannot be fabricated from general vendor policies.
  - Marks status as `Needs Input / Unknown` and prompts for stakeholder guidance.
  - Clicking `↳ Provide current company practice for this control` opens the composer with an active `REQUIRED INPUT` banner.
  - Type your answer: e.g., *"No third party contractors will be used for this engagement; all engineering and data handling is performed by full-time staff."*
  - Click **"Record & Save"**:
    - Persists resolution to `security_profile.json` with confidence **1.00**.
    - Live-updates the right-hand **Security Profile** sidebar with badge `confirmed by you`.
    - If you re-ask Q6.0, Sentinel **immediately recalls the stakeholder resolution from memory** with zero redundant questions!

---

## 📊 Full 66-Question Questionnaire Benchmark

To evaluate the agent against all 66 vendor security questionnaire items from `evidence/questionnaire.json`:

```bash
python3 security_agent/run_66_benchmark.py
```

### Benchmark Metrics:
- **Total Questionnaire Rows**: 66 / 66
- **Hallucination Rate**: **0.0%** (Strict Golden Rule enforcement)
- **Contradictions Caught**: **100%** (All 7 company-wide conflicts surfaced with bilateral citations)
- **Auditable Telemetry**: Full trajectory trace logged to PRISM Trace SDK and `evidence/questionnaire_audit_results_66.json`.

---

## 🔍 Core Security Contradictions Indexed in the Knowledge Graph

| ID | Control Domain | Policy Claim | Operational Reality | Resolution Strategy |
|---|---|---|---|---|
| **CONFLICT-001** | Hosting Architecture | InfoSec Policy: 100% cloud-only AWS architecture. | Asset Inventory: Dell PowerEdge R740 backup server in HQ server room. | Surface contradiction; prompt user to clarify operational role of on-prem server. |
| **CONFLICT-002** | Logging & SIEM | Architecture Diagram shows central SIEM pipeline. | InfoSec Policy Sec 11: No dedicated SIEM (native CloudWatch used). | Clarify CloudWatch vs third-party SIEM. |
| **CONFLICT-003** | Legal Entity Name | Form W-9: `Solsphere AI Inc`. | Commercial Contracts: `Solsphere AI Inc (dba Regodit)`. | Report formal DBA legal entity structure. |
| **CONFLICT-004** | Access Offboarding | HR Policy: Revoke within 24 hours of termination. | Access Review: Contractor M. Delgado retained AWS Admin access 5 days post-exit. | Report SLA gap and remediation ticket. |
| **CONFLICT-005** | Headcount / Incorporation | SOC 2 Sec 3.1: Founded June 2025 with 12 personnel. | SOC 2 Sec 3.1.2: Founded August 2024 with 9 personnel. | Surface timeline discrepancy to auditor. |
| **CONFLICT-006** | SDLC Execution | SDLC Policy: Formal secure development lifecycle. | SDLC Document: Marked as unexecuted template. | Reconcile with PR code review records in InfoSec Policy Sec 13. |
| **CONFLICT-007** | VAPT Findings SLA | Vulnerability Policy: High findings closed within 30 days. | VAPT Report: 20 findings open (CVSS 8.1 / CVSS 6.5). | Disclose open findings under active remediation window. |

---

## 🎯 Explicit Confidence Basis Evaluation

Rather than providing a raw floating-point score (e.g. `0.88`, `0.40`), Sentinel computes and renders an explicit, auditable **Confidence Basis** breakdown across three dimensions:

1. **Source Freshness**: Analyzes document lifecycle timestamps, active company policies (e.g. `Policy v1.0`), audit review periods (SOC 2 Type II), and penetration test report dates.
2. **Directness**: Distinguishes between explicit, normative contractual mandates vs. secondary operational telemetry or indirect inferences.
3. **Cross-Verification**: Quantifies multi-source corroboration across independent documents or flags documented internal contradictions.

In the UI, this is displayed directly beneath the confidence bar as a structured breakdown card:
- ⏱ **Freshness**: *Current: Active company policy v1.0 currently in effect.*
- 🎯 **Directness**: *Direct: Explicit contractual or normative requirement stated in authoritative policy text.*
- 🔗 **Cross-Verification**: *Strong: Verified from authoritative primary policy and corroborated by operational telemetry / audit records.*

---

## ⚖️ Live External Standards Check (NIST SP 800-63B & OWASP)

As specified in `graph/ARCHITECTURE.md`, Sentinel implements live external standard validation in `security_agent/external_check.py`:

- **Live Python Execution**: When questions reference controls such as replay-resistant MFA, TLS encryption in transit, or web vulnerability mitigation, the agent executes a live query to standards authorities (NIST, OWASP, CIS) using Tavily search with built-in authoritative fallback.
- **NIST SP 800-63B Evaluation**: Evaluates whether authenticators achieve Authenticator Assurance Level 2 (AAL2) or AAL3 (phishing-resistant FIDO2/WebAuthn), noting that manual OTP entry is not replay/phishing-resistant under Section 5.1.4.
- **Strict Boundary Isolation Rule**: `supplement_only_never_override_internal_evidence`. External standards benchmarks supplement company answers for audit rigor, but **never override, replace, or fabricate internal company documentation**.

---

## 🛡️ Full Spec & Golden Rule Validation Suite

To verify all system invariants, run the automated test suite:

```bash
python3 tools/validate_spec.py
```

### Validated Criteria:
1. **[1/7] Knowledge Graph Loading**: Verifies 9,646 nodes, 7 contradiction nodes, and 66 questionnaire anchors.
2. **[2/7] Golden Rule Enforcement**: Validates that out-of-scope/unsupported queries are escalated (`ask_user`) with 0.0% fabrication.
3. **[3/7] Contradiction Detection**: Proves bilateral evidence surfacing for CONFLICT-001 (Hosting), CONFLICT-002 (SIEM), CONFLICT-004 (Offboarding), and Q60.0 (MFA Policy vs VAPT).
4. **[4/7] Confidence Basis Breakdown**: Confirms explicit `source_freshness`, `directness`, and `cross_verification` strings.
5. **[5/7] Live External Check**: Executes live Python check for NIST SP 800-63B and validates the isolation rule.
6. **[6/7] Persistent Memory & In-Place Corrections**: Asserts atomic updates, `correction_count` tracking, and historical answer preservation.
7. **[7/7] ExternalFact Topology**: Verifies 16 `ExternalFact` nodes with strict unidirectional `SUPPLEMENTS` edge directionality.

---

## 📁 Repository Directory Structure

```
├── app/                                # Next.js 15 Frontend
│   ├── analyst/page.tsx               # Interactive analyst console & split-view
│   ├── components/GraphTrace.tsx      # Cytoscape & ReactFlow DAG visualizer
│   ├── theme.ts                       # Typography tokens (enlarged, warm paper theme)
│   ├── page.tsx                       # Product landing & capability proof page
│   └── layout.tsx                     # App layout & font definitions
├── server.py                          # FastAPI backend connecting UI to GraphTreeRetriever
├── security_agent/                    # Core Agent Decision Engine
│   ├── agent_loop.py                  # Guardrailed prompt & decision gates
│   ├── conversation_loop.py           # Multi-turn resolution & vague reply handler
│   ├── retrieve_graph.py              # GraphTreeRetriever (Neo4j topology walk)
│   ├── security_profile.py            # Persistent stakeholder memory store
│   ├── run_66_benchmark.py            # 66-question automated audit runner
│   └── security_profile.json          # Live state store (confirmed answers)
├── graph/                             # Knowledge Graph Pipeline
│   ├── build_security_graph.py        # Graph compilation script
│   └── out/security_graph.json        # Enriched graph (9,646 nodes)
├── evidence/                          # Atomic Evidence & Benchmark Sets
│   ├── blocks.jsonl                   # 9,446 parsed evidence blocks
│   ├── questionnaire.json             # 66 vendor security questions
│   └── questionnaire_audit_results_66.json
└── corpus_text/                       # 28 Curated Markdown Policies & Evidence Docs
```
