/* Judge worker: loads Pyodide from the files published next to the page and runs one submission per message. */
let pyodide = null;
let harness = null;
const base = self.location.href.replace(/[^/]*$/, '');

async function boot() {
  importScripts(base + 'pyodide.js');
  pyodide = await loadPyodide({ indexURL: base, stdLibURL: base + 'python_stdlib.wasm' });
  const res = await fetch(base + 'data/harness.py');
  harness = await res.text();
}
const ready = boot();

self.onmessage = async (ev) => {
  const { id, code, spec, tests } = ev.data;
  try {
    await ready;
  } catch (e) {
    self.postMessage({ id, fatal: 'Python runtime failed to load: ' + (e && e.message ? e.message : e) });
    return;
  }
  const out = [];
  pyodide.setStdout({ batched: (s) => out.push(s) });
  pyodide.setStderr({ batched: (s) => out.push(s) });
  const ns = pyodide.globals.get('dict')();
  try {
    pyodide.runPython(harness + '\n# ---- user code ----\n' + code + '\n', { globals: ns });
    const payload = JSON.stringify({ spec, tests });
    ns.set('__payload__', payload);
    const resultJson = pyodide.runPython('_run_payload(__payload__)', { globals: ns });
    self.postMessage({ id, results: JSON.parse(resultJson), stdout: out.join('\n').slice(-2000) });
  } catch (e) {
    const msg = (e && e.message) ? e.message : String(e);
    self.postMessage({ id, error: msg.slice(-3000), stdout: out.join('\n').slice(-2000) });
  } finally {
    ns.destroy();
  }
};
