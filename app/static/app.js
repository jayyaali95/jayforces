// pitstop front end. No framework on purpose: one state object, a few render functions.

const VS = "https://cdn.jsdelivr.net/npm/monaco-editor@0.52.2/min/vs";
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const pct = (n) => (Math.round(n * 10) / 10).toString();
const COLOR = { easy: "var(--green)", medium: "var(--yellow)", hard: "var(--red)" };
const LOCK = `<svg width="10" height="12" viewBox="0 0 10 12" aria-hidden="true"><rect x="1" y="5" width="8" height="7" rx="1.5" fill="currentColor"/><path d="M3 5V3.6a2 2 0 0 1 4 0V5" stroke="currentColor" fill="none" stroke-width="1.4"/></svg>`;

const S = {
  state: null,     // /api/state payload
  contest: null,   // active contest view
  idx: 0,          // open question index
  q: null,         // open question detail
  editor: null,
  results: {},     // last run per question index, kept while the page is open
  skew: 0,         // server clock minus browser clock, seconds
  saveTimer: null,
  loading: false,  // true while we programmatically set editor text
  busy: false,
};

async function api(method, path, body) {
  const res = await fetch(path, {
    method,
    headers: body ? { "Content-Type": "application/json" } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Request failed with status ${res.status}.`);
  return data;
}

// ---------- editor ----------

function loadEditor() {
  window.MonacoEnvironment = {
    getWorkerUrl: () => `data:text/javascript;charset=utf-8,${encodeURIComponent(
      `self.MonacoEnvironment={baseUrl:'${VS}/../'};importScripts('${VS}/base/worker/workerMain.js');`)}`,
  };
  return new Promise((resolve) => {
    if (!window.require) return resolve(plainEditor());
    require.config({ paths: { vs: VS } });
    require(["vs/editor/editor.main"], () => resolve(monacoEditor()), () => resolve(plainEditor()));
  });
}

function monacoEditor() {
  monaco.editor.defineTheme("tokyo-night", {
    base: "vs-dark",
    inherit: true,
    rules: [
      { token: "comment", foreground: "565f89", fontStyle: "italic" },
      { token: "keyword", foreground: "bb9af7" },
      { token: "string", foreground: "9ece6a" },
      { token: "number", foreground: "ff9e64" },
      { token: "delimiter", foreground: "89ddff" },
      { token: "identifier", foreground: "c0caf5" },
      { token: "type", foreground: "2ac3de" },
      { token: "tag", foreground: "7dcfff" },
    ],
    colors: {
      "editor.background": "#1a1b26",
      "editor.foreground": "#a9b1d6",
      "editorLineNumber.foreground": "#3b4261",
      "editorLineNumber.activeForeground": "#737aa2",
      "editor.selectionBackground": "#283457",
      "editor.lineHighlightBackground": "#1e2030",
      "editorCursor.foreground": "#c0caf5",
      "editorIndentGuide.background1": "#292e42",
      "editorWidget.background": "#16161e",
      "editorGutter.background": "#1a1b26",
    },
  });
  const ed = monaco.editor.create($("#editor"), {
    language: "python",
    theme: "tokyo-night",
    fontFamily: "'JetBrains Mono', ui-monospace, monospace",
    fontSize: 14,
    lineHeight: 22,
    tabSize: 4,
    insertSpaces: true,
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    automaticLayout: true,
    renderLineHighlight: "line",
    smoothScrolling: true,
    padding: { top: 4 },
  });
  ed.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, run);
  ed.onDidChangeModelContent(scheduleSave);
  document.fonts?.ready.then(() => monaco.editor.remeasureFonts());
  return ed;
}

// If the CDN is unreachable you still get a usable (if plain) editor.
function plainEditor() {
  const ta = document.createElement("textarea");
  ta.spellcheck = false;
  ta.style.cssText = "width:100%;height:100%;background:#1a1b26;color:#c0caf5;border:0;padding:12px 16px;font:14px/22px var(--mono);resize:none;outline:none;tab-size:4";
  ta.addEventListener("input", scheduleSave);
  ta.addEventListener("keydown", (e) => {
    if (e.key === "Tab") {
      e.preventDefault();
      ta.setRangeText("    ", ta.selectionStart, ta.selectionEnd, "end");
    }
  });
  $("#editor").append(ta);
  return {
    getValue: () => ta.value,
    setValue: (v) => { ta.value = v; },
    updateOptions: ({ readOnly }) => { ta.readOnly = !!readOnly; },
    focus: () => ta.focus(),
  };
}

function setCode(code) {
  S.loading = true;
  S.editor.setValue(code);
  S.loading = false;
}

function scheduleSave() {
  if (S.loading || !S.q || !S.contest?.active) return;
  clearTimeout(S.saveTimer);
  S.saveTimer = setTimeout(save, 700);
}

async function save() {
  S.saveTimer = null;
  if (!S.q || !S.contest?.active) return;
  await api("PUT", `/api/contests/${S.contest.id}/q/${S.idx}/code`, { code: S.editor.getValue() }).catch(() => {});
}

async function flushSave() {
  if (S.saveTimer) {
    clearTimeout(S.saveTimer);
    await save();
  }
}

window.addEventListener("beforeunload", () => {
  if (!S.saveTimer || !S.q) return;
  fetch(`/api/contests/${S.contest.id}/q/${S.idx}/code`, {
    method: "PUT", keepalive: true, headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: S.editor.getValue() }),
  });
});

// ---------- top bar ----------

function renderLaps() {
  const qs = S.contest?.active ? S.contest.questions : [];
  $("#laps").innerHTML = qs.map((q, i) => `
    <button class="lap ${q.solved ? "done" : ""}" data-i="${i}" ${q.open ? "" : "disabled"}
      aria-current="${i === S.idx && !!S.q}" aria-label="Question ${i + 1}, ${q.difficulty}${q.open ? `, ${pct(q.best)} percent` : ", locked"}"
      title="${esc(q.open ? q.title : "Solve the previous question to unlock")}">
      <span class="dot" style="background:${COLOR[q.difficulty]}"></span>
      <span class="label">Q${i + 1}</span>
      <span class="pct">${q.open ? `${pct(q.best)}%` : LOCK}</span>
    </button>`).join("");
  const active = !!S.contest?.active;
  $("#new-btn").hidden = !S.contest; // the home screen has its own big button
  $("#end-btn").hidden = !active;
  $("#clock").hidden = !active;
}

$("#laps").addEventListener("click", (e) => {
  const b = e.target.closest(".lap");
  if (b && !b.disabled) openQuestion(+b.dataset.i);
});

function tick() {
  const c = S.contest, bar = $("#fuel"), clock = $("#clock");
  if (!c?.active) {
    bar.style.width = "0";
    return;
  }
  const now = Date.now() / 1000 + S.skew;
  const left = Math.max(0, c.ends_at - now);
  const share = left / (c.ends_at - c.started_at);
  const low = left < 15 * 60, out = left < 5 * 60;
  const h = Math.floor(left / 3600), m = Math.floor(left / 60) % 60, s = Math.floor(left) % 60;
  clock.textContent = `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  clock.className = `clock ${out ? "out" : low ? "low" : ""}`;
  bar.style.width = `${share * 100}%`;
  bar.className = out ? "out" : low ? "low" : "";
  if (left <= 0) timeUp();
}

async function timeUp() {
  const id = S.contest.id;
  S.contest = { ...S.contest, active: false };
  S.editor.updateOptions({ readOnly: true });
  await flushSave();
  const done = (await api("GET", "/api/history")).find((c) => c.id === id);
  summary(done || S.contest, "Time's up", home);
}

// ---------- views ----------

function showWork(on) {
  $("#right").hidden = !on;
  $("#gutter-v").hidden = !on;
  $("#empty").hidden = on;
}

async function home() {
  S.q = null;
  S.contest = null;
  renderLaps();
  showWork(false);
  const [state, history] = await Promise.all([api("GET", "/api/state"), api("GET", "/api/history")]);
  S.state = state;
  const count = (cat) => Object.values(state.bank[cat] || {}).reduce((a, b) => a + b, 0);
  const when = (t) => new Date(t * 1000).toLocaleString(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  const runs = history.map((c) => `
    <div class="run">
      <span class="when">${when(c.started_at)}</span>
      <span class="sc">${pct(c.score)}%</span>
      <span class="chips">${c.questions.map((q) => `<span class="chip ${q.solved ? "solved" : ""}" title="${esc(q.title)}">${esc(q.title)} ${pct(q.best)}%</span>`).join("")}</span>
    </div>`).join("");
  $("#left").innerHTML = `
    <h1 class="hero">Four problems. Ninety minutes. Write it like it ships.</h1>
    <p class="lede">Each problem grows in parts, the way real requirements do: get a part fully green and the next one
      unlocks. The mix covers practical Python, algorithms, and ML written from scratch with numpy and PyTorch.</p>
    <div class="bank">
      <div><b>${count("coding")}</b>coding questions</div>
      <div><b>${count("ml")}</b>ML questions</div>
      <div><b>${history.length}</b>contests finished</div>
    </div>
    <div class="history">
      <h2>Past contests</h2>
      ${runs || `<p class="lede">Nothing here yet. Your scores land here when a contest ends.</p>`}
    </div>`;
  $("#empty").innerHTML = `
    <div class="start">
      <div class="lineup" aria-hidden="true">
        <span style="background:var(--green)"></span><span style="background:var(--yellow)"></span>
        <span style="background:var(--yellow)"></span><span style="background:var(--red)"></span>
      </div>
      <p>One easy, two medium and one hard question. You get ${state.minutes} minutes, and each question opens once the one before it reaches 100%.</p>
      <button class="primary" data-new>Generate contest</button>
    </div>`;
}

async function openQuestion(i) {
  await flushSave();
  const q = await api("GET", `/api/contests/${S.contest.id}/q/${i}`).catch((e) => toast(e.message));
  if (!q) return;
  S.idx = i;
  S.q = q;
  showWork(true);
  renderStatement(q);
  setCode(q.code);
  S.editor.updateOptions({ readOnly: !S.contest.active });
  renderResults(S.results[i]);
  renderLaps();
  if (innerWidth > 860) S.editor.focus(); // on phones focus would jump past the statement
}

function renderStatement(q, scrollToNew = false) {
  const md = [q.intro, ...q.sections].filter(Boolean).join("\n\n");
  $("#left").innerHTML = `
    <h1 class="title">${esc(q.title)}</h1>
    <div class="tags">
      <span class="tag ${q.difficulty}">${q.difficulty[0].toUpperCase() + q.difficulty.slice(1)}</span>
      <span class="tag ${q.category}">${q.category === "ml" ? "ML" : "Coding"}</span>
      ${q.tags.map((t) => `<span class="tag">${esc(t)}</span>`).join("")}
    </div>
    <div class="md">${marked.parse(md)}</div>
    ${q.locked.map((t) => `<div class="locked"><b>${esc(t)}</b> unlocks when every test so far passes.</div>`).join("")}`;
  if (window.monaco) {
    document.querySelectorAll(".md pre code").forEach((code) => {
      monaco.editor.colorize(code.textContent, "python", {}).then((html) => { code.innerHTML = html; });
    });
  }
  if (scrollToNew) [...document.querySelectorAll(".md h2")].pop()?.scrollIntoView({ behavior: "smooth", block: "start" });
  else $("#left").scrollTop = 0;
}

function renderResults(r) {
  const box = $("#results");
  if (!r) {
    $("#score").textContent = "Run the tests to see how you're doing.";
    box.innerHTML = `<p class="group">Tests run for every part you've unlocked. Your code saves as you type.</p>`;
    return;
  }
  const full = r.pct >= 100;
  $("#score").innerHTML = `
    <span class="big ${full ? "full" : ""}">${pct(r.pct)}%</span>
    <span class="meter"><div style="width:${r.pct}%"></div></span>
    <span>${r.passed} of ${r.total} tests</span>`;
  const parts = [...new Set(r.tests.map((t) => t.part))].sort((a, b) => a - b);
  let html = r.error ? `<div class="err">${esc(r.error)}</div>` : "";
  for (const p of parts) {
    const ts = r.tests.filter((t) => t.part === p);
    if (ts.every((t) => t.ok === null)) {
      html += `<div class="group">Part ${p}: ${ts.length} tests, locked</div>`;
      continue;
    }
    html += `<div class="group">Part ${p}: ${ts.filter((t) => t.ok).length} of ${ts.length} passing</div>`;
    html += ts.map((t) => `
      <div class="row ${t.ok ? "" : "fail"}">
        <span class="mark">${t.ok ? "✓" : "✗"}</span><span>${esc(t.name)}</span><span class="ms">${t.ms ?? ""}${t.ms != null ? " ms" : ""}</span>
        ${t.ok ? "" : `<pre>${esc(t.msg)}</pre>`}
      </div>`).join("");
  }
  if (r.stdout) html += `<details class="out"><summary>Printed output</summary>${esc(r.stdout)}</details>`;
  box.innerHTML = html;
  box.scrollTop = 0;
}

// ---------- actions ----------

async function run() {
  if (S.busy || !S.q || !S.contest?.active) return;
  S.busy = true;
  const btn = $("#run-btn");
  btn.disabled = true;
  btn.firstChild.textContent = "Running ";
  clearTimeout(S.saveTimer);
  S.saveTimer = null;
  try {
    const r = await api("POST", `/api/contests/${S.contest.id}/q/${S.idx}/run`, { code: S.editor.getValue() });
    S.results[S.idx] = r;
    S.contest = r.contest;
    renderResults(r);
    renderLaps();
    if (r.solved) celebrate();
    else if (r.new_part) {
      S.q = await api("GET", `/api/contests/${S.contest.id}/q/${S.idx}`);
      renderStatement(S.q, true);
      toast(`Part ${r.part} unlocked. The new requirements are in the description.`);
    }
  } catch (e) {
    toast(e.message);
    if (e.message.includes("over")) boot();
  } finally {
    S.busy = false;
    btn.disabled = false;
    btn.firstChild.textContent = "Run tests ";
  }
}

async function newContest() {
  const live = S.contest?.active && !S.contest.questions.every((q) => q.solved);
  if (live && !confirm("End the current contest and start a new one?")) return;
  await flushSave();
  try {
    S.contest = await api("POST", "/api/contests");
  } catch (e) {
    return toast(e.message);
  }
  S.skew = S.contest.now - Date.now() / 1000;
  S.results = {};
  tick();
  openQuestion(0);
}

async function endContest() {
  if (!confirm("End this contest now? Your best scores are kept.")) return;
  await flushSave();
  const c = await api("POST", `/api/contests/${S.contest.id}/end`);
  S.contest = c;
  summary(c, "Contest ended", home);
}

function resetCode() {
  if (!S.q || !confirm("Replace your code with the starter code? This can't be undone.")) return;
  S.editor.setValue(S.q.starter);
}

$("#run-btn").addEventListener("click", run);
$("#reset-btn").addEventListener("click", resetCode);
$("#end-btn").addEventListener("click", endContest);
$("#new-btn").addEventListener("click", newContest);
document.addEventListener("click", (e) => { if (e.target.closest("[data-new]")) newContest(); });
document.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); run(); }
});

