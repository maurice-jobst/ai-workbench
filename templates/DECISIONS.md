# DECISIONS.md — <project>

One-line gist: append-only log of decisions that shape this repo and its work; newest at
the bottom; a superseded decision gets a new entry that points back, never an edit.

<!--
Format:
- One H2 per decision: date and title.
- Body: what was decided, in past tense, with enough context to stand alone.
- "Why:" one short paragraph.
- "How to apply:" the behavioural consequence, one short paragraph.
- A decision that closes an issue cites the issue number.
-->

## YYYY-MM-DD — Example: the desk file is rewritten, not appended

`STATUS.md` is rewritten at every session close and states only what is true now.

**Why:** an appended status file grows past the cap within weeks and buries the current
state under history that git already keeps.

**How to apply:** delete struck-through items instead of carrying them; move anything
longer than two lines to its own document and link it from the desk.
