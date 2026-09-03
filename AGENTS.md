# AGENTS.md — ai-workbench

## Purpose

The public reference for the file-first AI workbench pattern: markdown as state,
deterministic scripts, a session loop with an open and a close, and one `scripts/check`.
This repo holds the template, the lint, the scaffold and the two session skills that
anyone can copy. Nothing here depends on any other repository.

## Rules

1. Public repo. No private hostnames, LAN addresses, credentials, personal paths or
   references to any specific deployment — in code, docs, comments or commit messages.
2. Standard library only. The lint and the tests run on a bare `python3` (3.10+); the
   check script and the hook are plain bash. No package manager, no third-party tools.
3. `templates/` and `skills/` must be copyable verbatim into a downstream repo. They may
   name each other by their downstream paths; they never assume this repo's layout.
4. `AGENTS.md` is capped at 100 lines and the desk file at 120, here and in every copy.
   The lint enforces it; overflow moves to a linked document, not to a bigger cap.
5. Pattern text carries no history: no dates of past decisions, no changelog prose, no
   version metadata in skills. Git history is the changelog.
6. Tests use `unittest`, live in `tests/`, and cover the lint's observable behaviour
   (findings, exit codes, flags). No tests for glue.
7. The lint may only ever report on files; it never edits, formats or deletes anything.

## Layout

- `templates/` — the downstream shape: `CLAUDE.md`, `AGENTS.md`, `STATUS.md`,
  `DECISIONS.md`. The scaffold fills the placeholders.
- `skills/` — `session-open`, `session-close` (copied into a downstream
  `.claude/skills/`) and `workbench-scaffold` (installed globally; it needs a clone of
  this repo to copy from).
- `scripts/` — `workbench_lint.py` and `check`; both are copied downstream unchanged.
- `.githooks/pre-commit` — runs `scripts/check`; also copied downstream unchanged.
- `tests/` — the lint's unit tests. `docs/why.md` — the assumptions and evidence.

## Commands

- `scripts/check` — lint plus tests; the whole CI. Read-only.
- `python3 scripts/workbench_lint.py --help` — the lint's flags. Read-only.
- `python3 -m unittest discover -s tests -v` — tests alone. Read-only.

## Working here

Cut a branch, keep the commit small, run `scripts/check`, push, open a pull request that
references its issue. The maintainer merges. Issues are the only backlog (labels: bug,
task, decision, blocked). Activate the hook once per clone with
`git config core.hooksPath .githooks`. This repo is the pattern's source, not a
workbench: it has no desk file and does not run the session loop on itself.
