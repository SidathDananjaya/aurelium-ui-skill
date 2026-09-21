"""Structural guards for SKILL.md and the workflow files.

The router is the entry point every agent loads, so its shape is worth
protecting against accidental loss during later phases.
"""

import importlib.util
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "aurelium-ui"
SKILL_MD = SKILL / "SKILL.md"
WORKFLOWS = SKILL / "workflows"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load("validate_skill", REPO_ROOT / "tools" / "validate_skill.py")
tokens = load("tokens_for_skill", SKILL / "scripts" / "tokens.py")

SKILL_TEXT = SKILL_MD.read_text(encoding="utf-8")
FRONTMATTER = validator.parse_frontmatter(validator.split_frontmatter(SKILL_TEXT)[0])
BODY = SKILL_TEXT.split("---", 2)[2]


def flat(text):
    """Collapse whitespace so a phrase split across a line wrap still matches."""
    return re.sub(r"\s+", " ", text).lower()


BODY_FLAT = flat(BODY)


class FrontmatterTests(unittest.TestCase):
    def test_name_matches_the_folder(self):
        self.assertEqual(FRONTMATTER["name"], SKILL.name)

    def test_license_is_mit(self):
        self.assertEqual(FRONTMATTER["license"], "MIT")

    def test_metadata_carries_author_and_version(self):
        metadata = FRONTMATTER["metadata"]
        self.assertEqual(metadata["author"], "SidathDananjaya")
        self.assertRegex(metadata["version"], r"^\d+\.\d+\.\d+$")

    def test_no_placeholder_angle_brackets_survive(self):
        block = validator.split_frontmatter(SKILL_TEXT)[0]
        self.assertNotIn("<", block)
        self.assertNotIn(">", block)

    def test_description_is_within_the_spec_limit(self):
        self.assertLessEqual(len(FRONTMATTER["description"]), 1024)

    def test_description_states_what_and_when(self):
        description = FRONTMATTER["description"].lower()
        # "what it does" verbs
        for word in ("design", "build"):
            self.assertIn(word, description)
        # "when to use it" triggers, which is what actually controls activation
        for word in ("redesign", "polish", "elevate", "review", "audit"):
            self.assertIn(word, description)

    def test_description_covers_the_archetypes_users_ask_for(self):
        description = FRONTMATTER["description"].lower()
        for word in ("dashboard", "saas", "e-commerce", "booking", "fintech",
                     "portfolio", "landing"):
            self.assertIn(word, description)

    def test_description_covers_the_adjectives_users_ask_for(self):
        description = FRONTMATTER["description"].lower()
        for word in ("premium", "luxury", "elegant", "minimal", "futuristic"):
            self.assertIn(word, description)


class BodySectionTests(unittest.TestCase):
    REQUIRED_SECTIONS = [
        "## Modes",
        "## Non-negotiable laws",
        "## Dials",
        "## Directions",
        "## Reference map",
        "## Output contract",
    ]

    def test_every_required_section_is_present(self):
        for heading in self.REQUIRED_SECTIONS:
            self.assertIn(heading, BODY, "missing {0}".format(heading))

    def test_sections_appear_in_the_documented_order(self):
        positions = [BODY.index(heading) for heading in self.REQUIRED_SECTIONS]
        self.assertEqual(positions, sorted(positions))

    def test_all_ten_laws_are_listed(self):
        laws = re.findall(r"^\d+\. \*\*", BODY, re.MULTILINE)
        self.assertEqual(len(laws), 10, laws)

    def test_complete_states_rule_names_every_state(self):
        for state in ("loading", "empty", "recoverable error", "fatal error",
                      "partial data", "offline", "success", "long content",
                      "permission denied"):
            self.assertIn(state, BODY_FLAT, state)

    def test_all_three_dials_are_defined(self):
        for dial in ("OPULENCE", "DENSITY", "MOTION"):
            self.assertIn(dial, BODY)

    def test_dial_defaults_are_stated(self):
        self.assertIn("opulence 4, density 5", BODY_FLAT)

    def test_both_workflows_are_referenced(self):
        self.assertIn("workflows/create.md", BODY)
        self.assertIn("workflows/audit.md", BODY)

    def test_every_direction_appears_in_the_table(self):
        for name in tokens.available_directions(SKILL / "assets" / "directions"):
            label = name.replace("-", " ").title().replace("Ui", "UI")
            self.assertIn(label, BODY, "{0} missing from the directions table".format(label))


class ReferenceMapTests(unittest.TestCase):
    def test_every_mapped_path_exists(self):
        section = BODY.split("## Reference map", 1)[1].split("## Output contract", 1)[0]
        paths = re.findall(r"`([a-z0-9_./-]+\.(?:md|py))`", section)
        self.assertGreaterEqual(len(paths), 10, paths)
        for relative in paths:
            self.assertTrue(
                (SKILL / relative).is_file(), "reference map points at missing {0}".format(relative)
            )

    def test_doctrine_and_foundations_are_fully_mapped(self):
        section = BODY.split("## Reference map", 1)[1]
        for folder in ("doctrine", "foundations"):
            for path in sorted((SKILL / "references" / folder).glob("*.md")):
                self.assertIn(
                    "references/{0}/{1}".format(folder, path.name),
                    section,
                    "{0} is not in the reference map".format(path.name),
                )


class WorkflowTests(unittest.TestCase):
    def test_both_workflow_files_exist(self):
        self.assertTrue((WORKFLOWS / "create.md").is_file())
        self.assertTrue((WORKFLOWS / "audit.md").is_file())

    def test_create_workflow_covers_every_planned_step(self):
        text = flat((WORKFLOWS / "create.md").read_text(encoding="utf-8"))
        for step in ("infer the brief", "direction and dials", "design system",
                     "information architecture", "layout", "components",
                     "state", "motion pass", "detail pass", "pre-flight"):
            self.assertIn(step, text, step)

    def test_create_workflow_lists_every_required_state(self):
        text = flat((WORKFLOWS / "create.md").read_text(encoding="utf-8"))
        for state in ("loading", "empty, first use", "empty, no results",
                      "error, recoverable", "error, fatal", "partial data",
                      "offline", "success", "long content", "permission denied"):
            self.assertIn(state, text, state)

    def test_audit_workflow_uses_the_rubric_weights(self):
        text = (WORKFLOWS / "audit.md").read_text(encoding="utf-8")
        for weight in ("40%", "30%", "20%", "10%"):
            self.assertIn(weight, text)

    def test_audit_workflow_defines_three_severities(self):
        text = (WORKFLOWS / "audit.md").read_text(encoding="utf-8")
        for severity in ("Critical", "Important", "Polish"):
            self.assertIn(severity, text)

    def test_workflows_do_not_reference_missing_files(self):
        # The validator covers this, but a failure here names the workflow.
        findings = []
        validator.check_references(SKILL, findings)
        self.assertEqual([str(finding) for finding in findings], [])


class HouseStyleTests(unittest.TestCase):
    def test_no_em_dashes_anywhere_in_the_skill(self):
        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in SKILL.rglob("*.md")
            if "—" in path.read_text(encoding="utf-8")
        ]
        self.assertEqual(offenders, [])

    def test_skill_md_stays_well_under_the_limit(self):
        lines = len(SKILL_TEXT.splitlines())
        self.assertLess(lines, 250, "SKILL.md is {0} lines, target is under 250".format(lines))


if __name__ == "__main__":
    unittest.main()
