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
  citations?: Citation[];
  graphTrace?: Trace;
  pending?: boolean;
  followUp?: string | null;
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
        citations?: Citation[];
        graphTrace?: Trace;
        followUp?: string | null;
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
              citations: data.citations ?? [],
              graphTrace: data.graphTrace ?? m.graphTrace,
              pending: false,
              followUp: data.followUp ?? null,
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
          <div className="starters" style={{ padding: "44px 0 20px", alignItems: "flex-start", width: "100%" }}>
            <div className="eyebrow">Interactive Security Analyst</div>
            <h2 style={{ margin: "0 0 8px", fontSize: "28px" }}>What do you want to investigate?</h2>
            <p className="empty" style={{ marginBottom: "20px" }}>
              Sentinel traverses the verified evidence graph, cites verbatim sources, flags contradictions, and escalates to human stakeholders when information is unavailable.
            </p>
            <div style={{ display: "flex", flexDirection: "column", gap: "10px", width: "100%", maxWidth: "720px" }}>
              <button
                type="button"
                className="starter"
                onClick={() => void send("Does your organization have a formal Information Security Program established?")}
              >
                <b style={{ color: "var(--ok)", marginRight: "8px" }}>✓ Verified (Q1.0):</b>
                Does your organization have a formal Information Security Program established?
              </button>
              <button
                type="button"
                className="starter"
                onClick={() => void send("Where is company and customer data hosted?")}
              >
                <b style={{ color: "var(--warn)", marginRight: "8px" }}>⚠ Conflict (Q22.0):</b>
                Where is company and customer data hosted? (Cloud vs On-Prem contradiction)
              </button>
              <button
                type="button"
                className="starter"
                onClick={() => void send("Will you be using third party contractors or sub-contractors to complete the engagement?")}
              >
                <b style={{ color: "var(--acc2)", marginRight: "8px" }}>? Needs Input (Q6.0):</b>
                Will you be using third party contractors or sub-contractors to complete the engagement?
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
                  {m.status && (
                    <span className="badge" style={{ color: STATUS_META[m.status].color, borderColor: STATUS_META[m.status].color + "55" }}>
                      {STATUS_META[m.status].label}
                    </span>
                  )}
                  <p className="ans">{m.text}</p>
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
                  {m.followUp && (
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
                  )}
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
          placeholder={answering ? "Type the current practice / stakeholder resolution…" : "Ask the security agent (e.g. Q1.0, Q22.0, Q6.0)…"}
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