// ---------- feedback ----------

let toastTimer;
function toast(msg) {
  const t = $("#toast");
  t.textContent = msg;
  t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { t.hidden = true; }, 3600);
}

function modal(html, onClose) {
  const d = $("#modal");
  d.innerHTML = html;
  d.onclose = () => onClose?.();
  d.onclick = (e) => { if (e.target.closest("[data-close]")) d.close(); };
  d.showModal();
  d.querySelector("button")?.focus();
}

function summary(c, title, then) {
  modal(`
    <h2>${esc(title)}</h2>
    <p>Final score ${pct(c.score)}%, the average of your best run on each question.</p>
    <div class="summary">${c.questions.map((q, i) => `<div><span>${i + 1}. ${esc(q.title)}</span><b>${pct(q.best)}%</b></div>`).join("")}</div>
    <div class="actions"><button class="primary" data-close>Back to start</button></div>`, then);
}

function celebrate() {
  confetti();
  const qs = S.contest.questions;
  const next = qs.findIndex((q, i) => i > S.idx && !q.solved);
  const allDone = qs.every((q) => q.solved);
  const msg = allDone
    ? `That was the last one. You cleared all four questions with ${Math.max(0, Math.round((S.contest.ends_at - S.contest.ended_at) / 60))} minutes to spare.`
    : `Question ${S.idx + 1} passes every test. Question ${next + 1} is open now.`;
  modal(`
    <div class="cheer">
      <h2>Eyval, damet garm mashti!</h2>
      <p>${msg}</p>
      <div class="actions"><button class="primary" data-close>${allDone ? "See results" : `Start question ${next + 1}`}</button></div>
    </div>`, () => (allDone ? summary(S.contest, "Contest complete", home) : openQuestion(next)));
}

