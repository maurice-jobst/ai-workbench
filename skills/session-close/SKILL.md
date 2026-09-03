---
name: session-close
description: Close a work session in a file-first AI workbench. Captures decisions and learnings, rewrites the desk file, runs scripts/check, commits on a branch and opens a pull request. Use at the end of every session, and whenever git status shows work that would otherwise be lost.
---

# Session close

A session that ends without capturing what it learned is unfinished. Walk every step;
each item is either done or named in the hand-over.

## 1. Capture

1. **Decisions.** Anything settled this session that changes how work is done goes
   into `DECISIONS.md` (or the log `AGENTS.md` names): what, why, how to apply. A
   decision that closes an issue cites its number.
2. **Learnings.** A gotcha that cost more than fifteen minutes becomes either a rule in
   `AGENTS.md` (only if it changes behaviour, one line) or a note where `AGENTS.md`
   says learnings live. Never a dated diary entry.
3. **Documents touched.** Every document whose subject changed this session is
   updated now, not next time. A doc that states how something works is a claim.

## 2. Rewrite the desk

Rewrite `STATUS.md` (or the desk file `AGENTS.md` names) from scratch: what is true
now, what is in flight and where, who owes what, the dates that matter, the open
questions. Delete finished and struck-through items; git keeps the history. Anything
longer than two lines moves to its own document with a link from the desk. Stay under
120 lines.

## 3. Check

Run `scripts/check`. Fix every finding it reports before committing; if a finding
cannot be fixed this session, say so in the hand-over rather than committing around
it. `check: clean` is the exit condition.

## 4. Commit on a branch

Never commit on `main`. If the session is still on `main`, cut a branch named for the
issue or the track first. Commit everything, work in progress included; the message
names the track and references the issue (`Refs #N`). Half-done work is committed as
WIP, never left dangling in the working tree.

## 5. Push and open a pull request

Push the branch and open a pull request against `main` that references the issue.
The body states what changed and what is still open. The maintainer merges; the
session does not.

## 6. Hand over

Close with a short list: what landed (branch, PR), what was parked, what the next
session should pick up first, and every item this session could not handle. No silent
drops.
