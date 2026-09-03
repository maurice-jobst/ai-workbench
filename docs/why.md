# Why the pattern looks like this

One-line gist: the assumptions behind the workbench and the published evidence they rest
on, stated so you can disagree with them before adopting it.

## Assumptions

1. **One or a few operators, one repo per project.** Multi-team workflows would need
   review lanes this pattern leaves out on purpose; a branch and a pull request are enough.
2. **The hot corpus stays small.** Below roughly 100k tokens of live content, navigation by
   folder names, file names and grep beats vector retrieval on quality and traceability.
   If a repo outgrows that, add keyword retrieval over per-page gist lines first.
3. **The agent will sometimes be wrong in fluent prose.** Every mechanism here assumes it:
   the check, the caps, the rule that a doc stating how something works is a claim.
4. **Sessions get interrupted.** Durable file state is the source of truth; the chat is
   scaffolding. Half-done work is committed as work in progress, never left in a transcript.

## Principles

- **Markdown is the state.** Versioned plain text is diffable, greppable, portable and
  reviewable. A second tracker splits the truth.
- **AI at the edges, deterministic core.** Ask of every task whether a boring tool would
  do it, then use that. A lint never hallucinates.
- **Just-in-time retrieval, capped.** The always-loaded layer is an agreement you can read
  in two minutes plus one desk file. Context is the scarce resource; spend it on the task.
- **The narrow lane for every tool.** Issues track that a follow-up exists; the repo holds
  the reasoning; chat holds nothing that matters past the session.
- **Prune like code.** Review the agreement when the agent misbehaves and prune it on
  every pass. An instruction file that only grows stops working.

## Evidence

- [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):
  recall degrades as context grows; folder hierarchy, naming and timestamps are retrieval
  signals; load instructions up front and fetch everything else just in time.
  → the caps, the two-file hot layer, gist lines.
- [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices):
  bloated instruction files get ignored; treat the memory file as code.
  → the 100-line cap and the line test "would removing this cause mistakes?".
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents):
  progress files are the recommended cross-session memory; machine-checkable verification
  turns supervised sessions into unattended ones; open with the log and the progress file.
  → the desk file, `scripts/check`, step one of `session-open`.
- [Claude Code expertise study](https://www.anthropic.com/research/claude-code-expertise):
  people keep most planning decisions and delegate most execution.
  → `session-open` ends with one proposal and waits.
- [Codellaborator, CHI 2025](https://dl.acm.org/doi/10.1145/3706598.3713357): proactive
  agents raise efficiency but disrupt workflow; visible context reduces the cost.
  → proactivity is channelled into one session-start brief instead of interruptions.
- [arXiv 2607.04576](https://arxiv.org/pdf/2607.04576): per-page one-line summaries cut
  agent cost by a third to a half at non-inferior quality.
  → the optional gist-line check.
- Practitioner consensus on agent-maintained wikis: ingest and query get built, lint gets
  skipped. → the lint exists and the hook runs it.

## Rejected, deliberately

| Rejected | Why |
|---|---|
| Vector search over the repo | Loses to a navigable markdown tree at this scale and destroys traceability. |
| Autonomous scheduled runs as the default | Session-start proactivity captures most of the value without background surprises. |
| Live write access to systems of record | A confused agent with write access is the failure mode; paste by hand costs minutes. |
| Test-driven ceremony for glue | Checks concentrate where failure is silent: caps, links, drift. |
