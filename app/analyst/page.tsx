"use client";
import { useEffect, useRef, useState } from "react";
import GraphTrace, { type Trace } from "../components/GraphTrace";
import { css } from "../theme";

type Status =
  | "answered" | "conflict" | "ask_user" | "insufficient"
  | "confirmed" | "remembered";
type Citation = { id: string; source: string; quote?: string; sourceType?: string };
type Answering = { questionId: string; question: string; followUp: string };
type Message = {
  id: string;
  role: "user" | "assistant";
  text: string;
  status?: Status;
  confidence?: number;
  confidenceBasis?: {
    source_freshness: string;
    directness: string;
    cross_verification: string;
    summary: string;
  };
  externalCheck?: {
    standard: string;
    title: string;
    url: string;
    benchmark_summary: string;
    provider: string;
  };
  citations?: Citation[];
  graphTrace?: Trace;
  pending?: boolean;
  followUp?: string | null;
  clarifyingQuestion?: string | null;
  recommendation?: string | null;
  recommendationAction?: string | null;
  questionId?: string;
  asked?: string;
};

type ProfileRecord = {
  question_id: string;
  question_text: string;
  status: string;
  answer?: string | null;
  confidence?: number | null;
  correction_count?: number;
  updated_at?: string;
};
type Profile = {
  total_questions: number;
  corrected_count: number;
  questions: Record<string, ProfileRecord>;
};

const STATUS_META: Record<string, { label: string; color: string }> = {
  answered: { label: "From documents", color: "#10b981" },
  conflict: { label: "Conflict", color: "#f59e0b" },
  ask_user: { label: "Needs input", color: "#64748b" },
  insufficient: { label: "Needs input", color: "#64748b" },
  confirmed: { label: "Confirmed by you", color: "#9a5b32" },
  remembered: { label: "From memory", color: "#7c6a9a" },
};

const RECORD_META: Record<string, { label: string; color: string }> = {
  verified_from_documents: { label: "from documents", color: "#4f8a5b" },
  confirmed_by_user: { label: "confirmed by you", color: "#9a5b32" },
};

const CHIP: Record<string, string> = {
  policy: "var(--pol)", infra: "var(--inf)", doc: "var(--doc)",
  message: "var(--msg)", employee: "var(--emp)",
};

