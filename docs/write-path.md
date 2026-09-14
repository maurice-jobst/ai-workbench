# The write path: how a proposal reaches an external system

One-line gist: the six-step order for any new path that writes to a system the repo does not
own — a shop API, a DNS provider, a calendar, a fleet — so that a wrong proposal is caught
before it lands and a change made elsewhere is never silently overwritten.

## The problem it solves

A workbench proposes changes to systems it does not own. The tempting shortcut is a script
that reads the target, decides, and writes in one go. It works until the day the target
changed under it (someone edited in the UI), the script was right about the wrong object, or
nobody can say afterwards what it did. Each of those has happened once in the repos this
pattern comes from; the order below is what stopped them recurring.

## The order

Build the path in this order, and do not skip forward. Each step is small; the value is in
the sequence.

1. **A decision function.** One pure function per write action that takes the proposed
   change and the live state and answers `apply`, `noop` or `conflict`, with a one-line
   reason. `noop`: the target already says this. `conflict`: the target says something the
   proposal did not expect — somebody changed it, or the proposal is stale. The function
   never writes and never reads the network; the caller hands it the live state.
2. **A self-checking generator.** The script that writes proposals into the queue file
   reads the live snapshot, sets `expected` on every entry to what it saw, and runs every
   entry through the decision function before emitting it. Anything that comes back
   `conflict` is a finding in the generator's report, never a queue entry.
3. **Tests on both.** The decision function is table-driven and cheap to test exhaustively;
   the generator's test proves it refuses what the function refuses. These tests carry load:
   they are what lets a review trust a queue of three hundred entries.
4. **One probe before the round.** The first apply is one asset, chosen because it is cheap
   to throw away, and it is reviewed on the target before the round runs.
5. **Read-back through the same reader.** After an apply, read the target again with the
   reader the generator used and compare. No read-back, no finding: the apply log records
   what was sent, the read-back records what stands.
6. **A dated baseline note.** One short note per round — what was applied, what the
   read-back showed, what was left out and why — so the next round starts from a fact.

## The gate around it

The queue file is the approval surface: a proposal is a diff in a pull request, the merge is
the approval, and the apply runs on the operator's explicit command, never on a timer and
never on the agent's own initiative. The decision function's `conflict` is what protects an
edit made in the target's own UI: the apply refuses it and reports it; nothing local ever
reverts a remote change.

## What it costs

A new write action is six small artifacts instead of one script. In practice the decision
function and its tests take an hour, the generator reuses the queue-writing module every
other generator uses, and the probe is one entry. The cost is paid once per action; the
saving is every round after the first.

Related: [templates/AGENTS.md](../templates/AGENTS.md) (the rule that names this order),
[why.md](why.md) (the assumptions behind the pattern).
