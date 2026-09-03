"""Tests for scripts/workbench_lint.py.

Run: python3 -m unittest discover -s tests
"""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LINT = Path(__file__).resolve().parent.parent / "scripts" / "workbench_lint.py"
spec = importlib.util.spec_from_file_location("workbench_lint", LINT)
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)


def lines(n: int, prefix: str = "line") -> str:
    return "\n".join(f"{prefix} {i}" for i in range(n)) + "\n"


class LintCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.write("AGENTS.md", "# AGENTS.md\n\n## Purpose\n\nFixture.\n")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, rel: str, text: str) -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    def findings(self, **kw) -> dict[str, list[str]]:
        sections, _ = lint.run(self.root, **kw)
        return dict(sections)

    def off(self, **kw) -> list[str]:
        return lint.run(self.root, **kw)[1]


class Caps(LintCase):
    def test_clean_fixture(self) -> None:
        self.assertEqual(sum(map(len, self.findings().values())), 0)

    def test_agents_missing(self) -> None:
        (self.root / "AGENTS.md").unlink()
        self.assertEqual(self.findings()["agents-cap"], ["AGENTS.md missing"])

    def test_agents_over_cap(self) -> None:
        self.write("AGENTS.md", lines(101))
        self.assertEqual(self.findings()["agents-cap"], ["AGENTS.md is 101 lines (cap 100)"])
        self.assertEqual(self.findings(agents_cap=150)["agents-cap"], [])

    def test_desk_default_off_when_absent(self) -> None:
        self.assertIn("desk-cap", self.off())
        self.assertNotIn("desk-cap", self.findings())

    def test_desk_default_on_when_present(self) -> None:
        self.write("STATUS.md", lines(121))
        self.assertEqual(self.findings()["desk-cap"], ["STATUS.md is 121 lines (cap 120)"])
        self.assertEqual(self.findings(desk_cap=200)["desk-cap"], [])

    def test_desk_explicit(self) -> None:
        self.assertEqual(self.findings(desk_file="notes/desk.md")["desk-cap"],
                         ["desk file notes/desk.md does not exist"])
        self.write("notes/desk.md", lines(5))
        self.assertEqual(self.findings(desk_file="notes/desk.md")["desk-cap"], [])


class Links(LintCase):
    def test_wikilinks(self) -> None:
        self.write("kb/a.md", "# a\n\n[[kb/b]] [[b]] [[kb/missing]] [[nowhere|alias]]\n")
        self.write("kb/b.md", "# b\n")
        self.assertEqual(self.findings()["links"],
                         ["kb/a.md → [[kb/missing]]", "kb/a.md → [[nowhere]]"])

    def test_wrapped_wikilink(self) -> None:
        self.write("a.md", "# a\n\nsee [[kb/\nb]]\n")
        found = self.findings()["links"]
        self.assertIn("a.md:3 wikilink spans a line break", found)
        self.assertIn("a.md:4 wikilink spans a line break", found)

    def test_relative_markdown_links(self) -> None:
        self.write("docs/a.md", "# a\n\n[ok](b.md) [up](../AGENTS.md#purpose) [gone](c.md) "
                                "[web](https://example.org/x.md) [anchor](#here) "
                                "![img](missing.png)\n")
        self.write("docs/b.md", "# b\n")
        self.assertEqual(self.findings()["links"], ["docs/a.md → (c.md)"])

    def test_code_is_ignored(self) -> None:
        self.write("a.md", "# a\n\n`[[kb/x]]` and\n\n```\n[[kb/y]] [z](z.md)\n```\n")
        self.assertEqual(self.findings()["links"], [])

    def test_skip_dirs(self) -> None:
        self.write("vendor/a.md", "[gone](c.md)\n")
        self.assertEqual(self.findings()["links"], ["vendor/a.md → (c.md)"])
        self.assertEqual(self.findings(skip=("vendor",))["links"], [])


class Skills(LintCase):
    def test_valid_frontmatter(self) -> None:
        self.write(".claude/skills/x/SKILL.md", "---\nname: x\ndescription: Does x.\n---\n# x\n")
        self.write("skills/y/SKILL.md", "---\nname: y\ndescription: \"Does y.\"\n---\n")
        self.assertEqual(self.findings()["skills"], [])

    def test_missing_fields(self) -> None:
        self.write(".claude/skills/x/SKILL.md", "---\nname: x\ndescription:\n---\n")
        self.write("skills/y/SKILL.md", "# y\nno frontmatter\n")
        self.assertEqual(self.findings()["skills"],
                         ["skills/y/SKILL.md: no frontmatter block",
                          ".claude/skills/x/SKILL.md: frontmatter lacks description"])


class Gist(LintCase):
    def test_off_by_default(self) -> None:
        self.write("kb/a.md", "# a\n\nbody\n")
        self.assertNotIn("gist", self.findings())
        self.assertIn("gist", self.off())

    def test_on(self) -> None:
        self.write("kb/a.md", "# a\n\nbody\n")
        self.write("kb/b.md", "# b\n\nOne-line gist: fine.\n")
        self.write("skills/s/SKILL.md", "---\nname: s\ndescription: d\n---\n# s\n")
        self.assertEqual(self.findings(gist=True)["gist"],
                         ["AGENTS.md: no gist line under the title",
                          "kb/a.md: no gist line under the title"])


class Cli(LintCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(LINT), "--root", str(self.root), *args],
                              capture_output=True, text=True)

    def test_exit_codes_and_report(self) -> None:
        out = self.run_cli()
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertTrue(out.stdout.startswith("workbench-lint — active: agents-cap, links, skills"))
        self.assertIn("lint: 0 finding(s)", out.stdout)

        self.write("AGENTS.md", lines(11))
        out = self.run_cli("--agents-cap", "10", "--desk", "STATUS.md")
        self.assertEqual(out.returncode, 1)
        self.assertIn("## agents-cap (1)", out.stdout)
        self.assertIn("## desk-cap (1)", out.stdout)
        self.assertIn("lint: 2 finding(s)", out.stdout)

    def test_bad_root(self) -> None:
        out = subprocess.run([sys.executable, str(LINT), "--root", str(self.root / "nope")],
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 2)


if __name__ == "__main__":
    unittest.main()
