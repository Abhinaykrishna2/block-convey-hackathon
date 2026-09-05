# AI x FINANCE HACKATHON — 💸 MONEY TALKS
**Official Memory & Project Blueprint: Regodit AI Security Analyst**

## 0. Standing Directive
**Always think from an enterprise CISO & auditor perspective.** The best AI Security Analyst is not the one that asks the most questions; it is the one that finds information before asking, asks the right follow-ups, remembers what it learns, detects contradictions, never confidently makes things up, and gets the questionnaire completed.

---

## 1. Executive Summary & Core Mission
- **Track:** Regodit Track — AI Security Analyst
- **The Problem:** A startup preparing to sell to a large enterprise receives a complex security questionnaire. Answers are scattered across company policies, infrastructure diagrams, employee records, internal audit reports, and human knowledge. The information is incomplete, ambiguous, and contradictory.
- **The Mission:** Build an autonomous AI Security Analyst that talks to a company employee, investigates scattered enterprise artifacts, resolves conflicts, and completes the 66-question vendor security questionnaire with verifiable evidence.

---

## 2. Event Logistics & Tech Stack
- **Event:** AI x Finance Hackathon — Money Talks (NYC Financial District)
- **Mandatory Sponsor Integration (Gold Rule):** **PRISM by Block Convey** (`prismtrace-sdk`) — Execution spine tracing all agent reasoning and tool trajectories.
- **External Web Grounding:** **Tavily** (`TAVILY_API_KEY`) for NIST SP 800-63B and Delaware entity checks.
- **Control Assurance:** **Prelint** for deterministic rule validation.
- **Voice UX:** **ElevenLabs** for conversational audio.

---

## 3. 🌟 The Golden Rule
> **NEVER MAKE UP AN ANSWER.**
> - If information is unavailable, **ask**.
> - If information conflicts, **investigate**.
> - If the answer remains unknown, **mark it as unknown**.

---

## 4. Official Hackathon Scoring Rubric & Judging Criteria

Judges evaluate the analyst on operational fidelity, not verbosity:
> *"The best AI Security Analyst is NOT the one that asks the most questions. It is the one that finds information before asking, asks the right follow-ups, remembers what it learns, detects contradictions, never confidently makes things up, and gets the questionnaire completed."*

### Core Evaluation Pillars
1. **Search Before Asking:** Exhaust internal corpus (`corpus_text/`, `evidence/blocks.jsonl`) before prompting the user. Every documented answer must cite exact source evidence and XML/cell locators.
2. **Ask When Missing (No Hallucinations):** If a control has no internal documentation (e.g. Q61 NIST SP 800-63B authenticator assurance levels), prompt the human stakeholder and record their answer.
3. **Ask Smart Follow-Ups:** Refuse vague answers (e.g., if user says "Yes, backups are done", follow up on frequency, automation, and whether restoration tests were performed).
4. **Detect and Resolve Conflicts:** Flag discrepancies proactively (e.g. AWS-only vs on-prem Dell server, HR immediate offboarding vs Delgado 5-day AWS Admin lag).
5. **Remember Everything:** Maintain a persistent, loop-updating security profile. Never ask the same question twice. Allow prior claims to be updated with revision history.
6. **Complete the 66-Question Benchmark:** Generate the completed questionnaire distinguishing:
   - `VERIFIED_FROM_CORPUS` (Green)
   - `USER_CONFIRMED` (Blue)
   - `RESOLVED_CONFLICT` (Orange/Yellow)
   - `UNKNOWN / NEEDS_CONFIRMATION` (Gray)

### 🏆 Bonus Points Checklist (Targeted Extra Credit)
- [x] **Excellent Conversational UX:** Clean interactive interface with clear citation badges and smart follow-up prompts.
- [x] **Persistent Memory:** Profile schema retaining `answer`, `status`, `scope`, `source_locator`, `source_date`, `confirmed_by`, `unresolved_conflict`, and `revision_history`.
- [x] **Conflict Detection Engine:** Pre-indexed contradiction playbook (7 core contradictions) with automated conflict triggers.
- [x] **Verifiable Evidence for Every Answer:** Exact document name, section, XML paragraph locator, or Excel cell coordinate.
- [x] **Confidence Scores with Stated Basis:** Confidence explained via source quality, specificity, freshness, and consistency (never an arbitrary percentage).
- [x] **Intelligent Follow-Up Questions:** Drilling into partial answers and unobservable operational reality.
- [x] **Prioritizing Important Unanswered Questions:** High/Critical risk domains (Production Access, Data Encryption, Vuln Mgmt, Incident Response) prioritized first.
- [x] **User Corrections & Updates:** Dynamically updating the knowledge graph when an employee provides new facts.
- [x] **Multiple Stakeholder Routing:** Directing questions to the appropriate role (IT/CISO for AWS/MFA, HR for offboarding, Leadership for entity structure).
- [x] **Automatic Questionnaire Generation:** Instant export of completed 66-question matrix with audit pack.
- [x] **Voice Interaction (ElevenLabs):** Spoken audio prompts for conversational engagement.
- [x] **PRISM Traceability (Mandatory Execution Spine):** Every agent step, tool call, reasoning span, and verdict submitted to Block Convey PRISM (`submit_trajectory`).
- [x] **Tavily External Grounding:** Real-time web evidence for external standards (NIST SP 800-63B, Delaware corporate registry).
- [x] **Prelint Code Assurance:** Automated validation of deterministic security rules against spec.

---

## 5. Knowledge Graph Architecture

The AI Analyst constructs and queries an in-memory heterogeneous Knowledge Graph:

```
 (Policy: Access Control v1.0) ──enforces──► (Control: Mandatory MFA) ◄──depicts── (Diagram: Admin Access PNG)
                                                    │
                                             verified_across
                                                    ▼
                                            (Target: AWS IAM, GitHub, GSuite)

 (Policy: InfoSec Sec 12) ──states──► (Architecture: 100% Cloud-Only AWS)
                                                    ▲
                                             conflicts_with (C1)
                                                    ▼
 (Record: Asset Inventory) ──logs───► (Hardware: Dell PowerEdge R740 On-Prem) ◄── Epistemic Bridge (Ask Employee)

 (Record: Access Review) ──flags───► (Contractor: M. Delgado - 5-day lag) ◄── Epistemic Bridge (Verify Revocation)
```

### Knowledge Graph Node Types:
- **PolicyNode:** Approved governance documents (`role: documented_policy`).
- **OperationalRecordNode:** Access reviews, asset inventories (`role: operational_record`).
- **TemplateNode:** Drafts and unexecuted frameworks (`role: template_with_placeholders`).
- **ControlNode:** Specific security requirements (MFA, AES-256, Daily Backups).
- **ConflictEdge:** Explicit contradictory claims triggering the investigation loop.
- **EvidenceLocator:** Immutable SHA-256 and XML paragraph/cell pointer in `evidence/blocks.jsonl`.