function confetti() {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const box = document.createElement("div");
  box.className = "confetti";
  const colors = ["#7aa2f7", "#9ece6a", "#e0af68", "#f7768e", "#bb9af7", "#7dcfff"];
  for (let i = 0; i < 90; i++) {
    const p = document.createElement("i");
    p.style.cssText = `left:${Math.random() * 100}%;background:${colors[i % colors.length]};` +
      `--x:${(Math.random() - 0.5) * 40}vw;--r:${Math.random() * 900 - 450}deg;--t:${1.6 + Math.random() * 1.4}s;--d:${Math.random() * 0.35}s`;
    box.append(p);
  }
  document.body.append(box);
  setTimeout(() => box.remove(), 3800);
}

// ---------- resizable panes ----------

function drag(gutter, onMove) {
  gutter.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    gutter.setPointerCapture(e.pointerId);
    gutter.classList.add("dragging");
    const up = () => {
      gutter.classList.remove("dragging");
      gutter.removeEventListener("pointermove", onMove);
      gutter.removeEventListener("pointerup", up);
    };
    gutter.addEventListener("pointermove", onMove);
    gutter.addEventListener("pointerup", up);
  });
}
const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
const setVar = (k, v) => document.documentElement.style.setProperty(k, `${v}%`);
let leftPct = 42, consolePct = 38;
drag($("#gutter-v"), (e) => {
  const r = $("#split").getBoundingClientRect();
  setVar("--left", (leftPct = clamp(((e.clientX - r.left) / r.width) * 100, 22, 70)));
});
drag($("#gutter-h"), (e) => {
  const r = $("#right").getBoundingClientRect();
  setVar("--console", (consolePct = clamp(((r.bottom - e.clientY) / r.height) * 100, 12, 80)));
});
$("#gutter-v").addEventListener("keydown", (e) => {
  const d = { ArrowLeft: -2, ArrowRight: 2 }[e.key];
  if (d) setVar("--left", (leftPct = clamp(leftPct + d, 22, 70)));
});
$("#gutter-h").addEventListener("keydown", (e) => {
  const d = { ArrowUp: 2, ArrowDown: -2 }[e.key];
  if (d) setVar("--console", (consolePct = clamp(consolePct + d, 12, 80)));
});

// ---------- start ----------

async function boot() {
  S.state = await api("GET", "/api/state");
  const c = S.state.contest;
  if (!c) return home();
  S.contest = c;
  S.skew = c.now - Date.now() / 1000;
  const open = c.questions.filter((q) => q.open);
  openQuestion(open[open.length - 1].idx);
}

(async () => {
  // Without the CDN, show statements as preformatted text rather than nothing.
  window.marked ||= { parse: (md) => `<pre>${esc(md)}</pre>`, setOptions() {} };
  marked.setOptions({ gfm: true });
  S.editor = await loadEditor();
  await boot().catch((e) => toast(e.message));
  setInterval(tick, 1000);
  tick();
})();
