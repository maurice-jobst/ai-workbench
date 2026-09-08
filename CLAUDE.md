@AGENTS.md

Everything under `templates/` and `skills/` ships verbatim into other people's repos:
keep it generic, with no author-specific hosts, paths or tooling.
Run `scripts/check` before every commit; it is the whole CI and the pre-commit hook.

## Governance (estate-wide, identical in every core repo — source: dotfiles/private_dot_claude/CLAUDE.md, 2026-09-08)

- Gitea is canonical; `bot` works branch → PR, never pushes `main`, never force-pushes.
- Merge licence: `bot` merges ≤ 400 changed lines and ≤ 10 files in auto mode. Doctrine, new
  write paths, the gate, host-deleting changes and anything larger merge only on Maurice's
  word: an approving Gitea review, or an explicit go on the issue/in chat that the PR cites.
- Models: Sonnet for daily sessions, Opus for planning and reviews, Fable for structural change.
- Channel or host writes run only on Maurice's explicit command; the 1Password prompt (or
  `./deploy.sh`) is the gate, never the agent's initiative.
- 14-day rule: an untouched open issue closes as `abandoned` at session close, unless
  `blocked` with a due date, `decision`, or dated in the title.
- 1.0 bar: README, AGENTS/CLAUDE, STATUS, session-open/close, `scripts/check` green, tests where
  scripts carry load, backlog only future-dated — declared by tag `v1.0.0` + CHANGELOG + STATUS.
