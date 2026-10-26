"""Build the static, serverless KaizenPrep into static-build/.

    python3 build_static.py /path/to/pyodide/package

Produces:
  static-build/index.html      page fragment for publishing as a Claude artifact (no doctype/html/body)
  static-build/local.html      the same page wrapped for local testing (python3 -m http.server)
  static-build/judge-worker.js, pyodide runtime files, data/
"""
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "static-build")
STATIC = os.path.join(HERE, "static")
PYODIDE_FILES = ["pyodide.js", "pyodide.asm.js", "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json"]

subprocess.run([sys.executable, os.path.join(HERE, "export_static.py")], check=True)

css = open(os.path.join(STATIC, "style.css"), encoding="utf-8").read()
# theme contract: dark values also under prefers-color-scheme, and color-scheme on both dark blocks
dark_block = re.search(r":root\[data-theme=\"dark\"\] \{(.*?)\}", css, re.S).group(1)
css = css.replace(':root[data-theme="dark"] {' + dark_block + '}',
                  '@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {' + dark_block + ' color-scheme: dark; } }\n'
                  ':root[data-theme="dark"] {' + dark_block + ' color-scheme: dark; }')
css = css.replace(".page { max-width: 1100px; margin: 0 auto; padding: 24px 16px 60px; }",
                  ".page { max-width: 1100px; margin: 0 auto; padding-block: 24px 60px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }")
css = css.replace("#topbar { height: 48px; display: flex; align-items: center; gap: 8px; padding: 0 16px;",
                  "#topbar { height: 48px; display: flex; align-items: center; gap: 8px; padding-block: 0; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));")
css += "\nhtml, body { height: 100%; }\n.pane-body, .page { min-width: 0; }\n"

index_html = open(os.path.join(STATIC, "index.html"), encoding="utf-8").read()
body = re.search(r"<body>(.*?)<script", index_html, re.S).group(1).strip()
local_api = open(os.path.join(STATIC, "local-api.js"), encoding="utf-8").read()
app_js = open(os.path.join(STATIC, "app.js"), encoding="utf-8").read()

CM = "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/"
cm_css = subprocess.run(["curl", "-sL", CM + "codemirror.min.css"], capture_output=True, text=True, check=True).stdout
cm_theme = subprocess.run(["curl", "-sL", CM + "theme/material-darker.min.css"], capture_output=True, text=True, check=True).stdout

fragment = f"""<title>KaizenPrep</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: LeetCode-style two-pane workspace; dashboard, list, plan and tracks as single-column pages. */
{cm_css}
{cm_theme}
{css}
</style>
{body}
<script src="{CM}codemirror.min.js"></script>
<script src="{CM}mode/python/python.min.js"></script>
<script src="{CM}addon/edit/matchbrackets.min.js"></script>
<script src="{CM}addon/edit/closebrackets.min.js"></script>
<script>
{local_api}
</script>
<script>
{app_js}
</script>
"""
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(fragment)
open(os.path.join(OUT, "local.html"), "w", encoding="utf-8").write(
    '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
    "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui}[hidden]{display:none!important}</style>"
    "</head><body>\n" + fragment + "\n</body></html>\n")
shutil.copy(os.path.join(STATIC, "judge-worker.js"), OUT)

if len(sys.argv) > 1:
    src = sys.argv[1]
    for f in PYODIDE_FILES:
        # the stdlib archive is served under a .wasm name because artifact hosting has no zip type
        dest = "python_stdlib.wasm" if f == "python_stdlib.zip" else f
        shutil.copy(os.path.join(src, f), os.path.join(OUT, dest))
    print("copied pyodide runtime from", src)
sizes = {f: os.path.getsize(os.path.join(OUT, f)) // 1024 for f in os.listdir(OUT) if os.path.isfile(os.path.join(OUT, f))}
print({k: f"{v} KB" for k, v in sorted(sizes.items())})
