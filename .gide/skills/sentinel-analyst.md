# Project: SENTINEL ANALYST (Next.js + TypeScript)

## Flow
Company Docs + Policies + Infra + Messages + Employees
  -> SEARCH ALL EVIDENCE FIRST
  -> VERIFIED | CONFLICT | UNKNOWN
       CONFLICT -> ask clarification
       UNKNOWN  -> ask user
  -> Persistent Security Profile
  -> Completed Questionnaire
  -> every line carries EVIDENCE + CONFIDENCE + SOURCE

## THE GOLDEN RULE — enforced by types and code, never by prompt
VERIFIED requires >=1 evidence ID that resolves to a real chunk. Empty or
unresolvable evidence -> code downgrades to UNKNOWN. The LLM proposes, code decides.
Never fabricate. UNKNOWN is a correct answer.

## Source types and precedence (drives conflict detection)
type SourceType = "policy" | "infra" | "doc" | "message" | "employee";
Precedence: policy(5) > infra(4) > doc(3) > message(2) > employee(1)
A CONFLICT is two chunks that disagree. When precedence differs, the reply states the
higher-precedence source as the nominal answer and asks the user to confirm currency.
Example: policy says MFA mandatory, a message implies someone lacks it -> CONFLICT.

## Evidence ID format (non-negotiable)
`<filename>:L<start>-L<end>` — must resolve via GET /api/evidence/[id]

## Verdict statuses (LLM returns 3)
VERIFIED | CONFLICT | UNKNOWN

## Profile statuses (stored, 4)
verified | user_confirmed | conflict | unknown

## Architecture rules
- Retrieval, citation resolution, precedence, status classification: deterministic TS.
- LLM only: phrasing, spotting disagreement, writing follow-ups.
- Strict JSON from every LLM call. Parse fail -> one retry -> UNKNOWN.
- Secrets server-side only. Never NEXT_PUBLIC_ for keys.

## Stack
Next.js App Router, TypeScript, module-level Map store, no DB, no retrieval library,
inline styles, local dev only.

## Files
lib/corpus.ts  lib/retriever.ts  lib/verdict.ts  lib/store.ts  lib/analyst.ts
lib/prism.ts  app/api/chat/route.ts  app/api/questionnaire/route.ts
app/api/evidence/[id]/route.ts  app/page.tsx
