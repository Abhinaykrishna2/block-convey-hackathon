export const css = `
/* ── tokens ─────────────────────────────────────────────── */
:root{
  --bg:#f4efe6;
  --s1:#fbf7f0;      /* base surface */
  --s2:#fffdf9;      /* raised */
  --s3:#f3ebe0;      /* hover */
  --line:#e4d8c8;
  --edge:rgba(255,255,255,.92);
  --tx:#2c261e; --tx2:#6b6256; --tx3:#8a8074;
  --acc:#9a5b32; --acc2:#b56f3e; --acc3:#c9a15b;
  --ok:#4f8a5b; --warn:#c4842a; --dim:#8a8074;
  --pol:#4f8a5b; --inf:#7c6a9a; --doc:#3d7a8c; --msg:#c4842a; --emp:#b06a8a;
}
*{box-sizing:border-box}
::selection{background:rgba(181,111,62,.22)}
::-webkit-scrollbar{width:9px;height:9px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#d8ccbc;border-radius:99px;
  border:2px solid transparent;background-clip:content-box}
::-webkit-scrollbar-thumb:hover{background:#c4b6a4;background-clip:content-box}

/* ── canvas: warm paper + soft wash ─────────────────────── */
body{
  margin:0;color:var(--tx);
  font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;
  -webkit-font-smoothing:antialiased;
  background:
    radial-gradient(900px 520px at 12% -8%, rgba(201,161,91,.18), transparent 62%),
    radial-gradient(760px 460px at 92% 2%,  rgba(181,111,62,.08), transparent 60%),
    radial-gradient(680px 520px at 50% 108%,rgba(154,91,50,.06), transparent 62%),
    var(--bg);
  background-attachment:fixed;
  position:relative;
}
body::before{
  content:"";position:fixed;inset:0;pointer-events:none;
  background-image:
    linear-gradient(rgba(44,38,30,.035) 1px,transparent 1px),
    linear-gradient(90deg,rgba(44,38,30,.035) 1px,transparent 1px);
  background-size:52px 52px;
  mask-image:radial-gradient(1100px 700px at 50% 0%,#000 20%,transparent 78%);
  z-index:0;
}
.land,.app{position:relative;z-index:1}
a{text-decoration:none;color:inherit}

/* ── surfaces: elevation + top light edge ───────────────── */
.card,.cards article,.ansbox,aside,.modal,.promise,.pill,.gt,.trace{
  background:linear-gradient(168deg,var(--s2),var(--s1));
  border:1px solid var(--line);
  border-top-color:var(--edge);
  box-shadow:
    0 1px 0 rgba(255,255,255,.85) inset,
    0 14px 34px -18px rgba(80,60,35,.18),
    0 2px 8px -4px rgba(80,60,35,.08);
}

/* ── nav / header ───────────────────────────────────────── */
nav,header{display:flex;justify-content:space-between;align-items:flex-start;
  gap:22px;flex-wrap:wrap;padding:22px 0 18px;
  border-bottom:1px solid var(--line);position:relative}
nav{align-items:center}
nav::after,header::after{content:"";position:absolute;left:0;right:0;bottom:-1px;
  height:1px;background:linear-gradient(90deg,transparent,rgba(154,91,50,.35),transparent)}
.brand{font-size:22px;font-weight:700;letter-spacing:.15em;
  background:linear-gradient(180deg,#2c261e,#6b6256);
  -webkit-background-clip:text;background-clip:text;color:transparent}
.brand span{color:var(--acc2);-webkit-text-fill-color:var(--acc2);font-weight:400}
.sub{color:var(--tx3);font-size:14px;margin-top:6px;letter-spacing:.01em}
.right{display:flex;align-items:center;gap:16px}
.counts{display:flex;gap:16px;font-size:13px;font-variant-numeric:tabular-nums;
  letter-spacing:.02em}

/* ── buttons: paper + lift ──────────────────────────────── */
button,.navcta,.ghost,.primary{
  display:inline-flex;align-items:center;justify-content:center;gap:8px;
  background:linear-gradient(170deg,var(--s2),var(--s3));
  color:var(--tx);border:1px solid var(--line);border-top-color:var(--edge);
  padding:10px 18px;border-radius:11px;font-size:14.5px;font-weight:500;cursor:pointer;
  line-height:1.2;letter-spacing:-.01em;
  transition:transform .14s ease,box-shadow .18s ease,border-color .18s ease,background .18s ease;
  box-shadow:0 1px 0 rgba(255,255,255,.8) inset,0 6px 16px -10px rgba(80,60,35,.2)}
button:hover:not(:disabled),.navcta:hover,.ghost:hover{
  border-color:#cbb9a4;transform:translateY(-1px);
  box-shadow:0 1px 0 rgba(255,255,255,.9) inset,0 12px 26px -12px rgba(80,60,35,.22)}
button:active:not(:disabled),.primary:active,.ghost:active{transform:translateY(0)}
button:disabled{opacity:.38;cursor:not-allowed;transform:none}
.primary{background:linear-gradient(175deg,#c98a52,#9a5b32);
  border-color:#b56f3e;border-top-color:rgba(255,255,255,.5);color:#fff;font-weight:600;
  box-shadow:0 1px 0 rgba(255,255,255,.35) inset,0 12px 28px -12px rgba(154,91,50,.5),
             0 0 0 1px rgba(154,91,50,.1)}
.primary:hover:not(:disabled){background:linear-gradient(175deg,#d4965c,#a8663a);
  border-color:#c4844a;transform:translateY(-1px);
  box-shadow:0 1px 0 rgba(255,255,255,.42) inset,0 16px 34px -12px rgba(154,91,50,.52),
             0 0 22px -4px rgba(201,161,91,.35)}
.primary.big{padding:16px 32px;font-size:16.5px;border-radius:12px}
.primary i,.ghost i{font-style:normal;opacity:.82;font-weight:500}

/* ── landing hero ───────────────────────────────────────── */
.land,.app{max-width:1200px;margin:0 auto;padding:0 26px 96px}
.app{padding-bottom:112px}
.hero{padding:92px 0 60px;max-width:780px;position:relative}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:12px;
  letter-spacing:.18em;text-transform:uppercase;color:var(--acc2);margin-bottom:24px;
  padding:6px 13px;border-radius:99px;border:1px solid rgba(154,91,50,.22);
  background:rgba(201,161,91,.12);box-shadow:0 0 20px -8px rgba(201,161,91,.45)}
.hero h1{font-size:clamp(36px,5.4vw,62px);line-height:1.04;letter-spacing:-.032em;
  margin:0 0 24px;font-weight:700;
  background:linear-gradient(175deg,#2c261e 20%,#6b6256 92%);
  -webkit-background-clip:text;background-clip:text;color:transparent}
.hero h1 em{font-style:normal;
  background:linear-gradient(100deg,var(--acc3),var(--acc2) 55%,#9a5b32);
  -webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{font-size:18px;line-height:1.72;color:var(--tx2);margin:0 0 34px;max-width:650px}
.ctas{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.ctas .primary,.ctas .ghost{padding:14px 24px;font-size:16px;border-radius:12px;min-height:46px}
.ctas .ghost{color:var(--tx);background:linear-gradient(170deg,#fffdf9,#f6efe4);
  border-color:#d8cbb8}
.promise{margin-top:38px;padding:16px 22px;border-radius:10px;font-size:15px;
  color:var(--tx2);max-width:580px;line-height:1.6;border-left:2px solid var(--ok);
  box-shadow:0 1px 0 rgba(255,255,255,.85) inset,-14px 0 30px -22px rgba(79,138,91,.35),
             0 14px 34px -18px rgba(80,60,35,.12)}
.promise b{color:var(--ok);font-weight:600}

/* ── source pills ───────────────────────────────────────── */
.sources{display:flex;align-items:center;gap:9px;flex-wrap:wrap;padding:28px 0 70px;
  border-top:1px solid var(--line)}
.sources span{font-size:12px;text-transform:uppercase;letter-spacing:.14em;
  color:var(--tx3);margin-right:6px}
.pill{font-size:13.5px;padding:7px 14px;border-radius:99px;color:var(--tx2)}

/* ── status badge with glow ─────────────────────────────── */
.badge,.b{font-size:12px;text-transform:uppercase;letter-spacing:.09em;
  border:1px solid;border-radius:99px;padding:4px 11px;display:inline-flex;
  align-items:center;gap:7px;font-weight:600;
  box-shadow:0 0 18px -6px currentColor}
.badge em,.b em{font-style:normal;opacity:.68;text-transform:none;letter-spacing:0;
  font-weight:400}

/* ── answer / proof cards: glowing accent rail ─────────── */
.proofhead{font-size:12px;text-transform:uppercase;letter-spacing:.14em;
  color:var(--tx3);margin-bottom:20px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:15px}
.cards article,.ansbox{position:relative;border-radius:12px;padding:17px 19px;
  overflow:hidden;transition:transform .2s ease,box-shadow .2s ease}
.cards article::before,.ansbox::before{content:"";position:absolute;left:0;top:0;bottom:0;
  width:3px;background:var(--rail,currentColor);opacity:.95;
  box-shadow:0 0 16px 1px var(--rail,currentColor)}
.cards article:hover,.ansbox:hover{transform:translateY(-2px);
  box-shadow:0 1px 0 rgba(255,255,255,.9) inset,0 22px 48px -22px rgba(80,60,35,.22)}
.cards p,.ans{font-size:15.5px;line-height:1.72;color:#3d362c;margin:14px 0 0}
.ans{font-size:16px;white-space:pre-wrap}

/* ── evidence chips ─────────────────────────────────────── */
.chips{display:flex;gap:7px;flex-wrap:wrap;margin-top:15px}
.chip{font-family:ui-monospace,SFMono-Regular,monospace;font-size:12px;padding:5px 10px;
  border-radius:7px;display:inline-flex;gap:6px;align-items:center;
  background:linear-gradient(170deg,#fffdf9,#f3ebe0);border:1px solid #e4d8c8;
  border-top-color:var(--edge);color:var(--tx2);cursor:pointer;transition:.15s;
  box-shadow:0 1px 0 rgba(255,255,255,.8) inset}
.chip:hover{border-color:#cbb9a4;color:var(--tx);
  box-shadow:0 0 16px -6px rgba(201,161,91,.5),0 1px 0 rgba(255,255,255,.9) inset}
.chip em{font-style:normal;text-transform:uppercase;font-size:10.5px;letter-spacing:.07em;
  font-weight:600}
.chip em:only-child{color:var(--acc2)}
.none{font-size:12px;color:var(--tx3);font-family:ui-monospace,monospace;font-style:italic}
.conf{font-size:12.5px;color:var(--tx3);margin-left:auto;font-variant-numeric:tabular-nums}

/* ── how it works ───────────────────────────────────────── */
.how{padding:92px 0 0}
.how h2,.close h2{font-size:clamp(25px,3.5vw,36px);letter-spacing:-.025em;margin:0 0 36px;
  background:linear-gradient(175deg,#2c261e,#6b6256);-webkit-background-clip:text;
  background-clip:text;color:transparent}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(258px,1fr));gap:28px}
.step .num{font-family:ui-monospace,monospace;font-size:13px;letter-spacing:.14em;
  margin-bottom:14px;color:var(--acc2);display:inline-block;padding:4px 9px;
  border-radius:6px;background:rgba(201,161,91,.14);border:1px solid rgba(154,91,50,.18)}
.step h3{font-size:18px;margin:0 0 10px;letter-spacing:-.012em}
.step p{font-size:15px;line-height:1.72;color:var(--tx2);margin:0}
.close{text-align:center;padding:104px 0 30px;border-top:1px solid var(--line);margin-top:92px}

/* ── console layout ─────────────────────────────────────── */
main{display:grid;grid-template-columns:1fr 330px;gap:26px;align-items:start;margin-top:24px}
@media(max-width:980px){main{grid-template-columns:1fr}aside{display:none}}
.thread{padding:28px 0 8px}
.starters{display:flex;flex-direction:column;gap:9px;align-items:flex-start}
.starter{font-size:14.5px;padding:11px 16px;text-align:left;color:var(--tx2);
  border-radius:10px}
.starter:hover{color:var(--tx);border-color:rgba(154,91,50,.35);
  box-shadow:0 0 24px -10px rgba(201,161,91,.5),0 1px 0 rgba(255,255,255,.8) inset}
.turn{margin-bottom:28px}
.you{font-size:19px;font-weight:650;margin-bottom:13px;letter-spacing:-.015em;
  padding-left:13px;border-left:2px solid rgba(154,91,50,.45)}
.thinking{display:flex;align-items:center;gap:5px;color:var(--acc2);font-size:14px;
  padding:8px 0 8px 13px}
.thinking i{width:5px;height:5px;background:currentColor;border-radius:50%;
  box-shadow:0 0 8px currentColor;animation:bob 1.2s ease-in-out infinite}
.thinking i:nth-child(2){animation-delay:.15s}
.thinking i:nth-child(3){animation-delay:.3s}
.thinking span{margin-left:9px;color:var(--tx3)}
@keyframes bob{0%,60%,100%{opacity:.2}30%{opacity:1}}
.follow{margin-top:14px;font-size:15px;line-height:1.55;color:var(--acc);text-align:left;
  display:flex;align-items:flex-start;gap:9px;width:100%;
  background:rgba(201,161,91,.1);border:1px dashed rgba(154,91,50,.32);padding:11px 15px;
  border-radius:10px;box-shadow:none}
.follow::before{content:"↳";flex:none;opacity:.65;font-size:12px;line-height:1.6}
.follow:hover{background:rgba(201,161,91,.18);border-style:solid;color:var(--tx);
  box-shadow:0 0 22px -8px rgba(201,161,91,.45)}
.reveal{margin-top:13px;font-size:13px;color:var(--tx3);background:none;border:none;
  padding:4px 0;box-shadow:none}
.reveal:hover{color:var(--acc2);background:none;transform:none;box-shadow:none}

/* ── right rail ─────────────────────────────────────────── */
aside{border-radius:12px;padding:17px;position:sticky;top:22px;
  max-height:calc(100vh - 170px);overflow:auto}
aside h3{margin:0 0 15px;font-size:13px;text-transform:uppercase;letter-spacing:.13em;
  color:var(--tx3);display:flex;justify-content:space-between;align-items:center}
aside h3 span{background:linear-gradient(170deg,#c4844a,#9a5b32);color:#fff;
  border-radius:99px;padding:2px 9px;font-size:10.5px;
  box-shadow:0 0 16px -5px rgba(154,91,50,.45)}
.empty{font-size:14px;color:var(--tx3);line-height:1.65;margin:0}
.pcard{border-left:2px solid;padding:10px 0 10px 12px;margin-bottom:14px;
  box-shadow:-12px 0 26px -22px currentColor}
.pq{font-size:14.5px;font-weight:600;margin-bottom:4px;color:var(--tx)}
.pa{font-size:13.5px;color:var(--tx2);line-height:1.55;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.pm{font-size:11.5px;color:var(--tx3);margin-top:6px;font-family:ui-monospace,monospace;
  letter-spacing:.03em}

/* ── composer ───────────────────────────────────────────── */
.composer{position:fixed;bottom:0;left:0;right:0;padding:18px 26px;z-index:20;
  display:flex;justify-content:center;gap:11px;flex-wrap:wrap;
  background:linear-gradient(180deg,transparent,rgba(244,239,230,.94) 42%);
  backdrop-filter:blur(14px);border-top:1px solid var(--line)}
.composer input{flex:1;max-width:840px;padding:15px 19px;border-radius:11px;font-size:16px;
  color:var(--tx);background:linear-gradient(170deg,#fffdf9,#f6f0e6);
  border:1px solid #e4d8c8;border-top-color:var(--edge);
  box-shadow:0 2px 10px rgba(80,60,35,.06) inset;transition:.18s}
.composer input::placeholder{color:var(--tx3)}
.answering{flex:0 0 100%;max-width:948px;margin:0 auto;display:flex;align-items:center;
  gap:10px;font-size:14px;line-height:1.5;color:var(--tx2);padding:8px 13px;border-radius:9px;
  background:rgba(201,161,91,.14);border:1px solid rgba(154,91,50,.24)}
.answering span{flex:none;font-size:9px;text-transform:uppercase;letter-spacing:.12em;
  font-weight:700;color:var(--acc)}
.answering button{margin-left:auto;flex:none;padding:2px 8px;font-size:11px;border-radius:6px;
  background:none;border:none;box-shadow:none;color:var(--tx3)}
.answering button:hover{color:var(--acc);background:rgba(255,255,255,.6);transform:none;
  box-shadow:none}
.composer input:focus{outline:none;border-color:var(--acc);
  box-shadow:0 2px 10px rgba(80,60,35,.06) inset,0 0 0 3px rgba(154,91,50,.12),
             0 0 30px -8px rgba(201,161,91,.4)}

/* ── modals ─────────────────────────────────────────────── */
.overlay{position:fixed;inset:0;background:rgba(44,38,30,.28);backdrop-filter:blur(6px);
  display:flex;align-items:center;justify-content:center;padding:26px;z-index:60;
  animation:fadein .16s ease}
@keyframes fadein{from{opacity:0}}
.modal{border-radius:14px;max-width:680px;width:100%;max-height:80vh;overflow:auto;
  animation:rise .22s cubic-bezier(.2,.9,.3,1);
  box-shadow:0 1px 0 rgba(255,255,255,.9) inset,0 40px 90px -30px rgba(80,60,35,.28)}
.modal.wide{max-width:880px}
@keyframes rise{from{opacity:0;transform:translateY(14px) scale(.985)}}
.mhead{display:flex;justify-content:space-between;align-items:center;padding:16px 19px;
  border-bottom:1px solid var(--line);position:sticky;top:0;z-index:2;
  background:linear-gradient(180deg,#fffdf9,#fbf7f0)}
.mhead code{font-size:13.5px;color:var(--acc2);font-family:ui-monospace,monospace}
.src{margin:0;padding:19px;font-size:14px;line-height:1.8;white-space:pre-wrap;
  color:#3d362c;font-family:ui-monospace,SFMono-Regular,monospace}
.rsec{padding:17px 19px;border-bottom:1px solid var(--line)}
.rsec h4{margin:0 0 13px;font-size:11px;text-transform:uppercase;letter-spacing:.1em}
.rrow{margin-bottom:14px}
.rrow b{display:block;font-size:13.5px;margin-bottom:4px}
.rrow span{display:block;font-size:13px;color:var(--tx2);line-height:1.62}
.rrow small{display:block;font-size:10px;color:var(--tx3);
  font-family:ui-monospace,monospace;margin-top:5px}

/* ── graph trace ────────────────────────────────────────── */
.gt{margin-top:11px;border-radius:10px;overflow:hidden}
.glog{padding:14px 16px;font-family:ui-monospace,SFMono-Regular,monospace;
  font-size:13px;line-height:1.9;max-height:220px;overflow:auto}
.gline{color:#7a7166;animation:gin .18s ease both}
.gline.sub{color:var(--tx3);padding-left:15px}
.gline.warn{color:var(--warn);text-shadow:0 0 14px rgba(196,132,42,.25)}
.gline.verdict{color:var(--acc2);font-weight:600;text-shadow:0 0 16px rgba(201,161,91,.35)}
.gt-caret{color:var(--acc);margin-right:8px}
.cursor{color:var(--acc2);animation:blink .9s step-end infinite}
@keyframes gin{from{opacity:0;transform:translateX(-5px)}}
@keyframes blink{50%{opacity:0}}
/* ── graph canvas (react flow) ──────────────────────────── */
.gcanvas{position:relative;border-bottom:1px solid var(--line);
  background:radial-gradient(620px 320px at 50% 35%,rgba(201,161,91,.13),transparent 72%),#fbf7f0}
.gcanvas .react-flow__renderer{cursor:grab}
.gcanvas .react-flow__pane.dragging{cursor:grabbing}
.gcanvas .react-flow__edge-path{stroke-linecap:round}
.gcanvas .react-flow__edge.animated .react-flow__edge-path{
  stroke-dasharray:5 5;animation:dash 1.1s linear infinite}
@keyframes dash{to{stroke-dashoffset:-20}}

.tnode{display:flex;align-items:center;gap:10px;padding:0 13px;border-radius:10px;
  background:linear-gradient(170deg,#fffdf9,#f6efe4);
  border:1px solid var(--line);border-left:2.5px solid var(--c);
  box-shadow:0 1px 0 rgba(255,255,255,.85) inset,0 8px 20px -14px rgba(80,60,35,.35);
  transition:box-shadow .18s ease,transform .18s ease}
.tnode:hover{transform:translateY(-1px);
  box-shadow:0 1px 0 rgba(255,255,255,.9) inset,0 14px 28px -14px rgba(80,60,35,.35),
             0 0 0 1px color-mix(in srgb,var(--c) 30%,transparent)}
.tdot{flex:none;width:8px;height:8px;border-radius:50%;background:var(--c);
  box-shadow:0 0 0 3px color-mix(in srgb,var(--c) 16%,transparent)}
.tbody{min-width:0;display:flex;flex-direction:column;gap:2px}
.tkind{display:flex;align-items:center;gap:6px;font-size:10.5px;text-transform:uppercase;
  letter-spacing:.12em;color:var(--c);font-weight:700;font-family:ui-monospace,monospace}
.tkind em{font-style:normal;text-transform:none;letter-spacing:.02em;font-weight:500;
  color:var(--tx3);padding:1px 5px;border-radius:4px;background:rgba(44,38,30,.05)}
.tlabel{font-size:12.5px;color:var(--tx);font-family:ui-monospace,SFMono-Regular,monospace;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.thandle{width:5px;height:5px;background:var(--c);border:none;opacity:.45}

.gcanvas .react-flow__controls{box-shadow:none;gap:3px;display:flex;flex-direction:column;
  margin:10px}
.gcanvas .react-flow__controls-button{width:22px;height:22px;border:1px solid var(--line);
  border-radius:6px;background:linear-gradient(170deg,#fffdf9,#f6efe4);color:var(--tx2);
  box-shadow:0 1px 0 rgba(255,255,255,.8) inset;transition:.15s}
.gcanvas .react-flow__controls-button:hover{border-color:#cbb9a4;color:var(--acc)}
.gcanvas .react-flow__controls-button svg{fill:currentColor;max-width:10px;max-height:10px}

.glegend{position:absolute;left:12px;bottom:10px;display:flex;gap:12px;flex-wrap:wrap;
  align-items:center;font-size:11px;font-family:ui-monospace,monospace;
  letter-spacing:.06em;color:var(--tx3);pointer-events:none}
.glegend span{display:inline-flex;align-items:center;gap:5px;text-transform:uppercase}
.glegend i{width:6px;height:6px;border-radius:50%;background:var(--c)}
.glegend b{color:var(--acc2);font-weight:600;margin-left:auto}
`;
