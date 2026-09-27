# AI Workbench

**A file-first pattern for working with an AI coding agent over many sessions: markdown as
state, deterministic scripts, a session loop with an open and a close, and one check that
tells you whether the repo is healthy.**

Built by [Maurice Jobst](https://github.com/maurice-jobst). MIT licensed, standard library
only, nothing to install beyond `git`, `bash` and `python3` 3.10 or newer.

## The problem

Every agent session starts from zero. You re-explain the project, the constraints and the
decision you made three sessions ago, and the agent still misses the connection. Chat
history is not memory; a repo is. Give the agent what you would give a new senior hire: one
place where everything lives, house rules, a desk with the current state, and checks that
catch drift before it costs you.

## The pattern

1. **Markdown is the state.** Plans, decisions, status and learnings live as versioned
   markdown in the repo. No second tracker, nothing trapped in a chat transcript.
2. **AI at the edges, deterministic core.** The agent drafts, triages and summarizes.
   Anything that must be reproducible — caps, link checks, tests — is a script.
3. **A session loop with an open and a close.** Open: read the log, the desk file, the
   check and the tracker; brief; propose one thing. Close: capture decisions and learnings,
   rewrite the desk, run the check, commit on a branch, open a pull request.
4. **A lint that enforces the caps and the links.** `AGENTS.md` stays under 100 lines and
   the desk file under 120, so the always-loaded layer stays small. Every wikilink and
   relative link resolves. Skill files carry a name that matches their folder and a
   description.
5. **One `scripts/check`.** Lint plus tests, exit non-zero on any finding, `check: clean`
   otherwise. The pre-commit hook runs it and nothing else.

The always-loaded layer is two files: `AGENTS.md`, the operating agreement, and
`STATUS.md`, the desk — rewritten at every close, never appended. Everything else is
found through folder names, file names and grep. [docs/why.md](docs/why.md) states the
assumptions and the evidence behind each choice, and what was rejected.

## Adopt it

**1. Clone this repo once**, anywhere you keep tools. The scaffold copies from the clone
and never retypes a file, so a stale clone means stale copies; `git pull` before scaffolding.

**2. Install the scaffold skill globally**, so it is available in folders that hold nothing
yet. Either symlink it into your agent's skills directory (for Claude Code, `~/.claude/skills`):

```sh
ln -s "$PWD/skills/workbench-scaffold" ~/.claude/skills/workbench-scaffold
```

or copy it there and point `WORKBENCH_HOME` at the clone. The two session skills are not
installed globally; the scaffold copies them into each workbench.

**3. Run `workbench-scaffold` in your project.** It picks a mode and says which before
touching anything: *fresh* for an empty folder (a short interview, then the files),
*adopt* for an existing repo (writes only what is missing, overwrites nothing), *audit*
for a repo that already has the lint (reports drift and findings, changes nothing without
a yes). Without an agent, copy by hand: `templates/*` to your root, `scripts/workbench_lint.py`,
`scripts/check` and `.githooks/pre-commit` to the same paths, and `skills/session-open`
and `skills/session-close` into `.claude/skills/`.

**4. Fill in `AGENTS.md`.** Purpose, the rules that change behaviour, the non-obvious
layout, the commands that matter, how work lands. Delete every placeholder you cannot
fill; a short file that is true beats a long one that is aspirational.

**5. Run the loop.** `git config core.hooksPath .githooks` once per clone, then start each
session with `session-open` and end it with `session-close`. `scripts/check` before every
push.

## What a session looks like

`session-open` reads the log, the desk file, the check output and the tracker, briefs
what changed and what turned urgent, and ends with exactly one proposal: the piece of
work, its issue, its branch. You pick. Work happens. `session-close` writes the decisions
and learnings down, rewrites `STATUS.md` from scratch, runs the check, commits on a
branch, opens a pull request and hands over what it could not finish. The next session
opens from that desk file, not from a transcript.

## The check

`scripts/check` runs the lint and, when a `tests/` folder exists, the unit tests. It only
reads. Exit 0 with `check: clean`, 1 on any finding, 2 when it could not run.

The lint alone is `python3 scripts/workbench_lint.py`; `--help` lists every check. Flags:

| Flag | Effect |
|---|---|
| `--agents-cap N`, `--desk-cap N` | Change the caps (100 and 120). Prefer moving overflow to a linked document. |
| `--desk FILE` | Name a desk file other than `STATUS.md`. Without it, a missing `STATUS.md` turns the desk check off. |
| `--gist` | Also require a `One-line gist:` line under every document title: a per-page summary that grep and retrieval can use. |
| `--skip DIR` | Leave a directory out of the link and gist checks. Repeatable. |

`scripts/check` calls the lint with defaults; a repo that needs a flag edits its own copy of
`scripts/check`, never the lint.

## Keeping a workbench current

The copied files (`scripts/workbench_lint.py`, `scripts/check`, `.githooks/pre-commit`,
the two session skills) are meant to stay identical to this repo. After pulling the
clone, run `workbench-scaffold` in the workbench: it detects the lint and enters audit
mode, lists each drifted file with a diff, and offers to re-copy it. Local edits to those
files are drift, not customisation; put project rules in `AGENTS.md` instead.

## What is in the repo

| Path | What it is |
|---|---|
| [templates/AGENTS.md](templates/AGENTS.md) | The operating agreement a downstream repo adopts. Capped at 100 lines. |
| [templates/CLAUDE.md](templates/CLAUDE.md) | Imports `AGENTS.md` and adds the few lines only an AI session needs. |
| [templates/STATUS.md](templates/STATUS.md) | The desk file: what is true now, who owes what. Capped at 120 lines. |
| [templates/DECISIONS.md](templates/DECISIONS.md) | An append-only decision log, one entry per decision with its why. |
| [scripts/workbench_lint.py](scripts/workbench_lint.py) | The lint: caps, links, skill frontmatter, optional gist lines. Read-only. |
| [scripts/check](scripts/check) | Runs the lint and, when `tests/` exists, the unit tests. |
| [.githooks/pre-commit](.githooks/pre-commit) | Runs `scripts/check`. Activate with `git config core.hooksPath .githooks`. |
| [skills/session-open](skills/session-open/SKILL.md) | Orient, brief, propose one next step. |
| [skills/session-close](skills/session-close/SKILL.md) | Capture, rewrite the desk, check, commit on a branch, open a PR. |
| [skills/workbench-scaffold](skills/workbench-scaffold/SKILL.md) | Copies the above into a target folder; audit mode reports drift from this repo. |
| [docs/why.md](docs/why.md) | The assumptions behind the design and the published evidence they rest on. |
| [tests/](tests/) | The lint's unit tests: `python3 -m unittest discover -s tests`. |
| [.github/workflows/check.yml](.github/workflows/check.yml) | Runs `scripts/check` on every push and pull request to this repo. |

## Is it tied to one agent?

No. `AGENTS.md` is the agreement; `CLAUDE.md` is a two-line import of it, which is what
Claude Code reads. Any agent that loads a repo-level instruction file works. The skills
are Claude Code conveniences over the loop, not requirements; the loop itself fits in the
five lines of `AGENTS.md` that describe it.

## Contributing

Open an issue, cut a branch, run `scripts/check`, open a pull request. Rules for working
on this repo are in [AGENTS.md](AGENTS.md).
