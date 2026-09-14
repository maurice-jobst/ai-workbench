# STATUS — ai-workbench desk

Rewritten at every session close, never appended. Last rewrite: 2026-09-14 (Fable 5.1, estate
structural session; the 1.0 round of Gitea issue #18).

## What is true now
- GitHub `maurice-jobst/ai-workbench` is the canonical remote; the Gitea mirror carries the backlog
  (issue #18 is the 1.0 checklist). `main` on GitHub is behind the local clone by one commit
  (the governance block in CLAUDE.md, 2026-09-08) — Maurice's push.
- The canonical `session-open` and `session-close` live in `skills/` and are copied verbatim
  into downstream repos (herald did so on 2026-09-14; lalebe, cubic, dotfiles, aurelius carry
  their own repo-specific versions from before the decision and adopt these on their next 1.0 pass).
- `docs/write-path.md` states the write-path order (decision function → self-checking
  generator → tests → probe → read-back → baseline note), generic, no repo names.
- `scripts/check` runs the lint and the lint's tests.

## In flight
- The branch for #18 (this desk, the write-path doc, the README row) — a pull request on
  GitHub; Maurice merges.

## Waiting on Maurice
- Push of `main` (the governance commit), then the #18 pull request.
- The code export (a generic `queue_apply` skeleton, `md2html.py`, `operator_page.py` with a
  config file): its own Fable session; Maurice reviews the diff for names, prices, hosts before
  the push.
- The tag `v1.0.0` + CHANGELOG, after the export.

## Next session
1. The code export (#18 item 3), Fable, with the port of the md2html and operator-page tests.
2. `workbench-scaffold` audit mode against the five repos that gained `## Working here` on
   2026-09-14 (dotfiles, herald, fiscus, dachwacht, fernwacht): report drift, change nothing.

## Pitfalls
- `bot` never merges here: GitHub is the remote, Maurice merges on GitHub.
- The lint caps: AGENTS.md 100 lines, STATUS.md 120 lines, gist lines on docs.
