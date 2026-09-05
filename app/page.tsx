"use client";
import Link from "next/link";
import { css } from "./theme";

export default function Landing() {
  return (
    <div className="land">
      <style>{css}</style>

      <nav>
        <div className="brand">SENTINEL <span>ANALYST</span></div>
        <Link href="/analyst" className="navcta">Open console →</Link>
      </nav>

      <section className="hero">
        <div className="eyebrow">Enterprise security questionnaires</div>
        <h1>Your security answers already exist.<br /><em>They&apos;re just scattered.</em></h1>
        <p>Sentinel searches every policy, infrastructure record, document and internal
          message before it answers a single question, cites the exact lines it used,
          flags contradictions between sources, and tells you plainly when it doesn&apos;t know.</p>
        <div className="ctas">
          <Link href="/analyst" className="primary">Start investigating <i aria-hidden>→</i></Link>
          <a href="#how" className="ghost">How it works <i aria-hidden>↓</i></a>
        </div>
        <div className="promise">
          <b>Never fabricates.</b> If the evidence isn&apos;t there, it says so “unknown” is a valid answer.
        </div>
      </section>

      <section className="sources">
        <span>Reads across</span>
        {["Policies", "Infrastructure", "Documents", "Internal messages", "Employee records"]
          .map((s) => <div key={s} className="pill">{s}</div>)}
      </section>

      <section className="proof">
        <div className="proofhead">Every answer arrives with its receipts</div>
        <div className="cards">
          <article style={{ ["--rail" as any]: "#10b981" }}>
            <div className="b" style={{ color: "#10b981", borderColor: "#10b98155" }}>
              Verified from company records <em>· high confidence</em>
            </div>
            <p>MFA is mandatory for Google Workspace and GitHub, enforced via SSO for all
              employees and contractors.</p>
            <div className="chips">
              <span className="chip"><em>policy</em>security-policy.md</span>
              <span className="chip"><em>infra</em>okta-config.json</span>
            </div>
          </article>

          <article style={{ ["--rail" as any]: "#f59e0b" }}>
            <div className="b" style={{ color: "#f59e0b", borderColor: "#f59e0b55" }}>
              Sources disagree
            </div>
            <p>Policy states MFA is mandatory, but a message from #it-help in February
              suggests one contractor account was exempted. Which is current?</p>
            <div className="chips">
              <span className="chip"><em>policy</em>security-policy.md</span>
              <span className="chip"><em>message</em>it-help.txt</span>
            </div>
          </article>

          <article style={{ ["--rail" as any]: "#64748b" }}>
            <div className="b" style={{ color: "#64748b", borderColor: "#64748b55" }}>
              Not found: needs confirmation
            </div>
            <p>No record of employee background checks in any available source.
              I won&apos;t guess, can you confirm the process?</p>
            <div className="chips"><span className="none">no evidence found</span></div>
          </article>
        </div>
      </section>

      <section className="how" id="how">
        <h2>Three steps, one honest answer</h2>
        <div className="steps">
          {[
            ["01", "Search all evidence first",
             "Before asking you anything, Sentinel queries the security graph across every source it has policies, infra, docs, messages, people."],
            ["02", "Verified, conflicted, or unknown",
             "Evidence found and consistent? Verified, with citations. Sources disagree? It flags the conflict and asks you to resolve it. Nothing found? It asks, it never invents."],
            ["03", "Completed questionnaire",
             "Findings accumulate into a persistent security profile you can export, with evidence, confidence and source on every single line."],
          ].map(([n, t, d]) => (
            <div key={n} className="step">
              <div className="num">{n}</div>
              <h3>{t}</h3>
              <p>{d}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="close">
        <h2>Ask it anything about your security posture.</h2>
        <Link href="/analyst" className="primary big">Open the console →</Link>
      </section>
    </div>
  );
}
