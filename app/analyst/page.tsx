"use client";
import { useEffect, useRef, useState } from "react";
import GraphTrace, { type Trace } from "../components/GraphTrace";
import { css } from "../theme";

type Status = "answered" | "conflict" | "ask_user" | "insufficient";
type Citation = { id: string; source: string; quote?: string; sourceType?: string };
type Message = {
  id: string;
  role: "user" | "assistant";
  text: string;
  status?: Status;
  citations?: Citation[];
  graphTrace?: Trace;
  pending?: boolean;
};

const STATUS_META: Record<string, { label: string; color: string }> = {
  answered: { label: "From documents", color: "#10b981" },
  conflict: { label: "Conflict", color: "#f59e0b" },
  ask_user: { label: "Needs input", color: "#64748b" },
  insufficient: { label: "Needs input", color: "#64748b" },
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
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    void fetch("/api/corpus")
      .then((r) => r.json())
      .then(setCorpus)
      .catch(() => setCorpus({ ready: false, documentCount: 0, chunkCount: 0 }));
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function send(text?: string) {
    const message = (text ?? draft).trim();
    if (!message || busy) return;
    setDraft("");
    const history = messages
      .filter((m) => !m.pending)
      .map((m) => ({ role: m.role, text: m.text }));
    const pendingId = `a-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      { id: `u-${Date.now()}`, role: "user", text: message },
      { id: pendingId, role: "assistant", text: "querying the security graph…", pending: true },
    ]);
    setBusy(true);
    try {
      const headers = { "Content-Type": "application/json" };
      const chatP = fetch("/api/chat", {
        method: "POST",
        headers,
        body: JSON.stringify({ message, history }),
      });
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

      const r = await chatP;
      if (!r.ok) throw new Error(`chat ${r.status}`);
      const data = await r.json() as {
        reply: string;
        status?: Status;
        citations?: Citation[];
        graphTrace?: Trace;
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
            }
          : m
      )));
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
          <a href="/" style={{ fontSize: 12, color: "#8a8074", textDecoration: "none" }}>← Back</a>
          <div className="brand">SENTINEL <span>ANALYST</span></div>
          <div className="sub">
            Ask anything about this company&apos;s security posture
            {corpus?.ready
              ? ` · ${corpus.documentCount} docs · ${corpus.graphNodes ?? 0} graph nodes`
              : " · waiting for the security agent"}
          </div>
        </div>
      </header>

      <div className="thread">
        {messages.length === 0 && (
          <div className="starters" style={{ padding: "56px 0", alignItems: "center", width: "100%" }}>
            <div className="eyebrow">Console</div>
            <h2 style={{ margin: "0 0 8px" }}>What do you want to know?</h2>
            <p className="empty">Sentinel queries the document graph first, then answers from cited evidence.</p>
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

      <form className="composer" onSubmit={(e) => { e.preventDefault(); void send(); }}>
        <input
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="Ask the security agent…"
          disabled={busy}
        />
        <button className="primary" disabled={busy || !draft.trim()} type="submit">
          Send
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
