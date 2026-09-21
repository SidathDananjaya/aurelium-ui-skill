"""Tests for tools/validate_skill.py."""

import importlib.util
import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = REPO_ROOT / "tests" / "fixtures"
VALIDATOR_PATH = REPO_ROOT / "tools" / "validate_skill.py"


def load_validator():
    """Import the validator by path, since tools/ is not a package."""
    spec = importlib.util.spec_from_file_location("validate_skill", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise ImportError("could not load {0}".format(VALIDATOR_PATH))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_validator()


def run(*argv):
    """Run the validator and return (exit_code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = validator.main(list(argv))
    return code, out.getvalue(), err.getvalue()


def fixture(name):
    return str(FIXTURES / name)


def checks_for(*argv):
    """Return the set of check names reported by a --json run."""
    code, out, _ = run(*(list(argv) + ["--json"]))
    payload = json.loads(out)
    return code, {finding["check"] for finding in payload["findings"]}


class FrontmatterParsingTests(unittest.TestCase):
    def test_parses_flat_keys(self):
        data = validator.parse_frontmatter("name: demo\ndescription: A demo skill.")
        self.assertEqual(data["name"], "demo")
        self.assertEqual(data["description"], "A demo skill.")

    def test_parses_nested_metadata(self):
        block = 'name: demo\nmetadata:\n  author: "someone"\n  version: "1.2.3"'
        data = validator.parse_frontmatter(block)
        self.assertEqual(data["metadata"], {"author": "someone", "version": "1.2.3"})

    def test_strips_matching_quotes_only(self):
        self.assertEqual(validator.strip_quotes('"quoted"'), "quoted")
        self.assertEqual(validator.strip_quotes("'quoted'"), "quoted")
        self.assertEqual(validator.strip_quotes('"unbalanced'), '"unbalanced')

    def test_value_containing_colon_is_kept_whole(self):
        data = validator.parse_frontmatter("description: Use when: the user asks.")
        self.assertEqual(data["description"], "Use when: the user asks.")

    def test_ignores_comments_and_blank_lines(self):
        data = validator.parse_frontmatter("# a comment\n\nname: demo\n")
        self.assertEqual(data, {"name": "demo"})

    def test_rejects_lists(self):
        with self.assertRaises(validator.FrontmatterError):
            validator.parse_frontmatter("tools:\n  - read\n  - write")

    def test_rejects_block_scalars(self):
        with self.assertRaises(validator.FrontmatterError):
            validator.parse_frontmatter("description: |\n  a folded value")

    def test_rejects_orphan_indented_key(self):
        with self.assertRaises(validator.FrontmatterError):
            validator.parse_frontmatter("name: demo\n  author: someone")

    def test_rejects_line_without_colon(self):
        with self.assertRaises(validator.FrontmatterError):
            validator.parse_frontmatter("name demo")

    def test_unclosed_frontmatter_is_an_error(self):
        with self.assertRaises(validator.FrontmatterError):
            validator.split_frontmatter("---\nname: demo\n")

    def test_missing_opening_delimiter_is_an_error(self):
        with self.assertRaises(validator.FrontmatterError):
            validator.split_frontmatter("# heading\n")


class ValidSkillTests(unittest.TestCase):
    def test_valid_fixture_passes(self):
        code, out, _ = run(fixture("valid-skill"))
        self.assertEqual(code, 0)
        self.assertIn("OK", out)

    def test_repository_skill_passes(self):
        code, out, err = run(str(REPO_ROOT / "skills"))
        self.assertEqual(code, 0, err)
        self.assertIn("OK", out)

    def test_json_output_is_well_formed(self):
        code, out, _ = run(fixture("valid-skill"), "--json")
        payload = json.loads(out)
        self.assertEqual(code, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["findings"], [])
        self.assertEqual(len(payload["skills"]), 1)


class BrokenFixtureTests(unittest.TestCase):
    def test_name_violations_are_reported(self):
        code, checks = checks_for(fixture("broken-name"))
        self.assertEqual(code, 1)
        self.assertEqual(checks, {"name"})

    def test_angle_brackets_are_rejected(self):
        code, checks = checks_for(fixture("angle-brackets"))
        self.assertEqual(code, 1)
        self.assertIn("frontmatter", checks)

    def test_missing_reference_paths_are_reported(self):
        code, out, _ = run(fixture("broken-links"), "--json")
        payload = json.loads(out)
        self.assertEqual(code, 1)
        messages = " ".join(finding["message"] for finding in payload["findings"])
        self.assertIn("references/missing.md", messages)
        self.assertIn("workflows/nowhere.md", messages)

    def test_missing_description_is_reported(self):
        code, checks = checks_for(fixture("missing-description"))
        self.assertEqual(code, 1)
        self.assertIn("frontmatter", checks)

    def test_absent_frontmatter_is_reported(self):
        code, checks = checks_for(fixture("no-frontmatter"))
        self.assertEqual(code, 1)
        self.assertEqual(checks, {"frontmatter"})

    def test_incomplete_direction_json_is_reported(self):
        code, out, _ = run(fixture("broken-direction"), "--json")
        payload = json.loads(out)
        self.assertEqual(code, 1)
        messages = " ".join(finding["message"] for finding in payload["findings"])
        for missing in ("colors.dark", "type.ratio", "spacing", "motion", "contrast_pairs"):
            self.assertIn(missing, messages)


class DiscoveryTests(unittest.TestCase):
    def test_discovers_every_fixture_skill(self):
        found = validator.discover_skills(FIXTURES)
        names = {path.name for path in found}
        self.assertIn("valid-skill", names)
        self.assertIn("broken-direction", names)

    def test_skill_folder_is_returned_directly(self):
        found = validator.discover_skills(FIXTURES / "valid-skill")
        self.assertEqual(found, [FIXTURES / "valid-skill"])

    def test_missing_path_is_a_usage_finding(self):
        code, checks = checks_for(str(REPO_ROOT / "does-not-exist"))
        self.assertEqual(code, 1)
        self.assertEqual(checks, {"usage"})

    def test_folder_without_a_skill_is_a_usage_finding(self):
        code, checks = checks_for(str(REPO_ROOT / "tools"))
        self.assertEqual(code, 1)
        self.assertEqual(checks, {"usage"})


class LineCountTests(unittest.TestCase):
    def test_long_skill_file_fails(self):
        findings = []
        long_file = FIXTURES / "valid-skill" / "SKILL.md"
        original = long_file.read_text(encoding="utf-8")
        padded = original + "\nfiller\n" * validator.MAX_SKILL_LINES
        try:
            long_file.write_text(padded, encoding="utf-8")
            validator.check_frontmatter(long_file, "valid-skill", findings)
        finally:
            long_file.write_text(original, encoding="utf-8")
        self.assertTrue(any(finding.check == "line-count" for finding in findings))

    def test_repository_skill_is_within_the_limit(self):
        skill_md = REPO_ROOT / "skills" / "aurelium-ui" / "SKILL.md"
        line_count = len(skill_md.read_text(encoding="utf-8").splitlines())
        self.assertLess(line_count, validator.MAX_SKILL_LINES)


class ReferenceResolutionTests(unittest.TestCase):
    def test_external_and_anchor_links_are_skipped(self):
        findings = []
        skill_dir = FIXTURES / "valid-skill"
        validator.check_references(skill_dir, findings)
        self.assertEqual(findings, [])

    def test_candidate_paths_strip_anchors(self):
        skill_dir = FIXTURES / "valid-skill"
        options = validator.candidate_paths(
            skill_dir / "SKILL.md", skill_dir, "references/example.md#section"
        )
        self.assertTrue(any(option.exists() for option in options))


if __name__ == "__main__":
    unittest.main()
