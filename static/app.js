/* KaizenPrep front end: hash-routed single page app, no build step. */
(function () {
  const app = document.getElementById('app');
  const api = window.PrepAPI || {
    get: (u) => fetch(u).then(r => r.json()),
    post: (u, body) => fetch(u, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).then(r => r.json()),
  };
  const STATIC = !!window.PrepAPI;
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  };

  // ---------- theme ----------
  function applyTheme() {
    const t = store.get('theme', matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.dataset.theme = t;
  }
  document.getElementById('theme-btn').onclick = () => {
    store.set('theme', document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
    applyTheme();
    if (window._cm) window._cm.setOption('theme', document.documentElement.dataset.theme === 'dark' ? 'material-darker' : 'default');
  };
  applyTheme();

  // ---------- tiny markdown ----------
  function md(src) {
    const lines = String(src || '').split('\n');
    let out = '', i = 0, inList = null;
    const inline = (s) => esc(s)
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/(^|[^*])\*([^*]+)\*(?!\*)/g, '$1<em>$2</em>');
    const closeList = () => { if (inList) { out += `</${inList}>`; inList = null; } };
    while (i < lines.length) {
      const l = lines[i];
      if (l.startsWith('```')) {
        closeList();
        let code = ''; i++;
        while (i < lines.length && !lines[i].startsWith('```')) { code += lines[i] + '\n'; i++; }
        out += `<pre><code>${esc(code)}</code></pre>`; i++; continue;
      }
      const h = l.match(/^(#{1,4})\s+(.*)/);
      if (h) { closeList(); out += `<h3>${inline(h[2])}</h3>`; i++; continue; }
      const ul = l.match(/^\s*[-*]\s+(.*)/), ol = l.match(/^\s*\d+[.)]\s+(.*)/);
      if (ul || ol) {
        const tag = ul ? 'ul' : 'ol';
        if (inList !== tag) { closeList(); out += `<${tag}>`; inList = tag; }
        out += `<li>${inline((ul || ol)[1])}</li>`; i++; continue;
      }
      if (l.trim() === '') { closeList(); i++; continue; }
      closeList();
      let para = l; i++;
      while (i < lines.length && lines[i].trim() !== '' && !/^(#{1,4}\s|\s*[-*]\s|\s*\d+[.)]\s|```)/.test(lines[i])) { para += ' ' + lines[i]; i++; }
      out += `<p>${inline(para)}</p>`;
    }
    closeList();
    return out;
  }

  // ---------- router ----------
  const routes = [];
  function route(re, fn) { routes.push([re, fn]); }
  let currentRoute = null;
  function go(path) { currentRoute = path; try { if (location.hash !== '#' + path) history.replaceState(null, '', '#' + path); } catch {} render(); }
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#/"]'); if (!a) return;
    e.preventDefault(); go(a.getAttribute('href').slice(1));
  });
  async function render() {
    const hash = currentRoute || (location.hash.startsWith('#/') ? location.hash.slice(1) : '/');
    document.title = 'KaizenPrep';
    document.querySelectorAll('#topbar nav a').forEach(a => a.classList.toggle('active', hash === a.dataset.nav || (a.dataset.nav !== '/' && hash.startsWith(a.dataset.nav))));
    if (window._cm) { window._cm = null; }
    if (window._stopwatch) { clearInterval(window._stopwatch); window._stopwatch = null; }
    for (const [re, fn] of routes) {
      const m = hash.match(re);
      if (m) { app.innerHTML = '<div class="page muted">Loading…</div>'; await fn(...m.slice(1)); window.scrollTo(0, 0); return; }
    }
    app.innerHTML = '<div class="page">Not found.</div>';
  }
  window.addEventListener('hashchange', () => { currentRoute = null; render(); });

  const diffPill = (d) => `<span class="pill ${d.toLowerCase()}">${d}</span>`;
  const statusIcon = (s) => s === 'solved' ? '<span class="st-solved" title="Solved">✔</span>' : s === 'attempted' ? '<span class="st-attempted" title="Attempted">◔</span>' : '<span class="muted">·</span>';
  const companyChips = (c) => Object.entries(c || {}).filter(([, v]) => v >= 3).sort((a, b) => b[1] - a[1]).map(([k]) => `<span class="pill company ${k}">${k[0].toUpperCase() + k.slice(1)}</span>`).join('');

  // ---------- dashboard ----------
  route(/^\/$/, async () => {
    const [{ stats, reviews }, { problems }] = await Promise.all([api.get('/api/stats'), api.get('/api/problems')]);
    const pct = (a, b) => b ? Math.round(100 * a / b) : 0;
    const d = stats.by_difficulty;
    const days = new Set(stats.active_days);
    let heat = '';
    for (let k = 89; k >= 0; k--) { const dt = new Date(); dt.setDate(dt.getDate() - k); const key = dt.toISOString().slice(0, 10); heat += `<i class="${days.has(key) ? 'on' : ''}" title="${key}"></i>`; }
    const next = problems.filter(p => p.status !== 'solved').slice(0, 5);
    app.innerHTML = `<div class="page">
      <h1>Dashboard</h1>
      <p class="lead">A practice platform modelled on the public LeetCode problem page: ${problems.length} problems written from scratch, a judge that runs your Python against hidden tests${STATIC ? ' right in this browser' : ''}, spaced-repetition reviews, an 8-week plan, and Google and Apple tracks.${STATIC ? ' Progress is saved in this browser only.' : ''}</p>
      <div class="grid cols-3">
        <div class="card"><div class="muted small">Solved</div><div class="stat">${stats.solved}<small>/ ${stats.total}</small></div>
          <div class="bar"><i style="width:${pct(stats.solved, stats.total)}%"></i></div>
          <div class="small muted" style="margin-top:8px">Easy ${d.Easy[0]}/${d.Easy[1]} · Medium ${d.Medium[0]}/${d.Medium[1]} · Hard ${d.Hard[0]}/${d.Hard[1]}</div>
          <div class="bar easy"><i style="width:${pct(d.Easy[0], d.Easy[1])}%"></i></div>
          <div class="bar medium"><i style="width:${pct(d.Medium[0], d.Medium[1])}%"></i></div>
          <div class="bar hard"><i style="width:${pct(d.Hard[0], d.Hard[1])}%"></i></div></div>
        <div class="card"><div class="muted small">Streak</div><div class="stat">${stats.streak}<small>days</small></div><div class="small muted" style="margin:8px 0">Last 90 days</div><div class="heat">${heat}</div></div>
        <div class="card"><div class="muted small">Reviews due</div><div class="stat">${reviews.length}</div>
          ${reviews.length ? '<ul class="plain small" style="margin:8px 0 0">' + reviews.slice(0, 6).map(r => `<li><a href="#/problem/${r.id}">${esc(r.title)}</a> <span class="muted">${r.due}</span></li>`).join('') + '</ul>' : '<div class="small muted" style="margin-top:8px">Nothing due. Solved problems come back after 1, 3, 7, 14, 30 and 60 days.</div>'}
        </div>
      </div>
      <div class="grid cols-2" style="margin-top:14px">
        <div class="card"><h2 style="margin-top:0">Up next</h2>
          <ul class="plain" style="padding-left:0;list-style:none">${next.map(p => `<li class="row" style="padding:4px 0">${statusIcon(p.status)} <a href="#/problem/${p.id}">${p.number}. ${esc(p.title)}</a> ${diffPill(p.difficulty)}</li>`).join('')}</ul>
          <div class="row" style="margin-top:10px"><a class="btn accent" href="#/plan">Open the 8-week plan</a><button class="btn" id="rand">Random unsolved</button></div></div>
        <div class="card"><h2 style="margin-top:0">Progress by pattern</h2>
          <div class="mix">${Object.entries(stats.by_pattern).map(([k, [a, b]]) => `<span>${esc(k)}</span><div class="bar" style="margin:0"><i style="width:${pct(a, b)}%"></i></div><span class="small muted">${a}/${b}</span>`).join('')}</div></div>
      </div>
      <h2>How to use this well</h2>
      <div class="card"><ol class="steps">
        <li><b>Follow the plan.</b> Six days a week, one pattern block per week, 3-5 problems a day. Open hints after 25 minutes, the editorial after 40.</li>
        <li><b>Read every editorial</b>, including for problems you solved. The follow-ups at the end are what separates a pass from a strong hire.</li>
        <li><b>Do the reviews.</b> When a solved problem comes back, write it from memory and rate it. The schedule stretches as you get reliable.</li>
        <li><b>Mock weekly from week 4.</b> Two problems, 45 minutes, talk out loud, no hints. Use the Google or Apple mock depending on your target.</li>
        <li><b>Keep notes.</b> The Notes tab on each problem is for the one-line insight you would want to remember in the interview.</li>
      </ol></div>
    </div>`;
    document.getElementById('rand').onclick = async () => { const r = await api.get('/api/random'); go('/problem/' + r.id); };
  });

  // ---------- problem list ----------
  route(/^\/problems$/, async () => {
    const { problems, patterns } = await api.get('/api/problems');
    const f = store.get('filters', { q: '', diff: '', pattern: '', company: '', status: '' });
    app.innerHTML = `<div class="page">
      <h1>Problems</h1>
      <div class="filters">
        <input id="f-q" placeholder="Search title or tag" value="${esc(f.q)}">
        <select id="f-diff"><option value="">Difficulty</option>${['Easy', 'Medium', 'Hard'].map(d => `<option ${f.diff === d ? 'selected' : ''}>${d}</option>`).join('')}</select>
        <select id="f-pattern"><option value="">Pattern</option>${patterns.map(p => `<option ${f.pattern === p ? 'selected' : ''}>${esc(p)}</option>`).join('')}</select>
        <select id="f-company"><option value="">Company</option>${['google', 'apple', 'meta', 'amazon', 'microsoft'].map(c => `<option value="${c}" ${f.company === c ? 'selected' : ''}>${c[0].toUpperCase() + c.slice(1)}</option>`).join('')}</select>
        <select id="f-status"><option value="">Status</option><option value="todo" ${f.status === 'todo' ? 'selected' : ''}>Todo</option><option value="attempted" ${f.status === 'attempted' ? 'selected' : ''}>Attempted</option><option value="solved" ${f.status === 'solved' ? 'selected' : ''}>Solved</option><option value="starred" ${f.status === 'starred' ? 'selected' : ''}>Starred</option></select>
        <button class="btn" id="f-clear">Clear</button><span class="muted small" id="count"></span>
      </div>
      <table class="plist"><thead><tr><th></th><th>#</th><th>Title</th><th>Difficulty</th><th>Pattern</th><th>Companies</th><th></th></tr></thead><tbody id="rows"></tbody></table>
    </div>`;
    const ids = ['q', 'diff', 'pattern', 'company', 'status'];
    const read = () => ({ q: $('#f-q').value.trim().toLowerCase(), diff: $('#f-diff').value, pattern: $('#f-pattern').value, company: $('#f-company').value, status: $('#f-status').value });
    function draw() {
      const f = read(); store.set('filters', f);
      const rows = problems.filter(p =>
        (!f.q || p.title.toLowerCase().includes(f.q) || p.tags.some(t => t.toLowerCase().includes(f.q)) || p.pattern.toLowerCase().includes(f.q)) &&
        (!f.diff || p.difficulty === f.diff) && (!f.pattern || p.pattern === f.pattern) &&
        (!f.company || (p.companies[f.company] || 0) >= 3) &&
        (!f.status || (f.status === 'todo' ? !p.status : f.status === 'starred' ? p.starred : p.status === f.status)));
      $('#count').textContent = `${rows.length} problems`;
      $('#rows').innerHTML = rows.map(p => `<tr>
        <td class="status">${statusIcon(p.status)}</td><td class="muted">${p.number}</td>
        <td><a href="#/problem/${p.id}">${esc(p.title)}</a></td><td>${diffPill(p.difficulty)}</td>
        <td class="small">${esc(p.pattern)}</td><td><div class="chips">${companyChips(p.companies)}</div></td>
        <td><span class="star ${p.starred ? 'on' : ''}" data-id="${p.id}" title="Star">★</span></td></tr>`).join('');
      $('#rows').querySelectorAll('.star').forEach(s => s.onclick = async () => { const r = await api.post('/api/star', { id: s.dataset.id }); s.classList.toggle('on', r.starred); problems.find(p => p.id === s.dataset.id).starred = r.starred; });
    }
    ids.forEach(i => $('#f-' + i).addEventListener('input', draw));
    $('#f-clear').onclick = () => { ids.forEach(i => $('#f-' + i).value = ''); draw(); };
    draw();
  });

  // ---------- problem workspace ----------
  route(/^\/problem\/([\w-]+)$/, async (id) => {
    const p = await api.get('/api/problem/' + id);
    if (p.error) { app.innerHTML = '<div class="page">Problem not found.</div>'; return; }
    document.title = `${p.number}. ${p.title} - KaizenPrep`;
    const mock = store.get('mock', null);
    app.innerHTML = `<div class="workspace">
      <section class="pane">
        <div class="pane-tabs" id="left-tabs">
          <button data-tab="desc" class="active">Description</button><button data-tab="edit">Editorial</button><button data-tab="subs">Submissions</button><button data-tab="notes">Notes</button>
          <span class="spacer"></span>
          <a class="btn sm" href="#/problems" title="Problem list">☰</a>
          ${p.prev ? `<a class="btn sm" href="#/problem/${p.prev.id}" title="${esc(p.prev.title)}">‹</a>` : ''}
          ${p.next ? `<a class="btn sm" href="#/problem/${p.next.id}" title="${esc(p.next.title)}">›</a>` : ''}
          <button class="btn sm" id="rand" title="Random unsolved">⤭</button>
        </div>
        <div class="pane-body" id="left-body"></div>
      </section>
      <section class="pane">
        <div class="editor-toolbar">
          <span>Python 3</span><span class="muted">·</span><span id="saved" class="muted">Draft</span>
          <span class="spacer"></span>
          <span class="stopwatch" id="sw">00:00</span><button class="btn sm" id="sw-btn">Start</button>
          <button class="btn sm" id="reset" title="Reset to starter code">↺</button>
          <button class="btn sm" id="run">▶ Run</button><button class="btn sm primary" id="submit">Submit</button>
        </div>
        <div class="editor-wrap" id="editor-wrap"></div>
        <div class="console">
          <div class="pane-tabs"><button data-ctab="cases" class="active">Testcase</button><button data-ctab="result">Test result</button><span class="spacer"></span><span class="small muted"><kbd>⌘/Ctrl</kbd>+<kbd>Enter</kbd> run · <kbd>⇧</kbd>+<kbd>Enter</kbd> submit</span></div>
          <div class="pane-body" id="console-body"></div>
        </div>
      </section>
    </div>`;

    // ---- left pane tabs ----
    const left = $('#left-body');
    const tabs = {
      desc: () => `<h2 class="ptitle">${p.number}. ${esc(p.title)}</h2>
        <div class="row" style="margin-bottom:12px;flex-wrap:wrap">${diffPill(p.difficulty)}<span class="pill">${esc(p.pattern)}</span>${companyChips(p.companies)}<span class="star ${p.starred ? 'on' : ''}" id="star" title="Star">★</span>${p.status === 'solved' ? '<span class="pill easy">Solved · review ' + esc(p.next_review) + '</span>' : ''}</div>
        <div class="desc md">${md(p.description)}</div>
        ${p.examples.map((e, i) => `<div class="sec-title">Example ${i + 1}</div><div class="example"><div><b>Input:</b> <code>${esc(e.input)}</code></div><div><b>Output:</b> <code>${esc(e.output)}</code></div>${e.explanation ? `<div><b>Explanation:</b> ${esc(e.explanation)}</div>` : ''}</div>`).join('')}
        <div class="sec-title">Constraints</div><ul class="plain">${p.constraints.map(c => `<li><code>${esc(c)}</code></li>`).join('')}</ul>
        <div class="sec-title">Hints</div>${p.hints.map((h, i) => `<details class="hint"><summary>Hint ${i + 1}</summary><p>${esc(h)}</p></details>`).join('')}
        <div class="sec-title">Topics</div><div class="chips">${p.tags.map(t => `<span class="pill">${esc(t)}</span>`).join('')}</div>
        ${p.similar.length ? `<div class="sec-title">Similar questions</div><ul class="similar">${p.similar.map(s => `<li><a href="#/problem/${s.id}">${esc(s.title)}</a> ${diffPill(s.difficulty)}</li>`).join('')}</ul>` : ''}
        <div class="sec-title">Company frequency</div><div class="small muted">${Object.entries(p.companies).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k[0].toUpperCase() + k.slice(1)} ${'●'.repeat(v)}${'○'.repeat(5 - v)}`).join(' &nbsp; ')}<br>Scores are an estimate from public interview reports, not an official tag.</div>`,
      edit: () => `<h2 class="ptitle">Editorial</h2><div class="md">${md(p.approach)}</div>
        <div class="sec-title">Complexity</div><p>Time <code>${esc(p.complexity.time)}</code> · Space <code>${esc(p.complexity.space)}</code></p>
        ${p.followups.length ? `<div class="sec-title">Follow-ups</div><ul class="plain">${p.followups.map(f => `<li>${esc(f)}</li>`).join('')}</ul>` : ''}
        <div class="sec-title">Reference solution</div><pre><code>${esc(p.solution)}</code></pre><button class="btn sm" id="load-sol">Load into editor</button>`,
      subs: () => `<h2 class="ptitle">Submissions</h2>${p.submissions.length ? p.submissions.map((s, i) => `<div class="sub-row" data-i="${i}"><span class="${s.status === 'Accepted' ? 'ok' : 'bad'}">${esc(s.status)}</span><span class="muted small">${s.passed}/${s.total} tests · ${s.ms} ms · ${esc(s.at.replace('T', ' '))}</span><span class="muted small">click to load</span></div>`).join('') : '<p class="muted">No submissions yet.</p>'}`,
      notes: () => `<h2 class="ptitle">Notes</h2><p class="muted small">One line about the key idea you want to remember. Saved automatically.</p><textarea class="note" id="note">${esc(p.note)}</textarea>`,
    };
    function showTab(name) {
      $('#left-tabs').querySelectorAll('button[data-tab]').forEach(b => b.classList.toggle('active', b.dataset.tab === name));
      left.innerHTML = tabs[name]();
      if (name === 'desc') $('#star').onclick = async () => { const r = await api.post('/api/star', { id }); p.starred = r.starred; $('#star').classList.toggle('on', r.starred); };
      if (name === 'edit') $('#load-sol').onclick = () => setCode(p.solution);
      if (name === 'subs') left.querySelectorAll('.sub-row').forEach(r => r.onclick = () => setCode(p.submissions[+r.dataset.i].code));
      if (name === 'notes') { let t; $('#note').oninput = (e) => { clearTimeout(t); t = setTimeout(() => api.post('/api/note', { id, note: e.target.value }), 500); }; }
    }
    $('#left-tabs').querySelectorAll('button[data-tab]').forEach(b => b.onclick = () => showTab(b.dataset.tab));
    showTab('desc');
    $('#rand').onclick = async () => { const r = await api.get('/api/random'); go('/problem/' + r.id); };

    // ---- editor ----
    const wrap = $('#editor-wrap');
    let cm = null, ta = null;
    const initial = p.draft || p.starter;
    if (window.CodeMirror) {
      cm = CodeMirror(wrap, { value: initial, mode: 'python', lineNumbers: true, indentUnit: 4, tabSize: 4, matchBrackets: true, autoCloseBrackets: true,
        theme: document.documentElement.dataset.theme === 'dark' ? 'material-darker' : 'default', extraKeys: { Tab: (c) => c.execCommand('indentMore'), 'Shift-Tab': (c) => c.execCommand('indentLess') } });
      window._cm = cm;
    } else {
      ta = document.createElement('textarea'); ta.className = 'plain-editor'; ta.value = initial; wrap.appendChild(ta);
    }
    const getCode = () => cm ? cm.getValue() : ta.value;
    const setCode = (v) => { cm ? cm.setValue(v) : (ta.value = v); };
    let saveT; const onChange = () => { $('#saved').textContent = 'Unsaved'; clearTimeout(saveT); saveT = setTimeout(async () => { await api.post('/api/draft', { id, code: getCode() }); $('#saved').textContent = 'Saved'; }, 800); };
    cm ? cm.on('change', onChange) : ta.addEventListener('input', onChange);
    let resetArmed = null;
    $('#reset').onclick = () => {
      if (resetArmed) { clearTimeout(resetArmed); resetArmed = null; $('#reset').textContent = '↺'; setCode(p.starter); return; }
      $('#reset').textContent = 'Reset? click again'; resetArmed = setTimeout(() => { resetArmed = null; $('#reset').textContent = '↺'; }, 3000);
    };

    // ---- stopwatch ----
    let swStart = null, swElapsed = 0;
    const fmt = (ms) => { const s = Math.floor(ms / 1000); return String(Math.floor(s / 60)).padStart(2, '0') + ':' + String(s % 60).padStart(2, '0'); };
    $('#sw-btn').onclick = () => {
      if (swStart) { swElapsed += Date.now() - swStart; swStart = null; $('#sw-btn').textContent = 'Start'; clearInterval(window._stopwatch); }
      else { swStart = Date.now(); $('#sw-btn').textContent = 'Pause'; window._stopwatch = setInterval(() => $('#sw').textContent = fmt(swElapsed + Date.now() - swStart), 500); }
    };

    // ---- console ----
    const cbody = $('#console-body');
    let activeCase = 0, lastResult = null, customInput = store.get('custom:' + id, '');
    const caseInput = (c) => Object.entries(c.input).map(([k, v]) => `<div class="kv"><label>${esc(k)} =</label><pre>${esc(JSON.stringify(v))}</pre></div>`).join('');
    function showConsole(name) {
      cbody.parentElement.querySelectorAll('button[data-ctab]').forEach(b => b.classList.toggle('active', b.dataset.ctab === name));
      if (name === 'cases') {
        const cases = p.visible_tests;
        cbody.innerHTML = `<div class="case-tabs">${cases.map((_, i) => `<button data-case="${i}" class="${activeCase === i ? 'active' : ''}">Case ${i + 1}</button>`).join('')}<button data-case="custom" class="${activeCase === 'custom' ? 'active' : ''}">+ Custom</button></div><div id="case-body"></div>`;
        const body = $('#case-body');
        if (activeCase === 'custom') {
          body.innerHTML = `<div class="kv"><label>Input as JSON object keyed by parameter name${p.kind === 'design' ? ' ({"ops": [[...], ...]})' : ''}</label><textarea id="custom-in">${esc(customInput || JSON.stringify(cases[0].input))}</textarea></div><div class="small muted">Custom inputs run with Run and show the output only (no expected value).</div>`;
          $('#custom-in').oninput = (e) => { customInput = e.target.value; store.set('custom:' + id, customInput); };
        } else body.innerHTML = caseInput(cases[activeCase]) + `<div class="small muted">Expected: <code>${esc(JSON.stringify(cases[activeCase].output))}</code> · ${p.hidden_count} more hidden tests run on Submit.</div>`;
        cbody.querySelectorAll('button[data-case]').forEach(b => b.onclick = () => { activeCase = b.dataset.case === 'custom' ? 'custom' : +b.dataset.case; showConsole('cases'); });
      } else {
        if (!lastResult) { cbody.innerHTML = '<p class="muted">Run or submit your code to see results here.</p>'; return; }
        const r = lastResult;
        const ok = r.status === 'Accepted';
        let html = `<div class="verdict ${ok ? 'ok' : 'bad'}">${esc(r.status)}<small>${r.passed}/${r.total} passed · ${r.ms} ms${r.submitted ? ' · submitted' : ''}</small></div>`;
        if (r.stderr && r.status !== 'Wrong Answer') html += `<pre class="kv">${esc(r.stderr)}</pre>`;
        if (r.cases.length) {
          html += `<div class="case-tabs">${r.cases.map((c, i) => `<button data-rcase="${i}" class="${c.ok ? 'pass' : 'fail'} ${i === (r._active || 0) ? 'active' : ''}">${c.custom ? 'Custom' : 'Case ' + (i + 1)}</button>`).join('')}</div>`;
          const c = r.cases[r._active || 0];
          html += caseInput(c);
          if (c.error) html += `<div class="kv"><label>Error</label><pre>${esc(c.error)}\n${esc(c.trace || '')}</pre></div>`;
          else html += `<div class="kv"><label>Output</label><pre>${esc(JSON.stringify(c.output))}</pre></div>` + (c.custom ? '' : `<div class="kv"><label>Expected</label><pre>${esc(JSON.stringify(c.expected))}</pre></div>`);
        }
        if (r.stdout) html += `<div class="kv"><label>stdout</label><pre>${esc(r.stdout)}</pre></div>`;
        if (r.submitted && ok) html += `<div class="rate"><span class="small muted">Review in ${esc(r.entry.next_review)}. How did it feel?</span><button class="btn sm" data-rate="again">Again</button><button class="btn sm" data-rate="hard">Hard</button><button class="btn sm" data-rate="easy">Easy</button></div>`;
        cbody.innerHTML = html;
        cbody.querySelectorAll('button[data-rcase]').forEach(b => b.onclick = () => { r._active = +b.dataset.rcase; showConsole('result'); });
        cbody.querySelectorAll('button[data-rate]').forEach(b => b.onclick = async () => { const e = await api.post('/api/rate', { id, rating: b.dataset.rate }); r.entry.next_review = e.next_review; cbody.querySelector('.rate').innerHTML = `<span class="small muted">Next review ${esc(e.next_review)}.</span>`; });
      }
    }
    cbody.parentElement.querySelectorAll('button[data-ctab]').forEach(b => b.onclick = () => showConsole(b.dataset.ctab));
    showConsole('cases');

    async function run(submit) {
      const btn = submit ? $('#submit') : $('#run');
      $('#run').disabled = $('#submit').disabled = true; btn.textContent = submit ? 'Judging…' : (STATIC && !window.__pyReady ? 'Loading Python…' : 'Running…');
      try {
        const body = { id, code: getCode() };
        if (!submit && activeCase === 'custom' && customInput.trim()) {
          try { body.custom = [JSON.parse(customInput)]; } catch { lastResult = { status: 'Invalid custom input', passed: 0, total: 0, ms: 0, cases: [], stderr: 'Custom input must be a JSON object keyed by parameter name.' }; showConsole('result'); return; }
        }
        const r = await api.post(submit ? '/api/submit' : '/api/run', body);
        window.__pyReady = true;
        r.submitted = submit; r._active = Math.max(0, r.cases.findIndex(c => !c.ok));
        lastResult = r; showConsole('result');
        if (submit && r.status === 'Accepted') { p.status = 'solved'; p.next_review = r.entry.next_review; }
        if (submit) { p.submissions = (await api.get('/api/problem/' + id)).submissions; }
      } finally { $('#run').disabled = $('#submit').disabled = false; $('#run').textContent = '▶ Run'; $('#submit').textContent = 'Submit'; }
    }
    if (STATIC && api.warm) api.warm();
    $('#run').onclick = () => run(false);
    $('#submit').onclick = () => run(true);
    const keys = (e) => { if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') { e.preventDefault(); run(e.shiftKey); } };
    wrap.addEventListener('keydown', keys);
  });

  // ---------- study plan ----------
  route(/^\/plan$/, async () => {
    const plan = await api.get('/api/plan');
    const open = store.get('plan-open', 1);
    app.innerHTML = `<div class="page">
      <h1>8-week study plan</h1>
      <p class="lead">One pattern block per week, six study days, problems ordered easy to hard within the block. Week 8 is design, strings, review and mocks. Adjust the pace: if you have 4 weeks, do two weeks per week and skip the Hard problems on the first pass.</p>
      <div class="card"><div class="sec-title" style="margin-top:0">Daily routine</div><ol class="steps">${plan.daily_routine.map(s => `<li>${esc(s)}</li>`).join('')}</ol></div>
      <h2>Weeks</h2>
      ${plan.weeks.map(w => `<details class="week" ${w.week === open ? 'open' : ''} data-week="${w.week}"><summary>Week ${w.week}: ${esc(w.title)}<span class="pill ${w.done === w.total ? 'easy' : ''}">${w.done}/${w.total}</span></summary>
        <div class="small muted" style="margin:6px 0 4px">${w.patterns.map(esc).join(' · ')}</div>
        ${w.days.map((d, i) => `<div class="day"><h4>Day ${i + 1}</h4><ul>${d.map(p => `<li>${statusIcon(p.status)} <a href="#/problem/${p.id}">${p.number}. ${esc(p.title)}</a> ${diffPill(p.difficulty)}</li>`).join('') || '<li class="muted">Rest or review day</li>'}</ul></div>`).join('')}
        ${w.extras.length ? `<div class="day"><h4>Also this week</h4><ul>${w.extras.map(e => `<li>• ${esc(e)}</li>`).join('')}</ul></div>` : ''}
      </details>`).join('')}
    </div>`;
    app.querySelectorAll('details.week').forEach(d => d.addEventListener('toggle', () => { if (d.open) store.set('plan-open', +d.dataset.week); }));
  });

  // ---------- pattern cheat sheet ----------
  route(/^\/patterns$/, async () => {
    const { patterns } = await api.get('/api/patterns');
    const { problems } = await api.get('/api/problems');
    app.innerHTML = `<div class="page">
      <h1>Pattern cheat sheet</h1>
      <p class="lead">The 19 techniques behind every problem in the bank: when to recognise each one, a template you should be able to write from memory, and the traps interviewers watch for. Revisit this the night before an interview.</p>
      ${patterns.map(pt => { const ps = problems.filter(p => p.pattern === pt.name); const solved = ps.filter(p => p.status === 'solved').length; return `<details class="week"><summary>${esc(pt.name)}<span class="pill ${solved === ps.length && ps.length ? 'easy' : ''}">${solved}/${ps.length}</span></summary>
        <div class="sec-title">When to use it</div><p>${esc(pt.signal)}</p>
        <div class="sec-title">Template</div><pre><code>${esc(pt.template)}</code></pre>
        <div class="sec-title">Pitfalls</div><ul class="plain">${pt.pitfalls.map(x => `<li>${esc(x)}</li>`).join('')}</ul>
        <div class="sec-title">Problems</div><div class="chips">${ps.map(p => `<a class="pill ${p.status === 'solved' ? 'easy' : ''}" href="#/problem/${p.id}">${esc(p.title)}</a>`).join('')}</div>
      </details>`; }).join('')}
    </div>`;
  });

  // ---------- company tracks ----------
  route(/^\/track\/(google|apple)$/, async (company) => {
    const t = await api.get('/api/track/' + company);
    const li = (p) => `<li>${statusIcon(p.status)}<span class="score">${'●'.repeat(p.score)}</span><a href="#/problem/${p.id}">${p.number}. ${esc(p.title)}</a>${diffPill(p.difficulty)}<span class="small muted">${esc(p.pattern)}</span></li>`;
    app.innerHTML = `<div class="page">
      <h1>${esc(t.name)} track</h1>
      <p class="lead">${esc(t.summary)}</p>
      <div class="notice">Frequency scores are an estimate built from public interview reports and prep communities, not an official company tag. Use the ordering as a prior; the patterns matter more than the exact problems.</div>
      <div class="grid cols-2">
        <div class="card"><h2 style="margin-top:0">Interview process</h2><ul class="plain">${t.process.map(s => `<li>${esc(s)}</li>`).join('')}</ul></div>
        <div class="card"><h2 style="margin-top:0">What they emphasise</h2><ul class="plain">${t.focus.map(s => `<li>${esc(s)}</li>`).join('')}</ul></div>
      </div>
      <div class="grid cols-2" style="margin-top:14px">
        <div class="card"><h2 style="margin-top:0">Tips from the loop</h2><ul class="plain">${t.tips.map(s => `<li>${esc(s)}</li>`).join('')}</ul></div>
        <div class="card"><h2 style="margin-top:0">Pattern mix at ${esc(t.name)}</h2><div class="mix">${t.pattern_mix.map(m => `<span>${esc(m.pattern)}</span><div class="bar" style="margin:0"><i style="width:${Math.min(100, m.share * 2)}%"></i></div><span class="small muted">${m.share}%</span>`).join('')}</div></div>
      </div>
      <div class="row" style="margin:18px 0 6px"><h2 style="margin:0">Must do (${t.must_do.length})</h2><a class="btn sm" href="#/mock?company=${company}">Start a ${esc(t.name)} mock</a></div>
      <div class="card"><ul class="track-list">${t.must_do.map(li).join('')}</ul></div>
      <h2>Also frequently reported (${t.also.length})</h2>
      <div class="card"><ul class="track-list">${t.also.map(li).join('')}</ul></div>
    </div>`;
  });

  // ---------- mock interview ----------
  route(/^\/mock(?:\?company=(\w+))?$/, async (company) => {
    const mock = store.get('mock', null);
    const sel = company || (mock && mock.company) || 'google';
    app.innerHTML = `<div class="page">
      <h1>Mock interview</h1>
      <p class="lead">Two problems, 45 minutes, like a real loop round. Talk out loud, state the brute force, ask clarifying questions to yourself, and only run the code when you believe it is correct. No hints, no editorial until the timer ends.</p>
      <div class="card">
        <div class="row"><label>Style</label><select id="mock-company" class="btn"><option value="google" ${sel === 'google' ? 'selected' : ''}>Google (graphs, DP, follow-ups)</option><option value="apple" ${sel === 'apple' ? 'selected' : ''}>Apple (arrays, strings, lists, design)</option></select>
        <button class="btn primary" id="mock-start">Start new mock</button>${mock ? '<button class="btn" id="mock-end">End current mock</button>' : ''}</div>
        <div id="mock-body" style="margin-top:14px">${mock ? renderMock(mock) : '<p class="muted">No mock in progress.</p>'}</div>
      </div>
      <h2>Scoring yourself afterwards</h2>
      <div class="card"><ul class="plain">
        <li><b>Problem navigation:</b> Did you restate the problem and ask about constraints before coding?</li>
        <li><b>Algorithm:</b> Did you reach the optimal complexity, and say it out loud?</li>
        <li><b>Coding:</b> Would the code compile on the first try? Variable names clear? Edge cases handled?</li>
        <li><b>Verification:</b> Did you trace an example by hand before running?</li>
        <li><b>Communication:</b> Could an interviewer follow you without reading the code?</li>
      </ul></div>
    </div>`;
    function renderMock(m) {
      return `<div class="small muted">Started ${esc(new Date(m.started).toLocaleString())} · ${m.company} style</div><ul class="track-list">${m.problems.map(p => `<li><a href="#/problem/${p.id}">${p.number}. ${esc(p.title)}</a>${diffPill(p.difficulty)}<span class="small muted">${esc(p.pattern)}</span></li>`).join('')}</ul>`;
    }
    $('#mock-start').onclick = async () => {
      const c = $('#mock-company').value;
      const r = await api.get('/api/mock?company=' + c);
      const m = { company: c, problems: r.problems, started: Date.now(), minutes: r.minutes };
      store.set('mock', m); tickMock(); go('/problem/' + m.problems[0].id);
    };
    const end = $('#mock-end'); if (end) end.onclick = () => { store.set('mock', null); tickMock(); render(); };
  });

  function tickMock() {
    const el = document.getElementById('mock-timer');
    const m = store.get('mock', null);
    if (!m) { el.classList.add('hidden'); return; }
    const left = m.minutes * 60 * 1000 - (Date.now() - m.started);
    const s = Math.floor(Math.abs(left) / 1000);
    el.textContent = `${left < 0 ? '-' : ''}${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')} mock`;
    el.classList.toggle('late', left < 0); el.classList.remove('hidden');
    el.onclick = () => go('/mock');
  }
  setInterval(tickMock, 1000); tickMock();

  function $(sel) { return app.querySelector(sel); }
  render();
})();
