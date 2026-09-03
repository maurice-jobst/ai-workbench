#!/usr/bin/env python3
"""workbench_lint.py — deterministic checks for a file-first AI workbench.

    python3 scripts/workbench_lint.py [--root DIR] [--agents-cap N]
                                      [--desk FILE] [--desk-cap N]
                                      [--gist] [--skip DIR ...]

Checks (every finding exits 1; the report is the product):
  agents-cap   AGENTS.md exists and is at most --agents-cap lines (100).
  desk-cap     the desk file (--desk, default STATUS.md) is at most
               --desk-cap lines (120). A missing default desk turns the
               check off; a missing --desk given explicitly is a finding.
  links        [[wikilinks]] and relative markdown links resolve to a file
               in the repo; no wikilink spans a line break.
  skills       every skills/*/SKILL.md and .claude/skills/*/SKILL.md has
               frontmatter with a non-empty name and description.
  gist         (--gist, off by default) every markdown document opens with
               a title followed by a `One-line gist:` line.

Exit 2 means the lint could not run. Standard library only.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_SKIP = (".git", "__pycache__", "node_modules", ".claude/worktrees")
WIKILINK_RE = re.compile(r"\[\[([^\]|#<>]+?)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.M | re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
SKILL_GLOBS = ("skills/*/SKILL.md", ".claude/skills/*/SKILL.md")


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def line_count(p: Path) -> int:
    return len(read(p).splitlines())


def default_root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    return Path(out.stdout.strip()) if out.returncode == 0 else Path.cwd()


def md_files(root: Path, skip: tuple[str, ...]) -> list[Path]:
    skipped = [root / s for s in skip]
    return sorted(p for p in root.rglob("*.md")
                  if not any(p.is_relative_to(s) for s in skipped))


# ── checks ────────────────────────────────────────────────────────────

def check_agents_cap(root: Path, cap: int) -> list[str]:
    agents = root / "AGENTS.md"
    if not agents.is_file():
        return ["AGENTS.md missing"]
    n = line_count(agents)
    return [f"AGENTS.md is {n} lines (cap {cap})"] if n > cap else []


def check_desk_cap(root: Path, desk: str, cap: int) -> list[str]:
    p = root / desk
    if not p.is_file():
        return [f"desk file {desk} does not exist"]
    n = line_count(p)
    return [f"{desk} is {n} lines (cap {cap})"] if n > cap else []


def resolves(base: Path, root: Path, target: str) -> bool:
    candidates = [base / target, root / target.lstrip("/")]
    for c in list(candidates):
        candidates.append(c.with_name(c.name + ".md"))
    return any(c.exists() for c in candidates)


def check_links(root: Path, skip: tuple[str, ...]) -> list[str]:
    findings: list[str] = []
    for p in md_files(root, skip):
        rel = p.relative_to(root)
        raw = read(p)
        for n, line in enumerate(raw.splitlines(), start=1):
            if line.count("[[") != line.count("]]"):
                findings.append(f"{rel}:{n} wikilink spans a line break")
        text = INLINE_CODE_RE.sub("", FENCE_RE.sub("", raw))
        for target in WIKILINK_RE.findall(text):
            target = target.strip()
            if target and not resolves(p.parent, root, target):
                findings.append(f"{rel} → [[{target}]]")
        for target in MDLINK_RE.findall(text):
            target = target.split("#", 1)[0]
            if not target or SCHEME_RE.match(target) or target.startswith("//"):
                continue
            if not (p.parent / target).exists():
                findings.append(f"{rel} → ({target})")
    return findings


def frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            fields[key.strip()] = value.strip().strip("'\"")
    return None


def check_skills(root: Path) -> list[str]:
    findings: list[str] = []
    for pattern in SKILL_GLOBS:
        for p in sorted(root.glob(pattern)):
            rel = p.relative_to(root)
            fm = frontmatter(read(p))
            if fm is None:
                findings.append(f"{rel}: no frontmatter block")
                continue
            for key in ("name", "description"):
                if not fm.get(key):
                    findings.append(f"{rel}: frontmatter lacks {key}")
    return findings


def check_gist(root: Path, skip: tuple[str, ...]) -> list[str]:
    findings: list[str] = []
    for p in md_files(root, skip):
        lines = [l for l in read(p).splitlines() if l.strip()]
        if not lines or lines[0].strip() == "---":
            continue  # frontmatter documents (skills) carry a description instead
        if not lines[0].startswith("# "):
            continue
        if len(lines) < 2 or not lines[1].startswith("One-line gist:"):
            findings.append(f"{p.relative_to(root)}: no gist line under the title")
    return findings


# ── report ────────────────────────────────────────────────────────────

def run(root: Path, agents_cap: int = 100, desk_file: str | None = None,
        desk_cap: int = 120, gist: bool = False,
        skip: tuple[str, ...] = DEFAULT_SKIP) -> tuple[list[tuple[str, list[str]]], list[str]]:
    """Return ([(check, findings)], [checks that were off])."""
    desk_name = desk_file or "STATUS.md"
    desk_on = desk_file is not None or (root / desk_name).is_file()
    sections = [("agents-cap", check_agents_cap(root, agents_cap))]
    off: list[str] = []
    if desk_on:
        sections.append(("desk-cap", check_desk_cap(root, desk_name, desk_cap)))
    else:
        off.append("desk-cap")
    sections.append(("links", check_links(root, skip)))
    sections.append(("skills", check_skills(root)))
    if gist:
        sections.append(("gist", check_gist(root, skip)))
    else:
        off.append("gist")
    return sections, off


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", type=Path, default=None,
                    help="repo root (default: git toplevel, else cwd)")
    ap.add_argument("--agents-cap", type=int, default=100)
    ap.add_argument("--desk", default=None,
                    help="desk file relative to root (default STATUS.md, off if absent)")
    ap.add_argument("--desk-cap", type=int, default=120)
    ap.add_argument("--gist", action="store_true", help="require One-line gist lines")
    ap.add_argument("--skip", action="append", default=[],
                    help="extra directory to leave out of link/gist checks")
    args = ap.parse_args(argv)

    root = (args.root or default_root()).resolve()
    if not root.is_dir():
        print(f"lint: {root} is not a directory", file=sys.stderr)
        return 2
    skip = DEFAULT_SKIP + tuple(args.skip)
    sections, off = run(root, args.agents_cap, args.desk, args.desk_cap, args.gist, skip)

    header = "workbench-lint — active: " + ", ".join(name for name, _ in sections)
    if off:
        header += " | off: " + ", ".join(off)
    print(header)
    total = 0
    for name, items in sections:
        if items:
            total += len(items)
            print(f"\n## {name} ({len(items)})")
            for it in items:
                print(f"  - {it}")
    print(f"\nlint: {total} finding(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
