# How the LeetCode problem page works, per REA

Method: a disposable headless Chrome was started with `--remote-debugging-port=9222` and
pointed at public leetcode.com pages. REA 6.8.0 (built from the cloned `morluto/rea` repo)
attached over the Chrome DevTools Protocol with `rea inspect-web-page`, `rea analyze-web-bundle`
and `rea capture-web-screenshot`. REA is passive: it reads DOM, accessibility tree, scripts,
storage key names and network metadata, and never executes site code.

Only the public problem page (`/problems/two-sum/description/`) completed loading. The problem
set, explore, contest, discuss and study-plan pages stayed on a Cloudflare interstitial, and no
attempt was made to get past it. No logged-in or Premium content was requested or observed.

Evidence files: `rea-evidence-summary.json` (trimmed), `leetcode-problem-page.png` (REA screenshot).

## Stack

- Next.js with React (high-confidence vendor fingerprints across 109 scripts). Pages render as a
  client-side SPA; route candidates in the bundle include `/problemset`, `/contest`, `/store`,
  `/help-center/`.
- Persistence on the client: `localStorage` keys `EDITOR_SETTING`, `QD_LAYOUT_JSON`,
  `QD_DISABLED_QUEST_SPOILER_ALERT`; `sessionStorage` key `new-query-filter`; an IndexedDB named
  `LeetCode-problems`. So editor preferences, panel layout and a local problem cache live in the
  browser, not the server.
- Bundle string literals hint at the data model without any API call being made: `questionInfo`,
  `langInfo`, `codeAction`, `difficulty`, `status`, `premiumOnly`, `favoriteSlug`, `csrftoken`.
- Sentry tracing headers (`sentry-trace`, `baggage`, `traceparent`) and a `next-router-prefetch`
  header are present in the bundle.

## Feature inventory of the problem page (from the accessibility tree, 1840 nodes)

| Area | Observed controls | Replica |
|---|---|---|
| Top bar | Problem List, prev/next question, "Pick one" random, Layouts, Settings, Stopwatch, Note, Run, Submit | List button, ‹ › navigation, random (⤭), stopwatch, Notes tab, Run, Submit |
| Left panel tabs | Description, Editorial, Solutions, Submissions | Description, Editorial, Submissions, Notes |
| Description | Title "1. Two Sum", difficulty pill, Topics (Array, Hash Table), Companies (Premium-gated), Hint, examples with Input/Output/Explanation, constraints, like/dislike counts | Same layout: difficulty, pattern, company chips (own estimate), progressive hints, examples, constraints, topics |
| Similar questions | 3Sum, 4Sum, Two Sum II, ... links | `similar` ids rendered as links |
| Discussion | comment textbox, sort by Best, pagination 1..221 | Replaced by a per-problem Notes tab (single user) |
| Editor | language picker (C++ default), Auto (format), `textbox: Code editor`, Saved indicator, "Upgrade to Cloud Saving" | Python 3 only, CodeMirror, draft auto-save with Saved indicator |
| Console | Testcase tab with Case 1/2/3, Test Result tab, "You need to log in / sign up to run or submit" | Case tabs plus Custom, Test result with per-case output/expected, verdicts: Accepted, Wrong Answer, Runtime Error, Time Limit Exceeded |
| Account | Register, Log in, Premium | None: single local user, progress in `data/progress.json` |

## What Premium adds, and what the replica does instead

Premium gates company tags and frequency, locked problems, official editorials, and the debugger.
Those are paid data and were not touched. The replica covers the same needs with content written
from scratch:

- Editorials: every problem has an `approach` with the key insight, algorithm, pitfalls and follow-ups.
- Company signal: a `companies` score per problem, estimated from public interview reports, plus
  curated Google and Apple tracks with process notes and must-do lists.
- Study plan: an 8-week schedule generated from the bank.
- Spaced repetition and mock interviews, which Premium does not have.
