# KaizenPrep

An interview practice platform modelled on the public LeetCode problem page: 211 original
problems, an in-browser Python judge, editorials, spaced repetition, an 8-week plan, Google
and Apple tracks, and an Apple MLE section (study guide, 53-question bank with model answers,
ML system design prompts, 16 implement-from-scratch ML coding problems, 4-week plan).

**Live site:** https://ahmedsidi9.github.io/kaizenprep/ (static build, Python runs in your browser via Pyodide)

## Run the server version locally

Standard-library Python server, vanilla JS front end, no accounts.

```bash
python3 server.py          # then open http://127.0.0.1:8000
```

## What is inside

- **Problem bank** (`bank/*.py`): problems grouped by pattern, each with a description, examples,
  constraints, progressive hints, hidden tests, a reference solution, an editorial with interview
  follow-ups, complexity, and company-frequency estimates. All text is original.
- **Judge** (`judge.py`): runs your Python in an isolated subprocess with a 10-second limit, converts
  linked lists / trees / graphs from JSON, and reports Accepted, Wrong Answer, Runtime Error or
  Time Limit Exceeded per test case. `Run` uses the visible examples plus a custom input; `Submit`
  runs every hidden test.
- **Progress and spaced repetition** (`progress.py`, `data/progress.json`): drafts auto-save,
  submissions are kept, solved problems come back for review after 1, 3, 7, 14, 30 and 60 days,
  and you rate each review (again / hard / easy).
- **Study plan** (`tracks.py`): 8 weeks, 6 days a week, one pattern block per week.
- **Google and Apple tracks**: interview process, what each company emphasises, tips, a must-do
  list and the full bank ordered by estimated frequency.
- **Mock interview**: two problems from a company track with a 45-minute countdown in the top bar.

## Keyboard

- `Cmd/Ctrl + Enter` run, `Cmd/Ctrl + Shift + Enter` submit, `Tab` indents.

## Build the static site

```bash
npm pack pyodide@0.26.4 && tar xzf pyodide-0.26.4.tgz
python3 build_static.py ./package     # writes static-build/, served from the gh-pages branch
```

## Validating the bank

```bash
python3 validate.py            # every problem: schema + reference solution passes its tests
python3 validate.py graphs     # one module
```

## Adding a problem

Copy an entry from `bank/seed.py`, follow `SCHEMA.md`, run the validator. Design problems use
`kind: "design"` with an ops list; in-place problems use `output_mode: "arg:<param>"`.

## Where the design came from

`research/REA-FINDINGS.md` documents how the public LeetCode problem page is built, captured with
REA over the Chrome DevTools Protocol, and maps each observed feature to its counterpart here.
No Premium or logged-in content was accessed, and no problem text was copied.
