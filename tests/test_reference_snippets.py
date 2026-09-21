"""Checks that the reference snippets obey the rules the references state.

The foundations ban hard-coded colour and off-scale spacing. Component
guidance that violates its own rule teaches the violation, so the snippets are
checked mechanically rather than by eye.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "aurelium-ui"
REFERENCES = SKILL / "references"

COMPONENT_FILES = sorted((REFERENCES / "components").glob("*.md"))
PATTERN_FILES = sorted((REFERENCES / "patterns").glob("*.md"))
GUIDANCE_FILES = COMPONENT_FILES + PATTERN_FILES

FENCE = re.compile(r"```(\w+)?\n(.*?)```", re.DOTALL)
HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
PX = re.compile(r"(?<![\w-])(\d+(?:\.\d+)?)px")

# Properties where a raw pixel value is legitimate rather than a spacing token:
# hairlines, focus rings, explicit target sizes, and optical corrections.
PIXEL_ALLOWED = (
    "border", "border-width", "border-block-end", "border-block-start",
    "border-inline", "outline", "outline-width", "outline-offset",
    "min-block-size", "block-size", "min-inline-size", "inline-size",
    "scroll-padding-block-start", "border-color", "border-block-end-color",
    "transform",
)


def code_blocks(path, language=None):
    text = path.read_text(encoding="utf-8")
    for lang, body in FENCE.findall(text):
        if language is None or lang == language:
            yield body


def css_declarations(path):
    """Yield (property, value) for each declaration in the file's CSS blocks.

    A selector may carry a pseudo-class colon and a whole rule may sit on one
    line, so anything before an opening brace is dropped rather than parsed as
    a declaration.
    """
    for body in code_blocks(path, "css"):
        for line in body.splitlines():
            line = line.split("/*", 1)[0].strip()
            if line.startswith("@") or not line:
                continue
            if "{" in line:
                # Keep only the declarations inside a single-line rule.
                line = line.split("{", 1)[1].split("}", 1)[0].strip()
            if ":" not in line:
                continue
            for declaration in line.split(";"):
                declaration = declaration.strip()
                if ":" not in declaration:
                    continue
                prop, _, value = declaration.partition(":")
                yield path, prop.strip(), value.strip()


class TokenDisciplineTests(unittest.TestCase):
    def test_no_hard_coded_hex_colours_in_css_snippets(self):
        offenders = []
        for path in GUIDANCE_FILES:
            for _, prop, value in css_declarations(path):
                if prop.startswith("--"):
                    continue  # a token definition is allowed to hold a literal
                if HEX.search(value):
                    offenders.append(
                        "{0}: {1}: {2}".format(path.name, prop, value)
                    )
        self.assertEqual(offenders, [], "hard-coded colour in guidance snippets")

    def test_spacing_properties_use_tokens(self):
        offenders = []
        spacing_props = ("padding", "margin", "gap", "inset")
        for path in GUIDANCE_FILES:
            for _, prop, value in css_declarations(path):
                if prop.startswith("--"):
                    continue
                if not prop.startswith(spacing_props):
                    continue
                if PX.search(value):
                    offenders.append(
                        "{0}: {1}: {2}".format(path.name, prop, value)
                    )
        self.assertEqual(offenders, [], "off-scale spacing in guidance snippets")

    def test_pixel_values_only_appear_where_they_are_legitimate(self):
        offenders = []
        for path in GUIDANCE_FILES:
            for _, prop, value in css_declarations(path):
                if prop.startswith("--") or not PX.search(value):
                    continue
                if not prop.startswith(PIXEL_ALLOWED):
                    offenders.append(
                        "{0}: {1}: {2}".format(path.name, prop, value)
                    )
        self.assertEqual(offenders, [], "raw pixels outside the allowed properties")

    def test_radius_always_comes_from_a_token(self):
        offenders = []
        for path in GUIDANCE_FILES:
            for _, prop, value in css_declarations(path):
                if prop.startswith("--") or "radius" not in prop:
                    continue
                if "var(--radius" not in value and value not in ("0", "none"):
                    offenders.append("{0}: {1}: {2}".format(path.name, prop, value))
        self.assertEqual(offenders, [], "radius not taken from the scale")

    def test_transition_durations_come_from_tokens(self):
        offenders = []
        for path in GUIDANCE_FILES:
            for _, prop, value in css_declarations(path):
                if prop.startswith("--") or prop != "transition":
                    continue
                if "var(--duration" not in value:
                    offenders.append("{0}: {1}".format(path.name, value))
        self.assertEqual(offenders, [], "transition not using a duration token")


class CoverageTests(unittest.TestCase):
    EXPECTED_COMPONENTS = {
        "buttons", "forms", "navigation", "cards-lists",
        "tables", "overlays", "data-display", "media",
    }
    EXPECTED_PATTERNS = {"states", "feedback", "search-filter", "onboarding"}

    def test_every_planned_component_file_exists(self):
        self.assertEqual({p.stem for p in COMPONENT_FILES}, self.EXPECTED_COMPONENTS)

    def test_every_planned_pattern_file_exists(self):
        self.assertEqual({p.stem for p in PATTERN_FILES}, self.EXPECTED_PATTERNS)

    def test_every_file_carries_at_least_one_snippet(self):
        for path in GUIDANCE_FILES:
            blocks = list(code_blocks(path))
            self.assertTrue(blocks, "{0} has no code snippet".format(path.name))

    def test_every_file_ends_with_an_anti_patterns_table(self):
        for path in GUIDANCE_FILES:
            text = path.read_text(encoding="utf-8")
            self.assertIn("## Anti-patterns", text, path.name)

    def test_component_files_cover_their_states(self):
        # Interactive components address pointer and keyboard states; display
        # components address data states. Both vocabularies count.
        vocabulary = (
            "hover", "focus", "active", "disabled", "loading",
            "empty", "error", "partial", "skeleton", "selected",
        )
        for path in COMPONENT_FILES:
            text = path.read_text(encoding="utf-8").lower()
            found = [state for state in vocabulary if state in text]
            self.assertGreaterEqual(
                len(found), 3,
                "{0} addresses too few states: {1}".format(path.name, found),
            )

    def test_every_guidance_file_is_in_the_reference_map(self):
        skill_md = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for path in GUIDANCE_FILES:
            relative = path.relative_to(SKILL).as_posix()
            self.assertIn(relative, skill_md, "{0} missing from reference map".format(relative))

    def test_files_stay_focused(self):
        for path in GUIDANCE_FILES:
            lines = len(path.read_text(encoding="utf-8").splitlines())
            self.assertLess(lines, 300, "{0} is {1} lines".format(path.name, lines))


class HouseStyleTests(unittest.TestCase):
    def test_no_em_dashes(self):
        offenders = [p.name for p in GUIDANCE_FILES if "—" in p.read_text(encoding="utf-8")]
        self.assertEqual(offenders, [])

    def test_no_emoji_used_as_icons(self):
        # The iconography reference bans emoji, so the guidance must not model it.
        emoji = re.compile("[\U0001F300-\U0001FAFF✀-➿]")
        offenders = [
            p.name for p in GUIDANCE_FILES if emoji.search(p.read_text(encoding="utf-8"))
        ]
        self.assertEqual(offenders, [])

    def test_html_snippets_use_button_for_actions(self):
        # A div with a click handler is banned in buttons.md, so none may appear.
        for path in GUIDANCE_FILES:
            for body in code_blocks(path, "html"):
                self.assertNotIn("onclick", body, path.name)


if __name__ == "__main__":
    unittest.main()
