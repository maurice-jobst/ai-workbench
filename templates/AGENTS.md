# AGENTS.md — <project>

## Purpose

<Two to four lines: what this repo is, who works in it, what it produces. State the one
thing an agent would get wrong without being told.>

## Rules

1. **Markdown is the state.** Plans, decisions, status and learnings live here as versioned
   markdown. No second tracker; nothing that matters stays in a chat transcript.
2. **AI at the edges, deterministic core.** The agent drafts, triages, summarizes.
   Anything that must be reproducible is a script under `scripts/`.
3. **The desk file is rewritten, never appended.** `STATUS.md` states what is true now
   and who owes what. Anything longer than two lines moves to its own document, and the
   desk carries the link.
4. **A decision that changes behaviour gets an entry in `DECISIONS.md`** with its why.
   A lesson that cost more than fifteen minutes becomes a rule here or a note there.
5. **No silent drops.** Anything unhandled, out of scope or uncertain is surfaced at
   session close, in the desk file or the hand-over.
6. **Caps.** This file stays under 100 lines and `STATUS.md` under 120. The lint
   enforces both; overflow moves to a linked document.
7. <Domain rules that would otherwise cause a real mistake, one line each. Earned by
   mistakes, not guessed at setup.>

## Layout

- `STATUS.md` — the desk file, read at every session open.
- `DECISIONS.md` — append-only decision log.
- `scripts/` — `check` (the whole CI) and `workbench_lint.py`.
- `.claude/skills/` — `session-open`, `session-close`.
- <Only the non-obvious folders. Never a file-by-file tour.>

## Commands

- `scripts/check` — lint plus tests; must pass before every push. Read-only.
- `python3 scripts/workbench_lint.py` — caps and links alone. Read-only.
- <The few commands that matter, one line each; mark writes and anything that costs
  money.>

## Working here

Open with `session-open`: read the log, the desk, the check and the tracker; brief;
propose one next step. Close with `session-close`: capture decisions and learnings, rewrite
`STATUS.md`, run `scripts/check`, commit on a branch, open a pull request that references
its issue. Issues are the only backlog (labels: bug, task, decision, blocked). Activate
the hook once per clone with `git config core.hooksPath .githooks`.

## Context

<Business or domain facts an agent cannot derive from the tree: people, cadence, systems
of record, what must never leave this repo. Under ten lines.>
