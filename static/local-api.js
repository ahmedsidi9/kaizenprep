/* In-browser replacement for server.py: same URL contract, data from static JSON files,
   progress in localStorage, judging in a Pyodide Web Worker. Loaded before app.js. */
(function () {
  const TIMEOUT_MS = 12000;
  const PKEY = 'prepcode:progress';
  let index = null, tracksData = null, patternsData = null, mleData = null;
  const problemCache = {};

  const fetchJson = (u) => fetch(u).then(r => { if (!r.ok) throw new Error(u + ' ' + r.status); return r.json(); });
  async function loadIndex() {
    if (!index) {
      [index, tracksData, patternsData, mleData] = await Promise.all([fetchJson('data/index.json'), fetchJson('data/tracks.json'), fetchJson('data/patterns.json'), fetchJson('data/apple-mle.json')]);
    }
    return index;
  }
  async function loadProblem(id) {
    if (!problemCache[id]) problemCache[id] = await fetchJson('data/problems/' + id + '.json');
    return problemCache[id];
  }

  // ---------- progress ----------
  function loadProgress() { try { return JSON.parse(localStorage.getItem(PKEY)) || { problems: {}, submissions: [] }; } catch { return { problems: {}, submissions: [] }; } }
  function saveProgress(d) { try { localStorage.setItem(PKEY, JSON.stringify(d)); } catch {} }
  const today = () => new Date().toISOString().slice(0, 10);
  const plusDays = (n) => { const d = new Date(); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); };
  const nowIso = () => new Date().toISOString().slice(0, 19);
  const INTERVALS = () => (tracksData && tracksData.intervals) || [1, 3, 7, 14, 30, 60];

  function recordSubmission(pid, code, result) {
    const data = loadProgress();
    const p = data.problems[pid] = data.problems[pid] || {};
    const accepted = result.status === 'Accepted';
    p.attempts = (p.attempts || 0) + 1; p.last_status = result.status; p.last_at = nowIso();
    if (accepted) {
      const level = p.level || 0; const iv = INTERVALS();
      p.level = level + 1; p.status = 'solved'; p.solved_at = p.solved_at || today();
      p.next_review = plusDays(iv[Math.min(level, iv.length - 1)]); p.accepted_code = code;
    } else if (p.status === 'solved') { p.level = Math.max(0, (p.level || 1) - 1); p.next_review = plusDays(1); }
    else p.status = 'attempted';
    p.draft = code;
    data.submissions.push({ id: pid, status: result.status, passed: result.passed, total: result.total, ms: result.ms, at: p.last_at, code });
    data.submissions = data.submissions.slice(-500);
    saveProgress(data);
    return p;
  }
  function rateReview(pid, rating) {
    const data = loadProgress(); const p = data.problems[pid] = data.problems[pid] || {}; const iv = INTERVALS();
    let level = p.level || 0;
    if (rating === 'again') level = 0; else if (rating === 'hard') level = Math.max(0, level - 1); else if (rating === 'easy') level += 1;
    p.level = level; p.next_review = plusDays(iv[Math.min(level, iv.length - 1)]); saveProgress(data); return p;
  }
  function stats(problems) {
    const data = loadProgress(); const prog = data.problems;
    const by_difficulty = { Easy: [0, 0], Medium: [0, 0], Hard: [0, 0] }; const by_pattern = {};
    let solved = 0, attempted = 0;
    for (const p of problems) {
      const e = prog[p.id] || {}; by_difficulty[p.difficulty][1]++; (by_pattern[p.pattern] = by_pattern[p.pattern] || [0, 0])[1]++;
      if (e.status === 'solved') { solved++; by_difficulty[p.difficulty][0]++; by_pattern[p.pattern][0]++; } else if (e.status === 'attempted') attempted++;
    }
    const days = new Set(data.submissions.filter(s => s.status === 'Accepted').map(s => s.at.slice(0, 10)));
    let streak = 0; const d = new Date(); if (!days.has(d.toISOString().slice(0, 10))) d.setDate(d.getDate() - 1);
    while (days.has(d.toISOString().slice(0, 10))) { streak++; d.setDate(d.getDate() - 1); }
    return { solved, attempted, total: problems.length, by_difficulty, by_pattern, streak, active_days: [...days].sort().slice(-120) };
  }
  function dueReviews(problems) {
    const prog = loadProgress().problems; const t = today();
    return problems.filter(p => { const e = prog[p.id]; return e && e.status === 'solved' && (e.next_review || '9999') <= t; })
      .map(p => ({ id: p.id, title: p.title, difficulty: p.difficulty, pattern: p.pattern, due: prog[p.id].next_review })).sort((a, b) => a.due < b.due ? -1 : 1);
  }

  // ---------- tracks and plan ----------
  const DIFF = { Easy: 0, Medium: 1, Hard: 2 };
  function companyTrack(problems, company) {
    const g = tracksData.guides[company]; const byId = Object.fromEntries(problems.map(p => [p.id, p]));
    const must = g.must_do.map(i => byId[i]).filter(Boolean); const mustIds = new Set(must.map(p => p.id));
    const sc = (p) => (p.companies || {})[company] || 0;
    const rest = problems.filter(p => sc(p) >= 3 && !mustIds.has(p.id)).sort((a, b) => sc(b) - sc(a) || DIFF[a.difficulty] - DIFF[b.difficulty] || a.number - b.number);
    const freq = problems.filter(p => sc(p) >= 1).sort((a, b) => sc(b) - sc(a) || a.number - b.number);
    const prog = loadProgress().problems;
    const brief = (p) => ({ id: p.id, number: p.number, title: p.title, difficulty: p.difficulty, pattern: p.pattern, score: sc(p), status: (prog[p.id] || {}).status });
    const weight = {}; for (const p of freq) weight[p.pattern] = (weight[p.pattern] || 0) + sc(p);
    const total = Object.values(weight).reduce((a, b) => a + b, 0) || 1;
    const pattern_mix = Object.entries(weight).map(([pattern, v]) => ({ pattern, share: Math.round(100 * v / total) })).sort((a, b) => b.share - a.share);
    return { company, name: g.name, summary: g.summary, process: g.process, focus: g.focus, tips: g.tips, must_do: must.map(brief), also: rest.map(brief), all_by_frequency: freq.map(brief), pattern_mix };
  }
  function studyPlan(problems) {
    const prog = loadProgress().problems;
    const weeks = tracksData.weeks.map(([title, patterns], wi) => {
      const week = wi + 1;
      const pool = problems.filter(p => patterns.includes(p.pattern)).sort((a, b) => patterns.indexOf(a.pattern) - patterns.indexOf(b.pattern) || DIFF[a.difficulty] - DIFF[b.difficulty] || a.number - b.number);
      const days = [[], [], [], [], [], []];
      pool.forEach((p, i) => days[i % 6].push({ id: p.id, number: p.number, title: p.title, difficulty: p.difficulty, pattern: p.pattern, status: (prog[p.id] || {}).status }));
      const extras = week === 8 ? ['Two full mock interviews (use the Mock tab): one Google-style, one Apple-style.', "Re-solve every problem marked 'again' or 'hard' in reviews.", 'Write out your 6 behavioural STAR stories and rehearse them aloud.'] : week === 5 ? ['Mid-point mock interview: one graph problem, 45 minutes, no hints.'] : [];
      return { week, title, patterns, days, extras, done: days.flat().filter(p => p.status === 'solved').length, total: pool.length };
    });
    return { weeks, daily_routine: ['Warm-up (10 min): one review-due problem from the Reviews list, from memory.', 'New problems (60-90 min): the day\'s list. Spend at most 25 minutes before opening a hint, 40 before the editorial.', 'After each problem: read the editorial even if you passed, and write one line in Notes about the key idea.', 'Wrap-up (5 min): re-explain today\'s hardest problem out loud as if to an interviewer.'] };
  }

  // ---------- judge ----------
  let worker = null, seq = 0; const pending = {};
  function getWorker() {
    if (!worker) {
      worker = new Worker('judge-worker.js');
      worker.onmessage = (ev) => { const cb = pending[ev.data.id]; if (cb) { delete pending[ev.data.id]; cb(ev.data); } };
      worker.onerror = (e) => { for (const k of Object.keys(pending)) { pending[k]({ fatal: 'Worker error: ' + e.message }); delete pending[k]; } };
    }
    return worker;
  }
  function execute(code, problem, tests) {
    return new Promise((resolve) => {
      const id = ++seq; const w = getWorker();
      const timer = setTimeout(() => { delete pending[id]; w.terminate(); worker = null; resolve({ timeout: true }); }, TIMEOUT_MS + (seq === 1 ? 30000 : 0));
      pending[id] = (msg) => { clearTimeout(timer); resolve(msg); };
      w.postMessage({ id, code, tests, spec: { kind: problem.kind || 'function', function: problem.function, class_name: problem.class_name, arg_types: problem.arg_types || {}, return_type: problem.return_type || '', output_mode: problem.output_mode || 'return' } });
    });
  }
  const norm = (v, mode) => mode === 'unordered_nested' ? (v || []).map(x => JSON.stringify(Array.isArray(x) ? [...x].sort((a, b) => a < b ? -1 : a > b ? 1 : 0) : x)).sort() : (v || []).map(x => JSON.stringify(x)).sort();
  function compare(expected, actual, mode, tol) {
    tol = tol || 1e-5;
    if (mode === 'any_of') return expected.some(e => compare(e, actual, 'exact', tol));
    if (mode === 'float') {
      const close = (a, b) => {
        if (Array.isArray(a) || Array.isArray(b)) return Array.isArray(a) && Array.isArray(b) && a.length === b.length && a.every((x, i) => close(x, b[i]));
        if (a && typeof a === 'object' || b && typeof b === 'object') { if (!a || !b || typeof a !== 'object' || typeof b !== 'object') return false; const ka = Object.keys(a).sort(), kb = Object.keys(b).sort(); return ka.join() === kb.join() && ka.every(k => close(a[k], b[k])); }
        if (typeof a === 'boolean' || typeof a === 'string' || a === null || typeof b === 'boolean' || typeof b === 'string' || b === null) return a === b;
        const x = +a, y = +b; return Number.isFinite(x) && Number.isFinite(y) && Math.abs(x - y) <= tol;
      };
      return close(expected, actual);
    }
    if (mode === 'unordered' || mode === 'unordered_nested') { const a = norm(expected, mode), b = norm(actual, mode); return a.length === b.length && a.every((x, i) => x === b[i]); }
    return JSON.stringify(expected) === JSON.stringify(actual);
  }
  async function runCode(code, problem, tests) {
    const t0 = performance.now();
    const msg = await execute(code, problem, tests);
    const ms = Math.round(performance.now() - t0);
    if (msg.timeout) return { status: 'Time Limit Exceeded', passed: 0, total: tests.length, cases: [], stderr: 'Execution exceeded ' + (TIMEOUT_MS / 1000) + 's. Check for an infinite loop or an exponential algorithm.', ms };
    if (msg.fatal) return { status: 'Runtime Error', passed: 0, total: tests.length, cases: [], stderr: msg.fatal, ms };
    if (msg.error) return { status: msg.error.includes('SyntaxError') || msg.error.includes('IndentationError') ? 'Compile Error' : 'Runtime Error', passed: 0, total: tests.length, cases: [], stderr: msg.error, stdout: msg.stdout, ms };
    const mode = problem.compare || 'exact'; const cases = []; let passed = 0, status = 'Accepted';
    tests.forEach((t, i) => {
      const r = msg.results[i] || {};
      if (r.ok) { const ok = compare(t.output, r.output, mode, problem.tolerance); passed += ok; cases.push({ input: t.input, expected: t.output, output: r.output, ok, ms: r.ms }); if (!ok && status === 'Accepted') status = 'Wrong Answer'; }
      else { cases.push({ input: t.input, expected: t.output, output: null, ok: false, error: r.error, trace: r.trace }); status = 'Runtime Error'; }
    });
    return { status, passed, total: tests.length, cases, stdout: msg.stdout, ms };
  }
  const visibleTests = (p) => p.tests.slice(0, Math.max(2, Math.min(3, p.examples.length)));

  // ---------- API ----------
  function summary(p, prog) { const e = prog[p.id] || {}; return { ...p, status: e.status, starred: !!e.starred, next_review: e.next_review, attempts: e.attempts || 0 }; }
  async function problemPayload(id) {
    const idx = await loadIndex(); const p = await loadProblem(id); const e = loadProgress().problems[id] || {};
    const byId = Object.fromEntries(idx.problems.map(x => [x.id, x])); const i = p.number - 1;
    const prev = idx.problems[i - 1], next = idx.problems[i + 1];
    const subs = loadProgress().submissions.filter(s => s.id === id).reverse().slice(0, 20);
    return { ...p, similar: (p.similar || []).filter(s => byId[s]).map(s => ({ id: s, title: byId[s].title, difficulty: byId[s].difficulty })), followups: p.followups || [], kind: p.kind || 'function',
      draft: e.draft, note: e.note || '', starred: !!e.starred, status: e.status, level: e.level || 0, next_review: e.next_review,
      visible_tests: visibleTests(p), hidden_count: p.tests.length - visibleTests(p).length, prev: prev ? { id: prev.id, title: prev.title } : null, next: next ? { id: next.id, title: next.title } : null, submissions: subs };
  }

  window.PrepAPI = {
    async get(url) {
      const [path, qs] = url.split('?'); const idx = await loadIndex(); const prog = loadProgress().problems;
      if (path === '/api/problems') return { problems: idx.problems.map(p => summary(p, prog)), patterns: idx.patterns };
      if (path.startsWith('/api/problem/')) return problemPayload(path.split('/')[3]);
      if (path === '/api/stats') return { stats: stats(idx.problems), reviews: dueReviews(idx.problems) };
      if (path === '/api/random') { const un = idx.problems.filter(p => (prog[p.id] || {}).status !== 'solved'); const pool = un.length ? un : idx.problems; return { id: pool[Math.floor(Math.random() * pool.length)].id }; }
      if (path.startsWith('/api/track/')) return companyTrack(idx.problems, path.split('/')[3]);
      if (path === '/api/plan') return studyPlan(idx.problems);
      if (path === '/api/patterns') return patternsData;
      if (path === '/api/apple-mle') {
        const byId = Object.fromEntries(idx.problems.map(p => [p.id, p]));
        const plan = mleData.plan.map(w => ({ ...w, problems: w.problems.filter(i => byId[i]).map(i => ({ id: i, title: byId[i].title, difficulty: byId[i].difficulty, pattern: byId[i].pattern, status: (prog[i] || {}).status })) }));
        return { ...mleData, plan, coding: idx.problems.filter(p => p.pattern === 'ML Coding').map(p => summary(p, prog)) };
      }
      if (path === '/api/mock') { const company = (qs || '').replace('company=', '') || 'google';
        if (company === 'apple-mle') { const src = idx.problems.filter(p => p.pattern === 'ML Coding').map(p => ({ id: p.id, number: p.number, title: p.title, difficulty: p.difficulty, pattern: p.pattern })); const pick = []; while (pick.length < 2 && src.length) pick.push(src.splice(Math.floor(Math.random() * src.length), 1)[0]); return { company, problems: pick, minutes: 45 }; } const t = companyTrack(idx.problems, company); const pool = [...t.must_do, ...t.also].filter(p => p.difficulty !== 'Easy'); const pick = []; const src = pool.length ? [...pool] : [...t.all_by_frequency]; while (pick.length < 2 && src.length) pick.push(src.splice(Math.floor(Math.random() * src.length), 1)[0]); return { company, problems: pick, minutes: 45 }; }
      return { error: 'unknown endpoint' };
    },
    async post(url, body) {
      const pid = body.id;
      if (url === '/api/run' || url === '/api/submit') {
        const p = await loadProblem(pid); const code = body.code || '';
        if (url === '/api/run') {
          let tests = visibleTests(p); if (body.custom) tests = tests.concat(body.custom.map(c => ({ input: c, output: null })));
          const res = await runCode(code, p, tests); this.post('/api/draft', { id: pid, code });
          for (const c of res.cases) if (c.expected === null) { c.ok = !c.error; c.custom = true; }
          const graded = res.cases.filter(c => !c.custom);
          if (res.cases.length) { if (res.status === 'Wrong Answer' || res.status === 'Accepted') res.status = graded.every(c => c.ok) ? 'Accepted' : 'Wrong Answer'; res.passed = graded.filter(c => c.ok).length; res.total = graded.length; }
          return res;
        }
        const res = await runCode(code, p, p.tests); const entry = recordSubmission(pid, code, res);
        res.entry = { status: entry.status, level: entry.level, next_review: entry.next_review, attempts: entry.attempts }; return res;
      }
      const data = loadProgress(); const e = data.problems[pid] = data.problems[pid] || {};
      if (url === '/api/draft') { e.draft = body.code; e.draft_at = nowIso(); saveProgress(data); return { ok: true }; }
      if (url === '/api/note') { e.note = body.note; saveProgress(data); return { ok: true }; }
      if (url === '/api/star') { e.starred = !e.starred; saveProgress(data); return { starred: e.starred }; }
      if (url === '/api/rate') return rateReview(pid, body.rating || 'hard');
      return { error: 'unknown endpoint' };
    },
    warm() { try { getWorker(); } catch {} },
  };
})();
