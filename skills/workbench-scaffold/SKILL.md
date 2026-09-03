---
name: workbench-scaffold
description: Lay out a file-first AI workbench in the current folder from a clone of the ai-workbench repo, bring an existing repo up to the pattern, or audit a workbench for drift between its copied files and the source. Use before session-open in a repo that has no AGENTS.md, and to check a workbench that may have fallen behind the source.
---

# Workbench scaffold

Turn a folder into a workbench: the operating agreement, the desk file, the lint, the
check, the hook and the two session skills. This skill is installed globally because it
runs in folders that hold nothing yet.

## 1. Resolve the source

First hit wins:

1. `$WORKBENCH_HOME`, if it contains `templates/AGENTS.md` and `scripts/workbench_lint.py`.
2. This skill's own directory, walked upward until a directory holds both.
3. Neither: stop, say the ai-workbench clone is missing, and name both options as the fix.

## 2. Pick the mode

Take the first case that fits and say which, and why, before touching anything:

- `scripts/workbench_lint.py` exists → **audit**.
- `AGENTS.md` exists, or the folder has content → **adopt**.
- Otherwise → **fresh**.

**Audit.** Compare the repo against the source and report, in this order:

1. Drift in every copied file, using `cmp` and `diff -u` against the source:
   `scripts/workbench_lint.py`, `scripts/check`, `.githooks/pre-commit`,
   `.claude/skills/session-open/SKILL.md`, `.claude/skills/session-close/SKILL.md`.
   Offer to re-copy each drifted file; offer nothing else for it. Local changes to
   these files are the drift, not a customisation.
2. `scripts/check` output; every finding is an audit item.
3. `AGENTS.md` sections missing against `templates/AGENTS.md`, and any placeholder
   (`<...>`) still unfilled.
4. Whether `git config core.hooksPath` prints `.githooks`.

Offer each fix separately and change nothing without a yes.

**Adopt.** Report what already exists. Ask only what the missing pieces need, reading
answers off the repo wherever it already states them. Write only what is missing.
Never overwrite an existing file.

**Fresh.** Interview, then write.

## 3. Interview

One question at a time, and only these:

1. Project name.
2. Purpose, in two to four lines: what the repo is and produces, and the one thing an
   agent would get wrong without being told.
3. The tracker, if any: where issues live. This becomes a line under `## Context`.
4. Which existing folders are non-obvious enough to earn a line under `## Layout`.
5. The commands that matter, and which of them write or cost money.

Leave the domain rules placeholder empty. Rules get earned by mistakes.

## 4. Write

If the folder is not a git repository yet, run `git init` first.

| Target | Source and treatment |
|---|---|
| `AGENTS.md` | `templates/AGENTS.md`, placeholders filled from the interview, unfilled placeholders deleted. Must stay under 100 lines. |
| `CLAUDE.md` | `templates/CLAUDE.md`, verbatim. A real file, never a symlink. |
| `STATUS.md` | `templates/STATUS.md`, project name filled, everything else left as the empty shape. |
| `DECISIONS.md` | `templates/DECISIONS.md`, project name filled, example entry kept as the format reference. |
| `scripts/workbench_lint.py` | Copied with `cp`, never retyped or edited. |
| `scripts/check` | Copied with `cp`, executable. |
| `.githooks/pre-commit` | Copied with `cp`, executable. |
| `.claude/skills/session-open/SKILL.md` | Copied with `cp`. |
| `.claude/skills/session-close/SKILL.md` | Copied with `cp`. |
| `.gitignore` | Ensure it lists `__pycache__/`, `.DS_Store`, `.claude/settings.local.json`, `.claude/worktrees/`. |

Create no other folders. Git does not hold empty directories, and the layout section
documents what appears on first use.

## 5. Prove it and commit

Run `git config core.hooksPath .githooks`, then `scripts/check`. Show the output and
confirm it ends in `check: clean`. Commit the written files on a branch with a message
naming the scaffold. Close by naming `session-open` as the command for the next session.
