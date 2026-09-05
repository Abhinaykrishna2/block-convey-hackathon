# Regodit Track: AI Security Analyst Knowledge Corpus

This repository houses the complete, curated, and multi-modal verified security and compliance corpus for the Regodit Track: AI Security Analyst.

## 📁 Repository Structure

- **`Hackathon/`**: The original source files across 5 categories:
  - `1. Sample_Vendor questionnaire/`
  - `2. Company policies/`
  - `3. Security Assessment Reports/`
  - `4. Contracts_agreements/`
  - `5. Infrastructure_internal info/`
- **`corpus_text/`**: The primary knowledge base organized into 6 clean, modular subdirectories containing **28 curated markdown documents** and master indices:
  - `00_INDEX/`: `master_corpus_index.json` (machine-readable knowledge graph) and `MASTER_CORPUS_INDEX.md` (comprehensive index & conflict guide).
  - `01_SAMPLE_VENDOR_QUESTIONNAIRE/`: Curated questionnaire (66 questions) and 4x4 risk matrix heatmap/ranges.
  - `02_COMPANY_POLICIES/`: All 13 core organizational security policies.
  - `03_SECURITY_ASSESSMENT_REPORTS/`: SOC 2 Type II report, CPA auditor attestation & badges, and VAPT report.
  - `04_CONTRACTS_AGREEMENTS/`: Employment and Master Services agreements.
  - `05_INFRASTRUCTURE_INTERNAL_INFO/`: Architectural diagrams, privileged access pathways, asset inventory, access reviews, BCP/DR plans, and Form W-9.
- **`extracted_media/`**: Clean visual assets extracted directly from source files for multi-modal verification.
- **`verify_corpus.py`**: Automated verification test suite validating file integrity, non-emptiness, and retrieval coverage across the 7 core questionnaire questions.

## 🚀 Verification Suite

To verify that all raw sources, scraped visual flowcharts, and index files are 100% complete and consistent:

```bash
python3 verify_corpus.py
```

## 🔍 Core Security Contradictions Indexed for AI Agents

1. **On-Premise Infrastructure**: Information Security Policy specifies cloud-only AWS; Asset Inventory logs an on-premise Dell PowerEdge R740 backup server in an HQ server room.
2. **Centralized Logging / SIEM**: Architecture diagrams show SIEM pipeline; Information Security Policy Section 11 notes no dedicated SIEM currently exists (cloud-native CloudWatch/S3 logging is used).
3. **Legal Entity Name**: Form W-9 lists `Solsphere AI Inc` (Delaware C-Corp); contracts clarify `Solsphere AI Inc (dba Regodit)`.
4. **Offboarding Lag**: HR Policy mandates immediate deprovisioning; Access Review shows contractor M. Delgado retained AWS Admin credentials 5 days post-hardware offboarding.
5. **SOC 2 Report Metadata**: Section 3.1 states June 2025 incorporation with 12 personnel; Section 3.1.2 states August 2024 with 9 personnel.
6. **SDLC Document Status**: Standalone SDLC 01 document is an unexecuted template; actual engineering controls (PR review, approvals) are governed by Information Security Policy Section 13.
7. **VAPT Pen Test Status**: Latest test identified 20 vulnerabilities (High CVSS 8.1 Missing Auth, CVSS 6.5 Prompt Injection); ongoing remediation under 30-day High SLA.