export default function Analyst() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [open, setOpen] = useState<Record<string, boolean>>({});
  const [drawer, setDrawer] = useState<{ id: string; text: string; sourceType?: string } | null>(null);
  const [corpus, setCorpus] = useState<{
    ready: boolean;
    documentCount: number;
    chunkCount: number;
    graphNodes?: number;
    conflicts?: number;
  } | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [answering, setAnswering] = useState<Answering | null>(null);
  const endRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const loadProfile = () =>
    fetch("/api/profile")
      .then((r) => r.json())
      .then(setProfile)
      .catch(() => undefined);

  useEffect(() => {
    void fetch("/api/corpus")
      .then((r) => r.json())
      .then(setCorpus)
      .catch(() => setCorpus({ ready: false, documentCount: 0, chunkCount: 0 }));
    void loadProfile();
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function send(text?: string) {
    const message = (text ?? draft).trim();
    if (!message || busy) return;
    setDraft("");
    const resolving = answering;
    setAnswering(null);
    const history = messages
      .filter((m) => !m.pending)
      .map((m) => ({ role: m.role, text: m.text }));
    const pendingId = `a-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      { id: `u-${Date.now()}`, role: "user", text: message },
      {
        id: pendingId,
        role: "assistant",
        text: resolving ? "recording your answer…" : "querying the security graph…",
        pending: true,
      },
    ]);
    setBusy(true);
    try {
      const headers = { "Content-Type": "application/json" };
      const chatP = fetch("/api/chat", {
        method: "POST",
        headers,
        body: JSON.stringify({ message, history, answering: resolving }),
      });
      // Resolutions are recorded, not retrieved - no graph to trace.
      if (!resolving) {
        void fetch("/api/trace", {
          method: "POST",
          headers,
          body: JSON.stringify({ message }),
        })
          .then((r) => r.json())
          .then((d: { graphTrace?: Trace }) => {
            if (!d.graphTrace) return;
            setMessages((prev) => prev.map((m) => (
              m.id === pendingId ? { ...m, graphTrace: d.graphTrace } : m
            )));
          })
          .catch(() => undefined);
      }

      const r = await chatP;
      if (!r.ok) throw new Error(`chat ${r.status}`);
      const data = await r.json() as {
        reply: string;
        status?: Status;
        confidence?: number;
        confidenceBasis?: Message["confidenceBasis"];
        externalCheck?: Message["externalCheck"];
        citations?: Citation[];
        graphTrace?: Trace;
        followUp?: string | null;
        clarifyingQuestion?: string | null;
        recommendation?: string | null;
        recommendationAction?: string | null;
        questionId?: string;
      };
      setOpen((o) => ({ ...o, [pendingId]: true }));
      setMessages((prev) => prev.map((m) => (
        m.id === pendingId
          ? {
              id: pendingId,
              role: "assistant",
              text: data.reply,
              status: data.status,
              confidence: data.confidence,
              confidenceBasis: data.confidenceBasis,
              externalCheck: data.externalCheck,
              citations: data.citations ?? [],
              graphTrace: data.graphTrace ?? m.graphTrace,
              pending: false,
              followUp: data.followUp ?? null,
              clarifyingQuestion: data.clarifyingQuestion ?? null,
              recommendation: data.recommendation ?? null,
              recommendationAction: data.recommendationAction ?? null,
              questionId: data.questionId,
              asked: message,
            }
          : m
      )));
      void loadProfile();
    } catch {
      setMessages((prev) => prev.map((m) => (
        m.id === pendingId
          ? {
              id: pendingId,
              role: "assistant",
              text: "The analyst could not reach the security agent. Is the Python API running on port 8000?",
            }
          : m
      )));
    }
    setBusy(false);
  }

  async function openEvidence(id: string) {
    const r = await fetch(`/api/evidence/${encodeURIComponent(id)}`);
    const d = await r.json();
    setDrawer({ id, text: d.text ?? "Evidence not found.", sourceType: d.sourceType });
  }

  return (
    <div className="app">
      <style>{css}</style>
      <header>
        <div>
          <a href="/" style={{ fontSize: 14, color: "#8a8074", textDecoration: "none" }}>← Back</a>
          <div className="brand">SENTINEL <span>ANALYST</span></div>
          <div className="sub">
            Ask anything about this company&apos;s security posture
            {corpus?.ready
              ? ` · ${corpus.documentCount} docs · ${corpus.graphNodes ?? 0} graph nodes`
              : " · waiting for the security agent"}
          </div>
        </div>
      </header>

      <main>
      <div className="thread">
        {messages.length === 0 && (
          <div className="starters" style={{ padding: "36px 0 20px", alignItems: "flex-start", width: "100%" }}>
            <div className="eyebrow">Autonomous AI Security Analyst</div>
            <h2 style={{ margin: "0 0 8px", fontSize: "28px" }}>How can I assist with your security review?</h2>
            <p className="empty" style={{ marginBottom: "20px", maxWidth: "680px", lineHeight: 1.55 }}>
              Ask any question regarding our security posture, infrastructure, or compliance controls. I will retrieve grounded facts from our company corpus, detect contradictions, cite exact sources, and ask clarifying questions with actionable recommendations if anything is unclear.
            </p>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: "10px", width: "100%", maxWidth: "780px" }}>
              <button
                type="button"
                className="starter"
                onClick={() => void send("How do we encrypt customer data in transit and at rest?")}
              >
                🔒 <b>Data Encryption:</b> How do we encrypt in transit & at rest?
              </button>
              <button
                type="button"
                className="starter"
                onClick={() => void send("Where is company and customer data hosted?")}
              >
                🏢 <b>Hosting:</b> Where is customer data hosted and backed up?
              </button>
              <button
                type="button"
                className="starter"
                onClick={() => void send("Do we require replay-resistant multi-factor authentication?")}
              >
                🔐 <b>Authentication:</b> Do we require replay-resistant MFA?
              </button>
              <button
                type="button"
                className="starter"
                onClick={() => void send("Will we be using third-party contractors for development?")}
              >
                👥 <b>Vendors:</b> Will we be using third-party contractors?
              </button>
              <button
                type="button"
                className="starter"
                onClick={() => void send("What is our employee and contractor offboarding SLA?")}
              >
                ⏱ <b>Offboarding:</b> What is our access revocation SLA?
              </button>
              <button
                type="button"
                className="starter"
                onClick={() => void send("How are backups and disaster recovery tested?")}
              >
                💾 <b>BC/DR:</b> How are backups and disaster recovery tested?
              </button>
            </div>
          </div>
        )}
        {messages.map((m) => (
          m.role === "user" ? (
            <div key={m.id} className="turn">
              <div className="you">{m.text}</div>
            </div>
          ) : (
            <div key={m.id} className="turn">
              {m.pending ? (
                m.graphTrace
                  ? <GraphTrace trace={m.graphTrace} live />
                  : <div className="thinking"><i /><i /><i /><span>querying the security graph…</span></div>
              ) : (
                <div
                  className="ansbox"
                  style={{ ["--rail" as any]: STATUS_META[m.status ?? "ask_user"].color }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap", marginBottom: "8px" }}>
                    {m.status && (
                      <span className="badge" style={{ color: STATUS_META[m.status].color, borderColor: STATUS_META[m.status].color + "55" }}>
                        {STATUS_META[m.status].label}
                      </span>
                    )}
                    {m.confidence !== undefined && (
                      <span style={{ fontSize: "12.5px", color: "var(--tx2)", fontFamily: "ui-monospace, monospace" }}>
                        Confidence: <b>{Math.round(m.confidence * 100)}%</b>
                      </span>
                    )}
                    {m.externalCheck && (
                      <a
                        href={m.externalCheck.url}
                        target="_blank"
                        rel="noreferrer"
                        style={{
                          fontSize: "11.5px",
                          color: "var(--doc)",
                          border: "1px solid var(--doc)",
                          borderRadius: "99px",
                          padding: "2px 10px",
                          textDecoration: "none",
                          fontWeight: 600,
                          display: "inline-flex",
                          alignItems: "center",
                          gap: "4px",
                          background: "rgba(61,122,140,0.08)"
                        }}
                        title={m.externalCheck.benchmark_summary}
                      >
                        ⚖ Standard: {m.externalCheck.standard} ↗
                      </a>
                    )}
                  </div>
                  <p className="ans">{m.text}</p>
                  {m.confidenceBasis && (
                    <div style={{ marginTop: "12px", padding: "11px 15px", borderRadius: "9px", background: "rgba(44,38,30,0.035)", border: "1px solid var(--line)", fontSize: "13px" }}>
                      <div style={{ fontWeight: 700, fontSize: "11px", textTransform: "uppercase", letterSpacing: "0.09em", color: "var(--tx3)", marginBottom: "5px" }}>
                        Confidence Basis & Evidence Evaluation
                      </div>
                      <div style={{ color: "var(--tx2)", lineHeight: 1.6 }}>
                        <div><b>• Source Freshness:</b> {m.confidenceBasis.source_freshness}</div>
                        <div><b>• Directness:</b> {m.confidenceBasis.directness}</div>
                        <div><b>• Cross-Verification:</b> {m.confidenceBasis.cross_verification}</div>
                      </div>
                    </div>
                  )}
                  {m.externalCheck && (
                    <div style={{ marginTop: "10px", padding: "11px 15px", borderRadius: "9px", background: "rgba(61,122,140,0.06)", border: "1px solid rgba(61,122,140,0.25)", fontSize: "13px" }}>
                      <div style={{ fontWeight: 700, fontSize: "11px", textTransform: "uppercase", letterSpacing: "0.09em", color: "var(--doc)", marginBottom: "4px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <span>External Authority Standard Check: {m.externalCheck.standard}</span>
                        <span style={{ fontSize: "10px", opacity: 0.85, textTransform: "none" }}>{m.externalCheck.provider}</span>
                      </div>
                      <div style={{ color: "var(--tx)", lineHeight: 1.55 }}>
                        {m.externalCheck.benchmark_summary}
                      </div>
                    </div>
                  )}
                  {!!m.citations?.length && (
                    <div className="chips">
                      {m.citations.map((c) => (
                        <button key={c.id} className="chip" onClick={() => void openEvidence(c.id)}>
                          {c.sourceType && <em style={{ color: CHIP[c.sourceType] ?? "var(--acc2)" }}>{c.sourceType}</em>}
                          {c.source}
                        </button>
                      ))}
                    </div>
                  )}
                  {(m.clarifyingQuestion || m.recommendation) ? (
                    <div style={{
                      marginTop: "14px",
                      padding: "16px 18px",
                      borderRadius: "10px",
                      background: "rgba(194, 99, 44, 0.05)",
                      border: "1px solid rgba(194, 99, 44, 0.25)",
                    }}>
                      {m.clarifyingQuestion && (
                        <div style={{ marginBottom: "12px" }}>
                          <div style={{ display: "flex", alignItems: "center", gap: "6px", marginBottom: "5px" }}>
                            <span style={{ fontSize: "13px" }}>❓</span>
                            <b style={{ fontSize: "12px", color: "var(--acc2)", textTransform: "uppercase", letterSpacing: "0.07em" }}>
                              Clarification Requested
                            </b>
                          </div>
                          <div style={{ fontSize: "14px", color: "var(--tx)", fontWeight: 500, lineHeight: 1.5 }}>
                            {m.clarifyingQuestion}
                          </div>
                        </div>
                      )}

                      {m.recommendation && (
                        <div style={{
                          padding: "11px 14px",
                          borderRadius: "8px",
                          background: "rgba(255, 255, 255, 0.85)",
                          border: "1px solid rgba(194, 99, 44, 0.18)",
                          marginBottom: "13px",
                          fontSize: "13px",
                          lineHeight: 1.55,
                        }}>
                          <div style={{ fontWeight: 700, color: "#9a5b32", marginBottom: "3px", display: "flex", alignItems: "center", gap: "6px" }}>
                            <span>💡</span> Recommended Operational Standard:
                          </div>
                          <div style={{ color: "var(--tx2)" }}>
                            {m.recommendation}
                          </div>
                        </div>
                      )}

                      <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", alignItems: "center" }}>
                        {m.recommendationAction && (
                          <button
                            type="button"
                            style={{
                              background: "var(--acc2)",
                              color: "#fff",
                              border: "none",
                              borderRadius: "7px",
                              padding: "8px 16px",
                              fontSize: "13px",
                              fontWeight: 600,
                              cursor: "pointer",
                              display: "inline-flex",
                              alignItems: "center",
                              gap: "6px",
                              boxShadow: "0 1px 3px rgba(0,0,0,0.12)",
                            }}
                            onClick={() => {
                              setAnswering({
                                questionId: m.questionId || (m.status === "conflict" ? "conflict_resolution" : "ask_user"),
                                question: m.asked ?? m.text,
                                followUp: m.clarifyingQuestion || "Recommended standard",
                              });
                              void send(m.recommendationAction!);
                            }}
                          >
                            ✓ Accept Recommendation
                          </button>
                        )}

                        <button
                          type="button"
                          style={{
                            background: "transparent",
                            color: "var(--tx)",
                            border: "1px solid var(--line)",
                            borderRadius: "7px",
                            padding: "8px 14px",
                            fontSize: "13px",
                            fontWeight: 500,
                            cursor: "pointer",
                          }}
                          onClick={() => {
                            setAnswering({
                              questionId: m.questionId || (m.status === "conflict" ? "conflict_resolution" : "ask_user"),
                              question: m.asked ?? m.text,
                              followUp: m.clarifyingQuestion || "Clarify",
                            });
                            if (m.recommendationAction) {
                              setDraft(m.recommendationAction);
                            }
                            setTimeout(() => inputRef.current?.focus(), 60);
                          }}
                        >
                          ✎ Type Custom Answer
                        </button>
                      </div>
                    </div>
                  ) : m.followUp ? (
                    <button
                      type="button"
                      className="follow"
                      onClick={() => {
                        setAnswering({
                          questionId: m.questionId || (m.status === "conflict" ? "conflict_resolution" : "ask_user"),
                          question: m.asked ?? m.text,
                          followUp: m.followUp!,
                        });
                        setTimeout(() => inputRef.current?.focus(), 60);
                      }}
                    >
                      {m.followUp}
                    </button>
                  ) : null}
                  {m.graphTrace && (
                    <>
                      <button className="reveal" onClick={() => setOpen((o) => ({ ...o, [m.id]: !o[m.id] }))}>
                        {open[m.id] ? "▾" : "▸"} graph traversal · {m.graphTrace.nodes.length} nodes
                      </button>
                      {open[m.id] && <GraphTrace trace={m.graphTrace} />}
                    </>
                  )}
                </div>
              )}
            </div>
          )
        ))}
        <div ref={endRef} />
      </div>

      <aside>
        <h3>
          Security profile
          {!!profile?.total_questions && <span>{profile.total_questions}</span>}
        </h3>
        {profile?.total_questions
          ? Object.values(profile.questions)
              .sort((a, b) => (b.updated_at ?? "").localeCompare(a.updated_at ?? ""))
              .map((r) => {
                const meta = RECORD_META[r.status] ?? RECORD_META.confirmed_by_user;
                return (
                  <div key={r.question_id} className="pcard" style={{ borderColor: meta.color }}>
                    <div className="pq">{r.question_text}</div>
                    <div className="pa">{r.answer}</div>
                    <div className="pm" style={{ color: meta.color }}>
                      {meta.label}
                      {r.correction_count ? ` · corrected ${r.correction_count}×` : ""}
                    </div>
                  </div>
                );
              })
          : (
            <p className="empty">
              Nothing recorded yet. Answers verified from documents, and any conflict
              you resolve, are saved here and reused on the next question.
            </p>
          )}
      </aside>
      </main>

      <form className="composer" onSubmit={(e) => { e.preventDefault(); void send(); }}>
        {answering && (
          <div className="answering">
            <span>answering</span>
            {answering.followUp}
            <button type="button" onClick={() => setAnswering(null)}>✕</button>
          </div>
        )}
        <input
          ref={inputRef}
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder={answering ? "Type your answer or confirm the recommendation…" : "Ask a security question, policy inquiry, or compliance control…"}
          disabled={busy}
        />
        <button className="primary" disabled={busy || !draft.trim()} type="submit">
          {answering ? "Record & Save" : "Send"}
        </button>
      </form>

      {drawer && (
        <div className="overlay" onClick={() => setDrawer(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="mhead">
              <code>{drawer.id}</code>
              <button onClick={() => setDrawer(null)}>✕</button>
            </div>
            <pre className="src">{drawer.text}</pre>
          </div>
        </div>
      )}
    </div>
  );
}
