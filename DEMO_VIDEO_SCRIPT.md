# 🎬 SENTINEL AI Security Analyst — 60 to 90 Second Demo Video Script

**Live URL to Open in Browser:** http://localhost:3000/analyst  
**Target Duration:** 1 minute 15 seconds to 1 minute 30 seconds  
**Tone:** Confident, fast-paced, high-conviction security expert.

---

## ⏱ Timeline & Step-by-Step Recording Actions

### 🕒 0:00 – 0:15 | The Hook & Golden Rule
- **Screen Action:** Open `http://localhost:3000/analyst`. Show the clean 3-pane interface: Chat Console on the left, Live DAG Knowledge Graph on the right, and the Persistent Security Profile memory store.
- **Speak:**  
  > *"Welcome to Sentinel, our autonomous AI Security Analyst for vendor security reviews.  
  > In compliance, the Golden Rule is absolute: **Never make up an answer. If information conflicts, investigate. If unknown, ask the team with recommendations.**  
  > Powered by a 9,646-node Knowledge Graph and live standards checks, Sentinel retrieves grounded evidence, detects contradictions, and asks targeted back-questions with industry recommendations."*

---

### 🕒 0:15 – 0:35 | Step 1: Retrieval & Conversational Answering
- **Screen Action:** Click the prompt or type:  
  👉 `🔒 How do we encrypt customer data in transit and at rest?`  
  Wait 1 second for the instant response.
- **Screen Action:** Point the cursor at:
  1. The natural, executive-ready explanation of TLS 1.2/1.3 and AES-256 KMS encryption.
  2. The **Confidence Basis** breakdown card: *Freshness (Policy v1.0)*, *Directness (Normative requirement)*, and *Cross-Verification*.
  3. The **Live Graph Trace** showing the DAG path from Query -> ControlArea -> Policy.
- **Speak:**  
  > *"When we ask how customer data is encrypted, Sentinel retrieves our authoritative policies and infrastructure records in real-time. It explains our TLS 1.3 and AES-256 KMS standards, cites exact verbatim document blocks, and provides an auditable 3-part Confidence Basis—never a raw, unexplained number."*

---

### 🕒 0:35 – 1:05 | Step 2: Contradiction Detection & Back-Question with Recommendation
- **Screen Action:** Click the prompt or type:  
  👉 `🏢 Where is company and customer data hosted?` *(or offboarding / SIEM)*  
  Wait for the response.
- **Screen Action:** Point the cursor at:
  1. The surfaced discrepancy: Policy claims 100% AWS Cloud, but Asset Inventory logs an on-prem Dell PowerEdge server in the HQ server room.
  2. The **Clarification Needed** card with the targeted clarifying question:  
     *"Does Regodit operate strictly on AWS cloud infrastructure, or is the on-premise Dell PowerEdge server still actively maintained for emergency backups?"*
  3. The **💡 Recommended Operational Standard**:  
     *"We recommend formally certifying 100% AWS cloud hosting and decommissioning or isolating the on-premises Dell server to eliminate the SOC 2 audit discrepancy."*
- **Speak:**  
  > *"Now see what happens when internal company records conflict. Asking about data hosting reveals CONFLICT-001: our InfoSec Policy declares 100% AWS cloud, but our physical Asset Inventory logs a Dell PowerEdge server in the HQ server room.  
  > Sentinel doesn't guess or sweep this under the rug. It explains both sides, asks us a targeted clarifying question, and provides an actionable compliance recommendation to decommission the on-prem server."*

---

### 🕒 1:05 – 1:25 | Step 3: One-Click Recommendation Acceptance & Persistent Memory
- **Screen Action:** 
  1. Click the **`✓ Accept Recommendation`** button right on the card!
  2. The answer is instantly recorded into the conversation and written to `security_profile.json`.
  3. Point to the right sidebar: Notice the newly confirmed record under **Security Profile**.
  4. Ask the same question again (or click the button). Sentinel immediately answers:  
     *"Confirmed by stakeholder: All production and customer data is hosted exclusively in AWS..."* with zero redundant questions!
- **Speak:**  
  > *"With a single click, I can **Accept the Recommendation**.  
  > Sentinel immediately writes our stakeholder decision into persistent memory. When we ask the question again, Sentinel recalls our confirmed standard instantly. It never asks the same question twice."*

---

### 🕒 1:25 – 1:35 | Outro & Spec Validation Scorecard
- **Screen Action:** Show the terminal running `python3 tools/validate_spec.py` with all 7 criteria passing (100% compliance).
- **Speak:**  
  > *"Across all 66 vendor questionnaire controls, Sentinel maintains **0.0% hallucinations**, surfaces **100% of documented contradictions**, and empowers teams with intelligent recommendations. That's true enterprise security intelligence. Thank you!"*

---

## 📋 Copy-Paste Cheat Sheet for Recording

### Question 1 (Data Encryption):
```text
How do we encrypt customer data in transit and at rest?
```

### Question 2 (Contradiction & Recommendation):
```text
Where is company and customer data hosted?
```

### Question 3 (Vendor / Contractor Governance):
```text
Will we be using third-party contractors for development?
```
