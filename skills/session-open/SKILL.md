---
name: session-open
description: Open a work session in a file-first AI workbench. Orients from git log, the desk file, scripts/check and the tracker, then briefs what matters now and proposes exactly one next step. Use at the start of every session in a repo whose AGENTS.md describes the session loop.
---

# Session open

Orient, brief, propose one thing. Do not start work until the operator picks.

## 1. Preflight

Run `git rev-parse --show-toplevel` and read `AGENTS.md` there. Stop and name
`workbench-scaffold` as the fix if any of these holds:

- the folder is not a git repository
- `AGENTS.md` is missing
- `AGENTS.md` has no `## Working here` section describing an open and a close

Never substitute a default protocol for a missing one.

## 2. Orient

Read, in this order, and keep the output for the brief:

1. `git log --oneline -n 20 --date=short` and `git status --porcelain`.
2. The desk file: `STATUS.md`, or the file `AGENTS.md` names instead.
3. `scripts/check` (fall back to `python3 scripts/workbench_lint.py` when there is
   no check script). Findings go into the brief; do not fix them yet.
4. The tracker, if `AGENTS.md` names one: open issues, newest first, and anything
   assigned or labelled blocked.
5. Every command listed under `## Commands` that is marked read-only.

If `git log --since="<most recent Monday> 00:00" --oneline` is empty this is the
week's first session: read the full desk file and the last week of the decision log
instead of skimming. Keep the explicit `00:00`; a bare date anchors to the current
time of day.

## 3. Brief

One short block, each category omitted when empty:

1. check findings (a cap or a broken link first)
2. uncommitted work found by `git status`
3. dates from the desk file that turned urgent
4. contradictions between the tracker, the log and the desk file
5. stalled waiting-on items

Headline what fits. On a fat day, review beats completeness: name what was parked.

## 4. Propose one step

End with exactly one proposal: the single piece of work this session should do, with
the issue it belongs to and the branch name it will use. Then wait. The operator picks;
the session does not start work on its own.
