"""Guards for the quality layer and the DESIGN.md template.

The quality files are the gate the whole skill leans on, so their structure is
checked rather than trusted. The one-source-per-rule decision is also enforced:
the workflows must point at preflight.md rather than restate it.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "aurelium-ui"
QUALITY = SKILL / "references" / "quality"
WORKFLOWS = SKILL / "workflows"
TEMPLATE = SKILL / "assets" / "templates" / "DESIGN.md"

PREFLIGHT = QUALITY / "preflight.md"
RUBRIC = QUALITY / "rubric.md"
CHECKLIST = QUALITY / "detail-checklist.md"
ANTI_PATTERNS = QUALITY / "anti-patterns.md"


def read(path):
    return path.read_text(encoding="utf-8")


def flat(path):
    return re.sub(r"\s+", " ", read(path)).lower()


def table_rows(text):
    """Count data rows across every Markdown table in the text."""
    return [
        line for line in text.splitlines()
        if line.startswith("|") and not re.match(r"^\|[\s|:-]+\|$", line)
        and not line.startswith("| #") and not line.startswith("| Anti-pattern")
    ]


class FilesExistTests(unittest.TestCase):
    def test_every_quality_file_ships(self):
        for path in (PREFLIGHT, RUBRIC, CHECKLIST, ANTI_PATTERNS):
            self.assertTrue(path.is_file(), "missing {0}".format(path.name))

    def test_design_template_ships(self):
        self.assertTrue(TEMPLATE.is_file())

    def test_all_are_in_the_reference_map(self):
        skill_md = read(SKILL / "SKILL.md")
        for path in (PREFLIGHT, RUBRIC, CHECKLIST, ANTI_PATTERNS, TEMPLATE):
            relative = path.relative_to(SKILL).as_posix()
            self.assertIn(relative, skill_md, "{0} not in the reference map".format(relative))


class PreflightTests(unittest.TestCase):
    EXPECTED_GROUPS = (
        "Tokens", "Contrast and colour", "Hierarchy and layout", "States",
        "Keyboard and focus", "Semantics", "Targets", "Motion",
        "Responsive", "Performance", "Content",
    )

    def test_covers_every_group(self):
        text = read(PREFLIGHT)
        for group in self.EXPECTED_GROUPS:
            self.assertIn(group, text, "preflight missing group {0}".format(group))

    def test_every_check_is_numbered_and_has_a_method(self):
        # Each row is "| n.n | check | how |", so a check always states how.
        rows = re.findall(r"^\| (\d+\.\d+) \| (.+?) \| (.+?) \|$", read(PREFLIGHT), re.M)
        self.assertGreaterEqual(len(rows), 50, "expected at least 50 checks")
        for number, check, how in rows:
            self.assertTrue(check.strip(), number)
            self.assertTrue(how.strip(), number)

    def test_check_numbers_are_unique(self):
        numbers = re.findall(r"^\| (\d+\.\d+) \|", read(PREFLIGHT), re.M)
        self.assertEqual(len(numbers), len(set(numbers)), "duplicate check numbers")

    def test_states_the_never_claim_rule(self):
        self.assertIn("never claim a check passed unless you ran it", flat(PREFLIGHT))

    def test_references_the_contrast_script(self):
        self.assertIn("contrast.py", read(PREFLIGHT))


class SingleSourceTests(unittest.TestCase):
    """One source per rule: the workflows point, they do not restate."""

    def test_create_workflow_points_at_preflight(self):
        self.assertIn("quality/preflight.md", read(WORKFLOWS / "create.md"))

    def test_create_workflow_does_not_restate_the_gate(self):
        # A numbered 10-item list in step 10 would be a second copy of the gate.
        step = read(WORKFLOWS / "create.md").split("## 10. Pre-flight", 1)[1]
        numbered = re.findall(r"^\d+\. ", step, re.M)
        self.assertLess(
            len(numbered), 5,
            "step 10 restates the pre-flight instead of pointing at it",
        )

    def test_create_workflow_points_at_the_detail_checklist(self):
        self.assertIn("quality/detail-checklist.md", read(WORKFLOWS / "create.md"))

    def test_audit_workflow_points_at_rubric_and_preflight(self):
        text = read(WORKFLOWS / "audit.md")
        self.assertIn("quality/rubric.md", text)
        self.assertIn("quality/preflight.md", text)

    def test_doctrine_cross_links_are_restored(self):
        # These were prose in Phase 2 because the targets did not exist yet.
        doctrine = SKILL / "references" / "doctrine"
        self.assertIn("../quality/rubric.md", read(doctrine / "heuristics.md"))
        self.assertIn("../quality/preflight.md", read(doctrine / "luxury-principles.md"))


class RubricTests(unittest.TestCase):
    def test_weights_sum_to_one_hundred(self):
        weights = [int(n) for n in re.findall(r"\| (\d+)% \|", read(RUBRIC))]
        self.assertEqual(sorted(weights), [10, 20, 30, 40])
        self.assertEqual(sum(weights), 100)

    def test_names_all_four_categories(self):
        text = flat(RUBRIC)
        for category in ("design", "usability", "creativity", "content"):
            self.assertIn(category, text)

    def test_craft_checklist_has_six_items(self):
        rows = re.findall(r"^\| (C\d) \|", read(RUBRIC), re.M)
        self.assertEqual(rows, ["C1", "C2", "C3", "C4", "C5", "C6"])

    def test_states_the_independence_disclaimer(self):
        text = flat(RUBRIC)
        self.assertIn("not affiliated with", text)
        self.assertIn("independent", text)

    def test_worked_example_arithmetic_is_correct(self):
        # (7 x 0.4) + (5 x 0.3) + (6 x 0.2) + (8 x 0.1) = 6.3
        self.assertAlmostEqual(7 * 0.4 + 5 * 0.3 + 6 * 0.2 + 8 * 0.1, 6.3, places=9)
        self.assertIn("6.3", read(RUBRIC))

    def test_failed_craft_item_caps_a_category(self):
        self.assertIn("caps", flat(RUBRIC))


class DetailChecklistTests(unittest.TestCase):
    def test_has_between_forty_and_eighty_checks(self):
        ids = re.findall(r"^\| ([TSCINRM]\d+) \|", read(CHECKLIST), re.M)
        self.assertGreaterEqual(len(ids), 40, "fewer than 40 checks")
        self.assertLessEqual(len(ids), 80, "more than 80 checks")

    def test_check_ids_are_unique(self):
        ids = re.findall(r"^\| ([TSCINRM]\d+) \|", read(CHECKLIST), re.M)
        self.assertEqual(len(ids), len(set(ids)), "duplicate check ids")

    def test_covers_every_required_group(self):
        text = read(CHECKLIST)
        for group in ("Typography", "Spacing and layout", "Colour and surface",
                      "Interaction", "Content and copy", "Responsive"):
            self.assertIn(group, text, group)

    def test_defers_to_preflight_as_the_gate(self):
        self.assertIn("preflight.md", read(CHECKLIST))
        self.assertIn("this is not the gate", flat(CHECKLIST))


class AntiPatternTests(unittest.TestCase):
    def test_all_four_sections_are_complete(self):
        text = read(ANTI_PATTERNS)
        for section in ("## Visual", "## UX", "## Motion", "## Copy"):
            self.assertIn(section, text, section)

    def test_no_section_is_still_marked_as_pending(self):
        self.assertNotIn("expanded in a later release", flat(ANTI_PATTERNS))

    def test_each_section_has_substantial_content(self):
        text = read(ANTI_PATTERNS)
        for section in ("Visual", "UX", "Motion", "Copy"):
            body = text.split("## {0}".format(section), 1)[1].split("\n## ", 1)[0]
            rows = [line for line in body.splitlines() if line.startswith("| **")]
            self.assertGreaterEqual(
                len(rows), 15, "{0} section has only {1} rows".format(section, len(rows))
            )

    def test_every_row_names_a_replacement(self):
        text = read(ANTI_PATTERNS)
        for line in text.splitlines():
            if not line.startswith("| **"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            self.assertEqual(len(cells), 3, line)
            self.assertTrue(cells[2], "no replacement given: {0}".format(line))


class DesignTemplateTests(unittest.TestCase):
    def test_instructs_the_agent_to_follow_it(self):
        text = flat(TEMPLATE)
        self.assertIn("read this file before changing", text)
        self.assertIn("outranks your own preference", text)

    def test_covers_the_decisions_a_later_session_needs(self):
        text = read(TEMPLATE)
        for section in ("## Identity", "## Direction and dials", "## Tokens",
                        "## Typography", "## Layout", "## Screens",
                        "## Accessibility commitments", "## Known gaps",
                        "## Decision log"):
            self.assertIn(section, text, section)

    def test_placeholders_are_bracketed_not_angle_bracketed(self):
        # Angle brackets are banned in frontmatter and read as HTML in Markdown.
        self.assertNotIn("<", read(TEMPLATE))
        self.assertGreater(len(re.findall(r"\[[a-z0-9 ,.]+\]", read(TEMPLATE))), 20)

    def test_template_paths_cannot_be_mistaken_for_real_references(self):
        # The validator resolves backticked relative paths. A template must not
        # carry any that would fail, since it is filled in elsewhere.
        text = read(TEMPLATE)
        for match in re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|css|py))`", text):
            if "/" not in match:
                continue
            self.assertTrue(
                (SKILL / match).is_file(),
                "template references {0}, which does not resolve".format(match),
            )

    def test_names_every_direction_as_an_option(self):
        text = read(TEMPLATE)
        for name in ("quiet-luxury", "obsidian", "tactile-craft",
                     "swiss-precision", "functional-futurism"):
            self.assertIn(name, text, name)

    def test_no_em_dashes(self):
        self.assertNotIn("—", read(TEMPLATE))


class HouseStyleTests(unittest.TestCase):
    def test_no_em_dashes_in_the_quality_layer(self):
        offenders = [
            p.name for p in QUALITY.glob("*.md") if "—" in read(p)
        ]
        self.assertEqual(offenders, [])

    def test_quality_files_stay_focused(self):
        for path in QUALITY.glob("*.md"):
            lines = len(read(path).splitlines())
            self.assertLess(lines, 300, "{0} is {1} lines".format(path.name, lines))


if __name__ == "__main__":
    unittest.main()
