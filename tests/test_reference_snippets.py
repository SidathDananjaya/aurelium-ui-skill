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
MOTION_FILES = sorted((REFERENCES / "motion").glob("*.md"))
STACK_FILES = sorted((REFERENCES / "stacks").glob("*.md"))
GUIDANCE_FILES = COMPONENT_FILES + PATTERN_FILES + MOTION_FILES + STACK_FILES

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


def flat_text(path):
    """Lowercased with whitespace collapsed, so a wrapped phrase still matches."""
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).lower()


def code_blocks(path, language=None):
    text = path.read_text(encoding="utf-8")
    for lang, body in FENCE.findall(text):
        if language is None or lang == language:
            yield body


COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
DECLARATION = re.compile(r"([a-zA-Z-]+)\s*:\s*([^;{}]+?)\s*[;}]", re.DOTALL)


def css_declarations(path):
    """Yield (path, property, value) for each declaration in the CSS blocks.

    Matching on the whole block rather than line by line handles declarations
    that wrap across several lines, such as a multi-part transition. Selectors
    are not matched because a selector is followed by an opening brace rather
    than a semicolon, and at-rule preludes fall out for the same reason.
    """
    for body in code_blocks(path, "css"):
        body = COMMENT.sub(" ", body)
        for prop, value in DECLARATION.findall(body):
            value = re.sub(r"\s+", " ", value).strip()
            yield path, prop.strip(), value


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
        # Motion keeps its anti-patterns in quality/anti-patterns.md instead.
        for path in COMPONENT_FILES + PATTERN_FILES + STACK_FILES:
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
        # recipes.md is a catalogue of eleven recipes, so it gets more room.
        limits = {"recipes.md": 400}
        for path in GUIDANCE_FILES:
            lines = len(path.read_text(encoding="utf-8").splitlines())
            limit = limits.get(path.name, 300)
            self.assertLess(
                lines, limit, "{0} is {1} lines, limit {2}".format(path.name, lines, limit)
            )


class StackTests(unittest.TestCase):
    """Every stack must map to the generated tokens rather than fork them."""

    EXPECTED = {"html-css", "tailwind", "react", "nextjs"}

    def test_all_four_stacks_ship(self):
        self.assertEqual({p.stem for p in STACK_FILES}, self.EXPECTED)

    def test_each_points_at_the_token_generator(self):
        for path in STACK_FILES:
            text = path.read_text(encoding="utf-8")
            self.assertTrue(
                "tokens.py" in text or "tokens.css" in text,
                "{0} does not reference the generated tokens".format(path.name),
            )

    def test_tailwind_recipe_requires_the_inline_theme_directive(self):
        # Without "inline" the values bake in and theme switching dies.
        text = (REFERENCES / "stacks" / "tailwind.md").read_text(encoding="utf-8")
        self.assertIn("@theme inline", text)
        self.assertIn("au-", text)

    def test_tailwind_recipe_matches_what_the_generator_emits(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "tokens_for_stacks", SKILL / "scripts" / "tokens.py"
        )
        tokens = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tokens)

        direction = tokens.load_direction(
            "obsidian", SKILL / "assets" / "directions"
        )
        emitted = tokens.format_tailwind(
            tokens.build_tokens(direction, 4, 5, 4), "auto"
        )
        # The recipe teaches these exact shapes, so they must be real.
        self.assertIn("@theme inline", emitted)
        self.assertIn("--color-page: var(--au-color-page);", emitted)
        self.assertNotIn("module.exports", emitted)

    def test_each_warns_against_forking_the_system(self):
        # A stack either states the regenerate rule itself, or defers to the
        # stack file that does. nextjs.md builds on react.md by design.
        for path in STACK_FILES:
            text = flat_text(path)
            defers = any(
                "{0}.md".format(other) in text
                for other in self.EXPECTED
                if other != path.stem
            )
            self.assertTrue(
                "regenerate" in text or defers,
                "{0} neither states the regenerate rule nor defers".format(path.name),
            )

    def test_the_stacks_that_define_token_handling_state_the_rule(self):
        for name in ("html-css", "tailwind", "react"):
            text = flat_text(REFERENCES / "stacks" / "{0}.md".format(name))
            self.assertIn("regenerate", text, name)

    def test_no_stack_recommends_hand_editing_tokens(self):
        for path in STACK_FILES:
            text = flat_text(path)
            if "hand-edit" in text or "hand edit" in text:
                self.assertTrue(
                    "never" in text or "anti-pattern" in text,
                    "{0} mentions hand editing without forbidding it".format(path.name),
                )

    def test_react_and_nextjs_cover_state_rendering(self):
        text = flat_text(REFERENCES / "stacks" / "react.md")
        for topic in ("key", "focus", "states"):
            self.assertIn(topic, text, topic)

    def test_nextjs_covers_fonts_metadata_and_images(self):
        text = flat_text(REFERENCES / "stacks" / "nextjs.md")
        for topic in ("next/font", "metadatabase", "next/image", "priority"):
            self.assertIn(topic, text, topic)

    def test_every_stack_is_in_the_reference_map(self):
        skill_md = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for path in STACK_FILES:
            relative = path.relative_to(SKILL).as_posix()
            self.assertIn(relative, skill_md, "{0} missing from reference map".format(relative))


class MotionTests(unittest.TestCase):
    """Motion guidance must obey the rules it states.

    The acceptance check for the motion phase is that every recipe carries a
    reduced-motion variant. That is the easiest thing to fudge in review, so it
    is checked mechanically.
    """

    RECIPES = REFERENCES / "motion" / "recipes.md"
    PRINCIPLES = REFERENCES / "motion" / "principles.md"

    def test_both_motion_files_exist(self):
        self.assertTrue(self.RECIPES.is_file())
        self.assertTrue(self.PRINCIPLES.is_file())

    def test_every_motion_css_block_handles_reduced_motion(self):
        # Any block that animates must sit in a file that also addresses
        # prefers-reduced-motion, and the recipes file addresses it per recipe.
        for path in MOTION_FILES:
            text = path.read_text(encoding="utf-8")
            animates = any(
                "transition:" in block or "animation:" in block
                for block in code_blocks(path, "css")
            )
            if animates:
                self.assertIn(
                    "prefers-reduced-motion", text,
                    "{0} animates without a reduced-motion path".format(path.name),
                )

    def test_each_recipe_section_has_a_reduced_motion_path(self):
        text = self.RECIPES.read_text(encoding="utf-8")
        # Split on level-two headings, skipping the intro and the checklist.
        sections = re.split(r"\n## ", text)[1:]
        skip = ("Recipe checklist",)
        checked = 0
        for section in sections:
            heading = section.split("\n", 1)[0].strip()
            if heading in skip:
                continue
            body = section
            if "transition:" not in body and "animation:" not in body:
                continue
            checked += 1
            self.assertIn(
                "prefers-reduced-motion", body,
                "recipe '{0}' has no reduced-motion variant".format(heading),
            )
        self.assertGreaterEqual(checked, 10, "expected at least 10 animated recipes")

    def test_no_raw_millisecond_durations(self):
        offenders = []
        for path in MOTION_FILES:
            for _, prop, value in css_declarations(path):
                if prop.startswith("--"):
                    continue
                if not ("duration" in prop or prop in ("transition", "animation")):
                    continue
                # 1ms is the documented reduced-motion floor.
                for match in re.findall(r"(\d+)ms", value):
                    if match != "1":
                        offenders.append(
                            "{0}: {1}: {2}".format(path.name, prop, value)
                        )
        self.assertEqual(offenders, [], "raw millisecond values instead of tokens")

    def test_no_bare_easing_keywords(self):
        offenders = []
        for path in MOTION_FILES:
            for _, prop, value in css_declarations(path):
                if prop.startswith("--") or prop not in ("transition", "animation"):
                    continue
                # "linear" is permitted for spinners, which live elsewhere.
                if re.search(r"\b(ease-in-out|ease-in|ease-out)\b", value):
                    offenders.append("{0}: {1}: {2}".format(path.name, prop, value))
                elif re.search(r"\bease\b", value) and "var(--ease" not in value:
                    offenders.append("{0}: {1}: {2}".format(path.name, prop, value))
        self.assertEqual(offenders, [], "bare easing keyword instead of a token")

    def test_never_animates_from_zero_scale(self):
        for path in MOTION_FILES:
            text = path.read_text(encoding="utf-8")
            for block in code_blocks(path, "css"):
                self.assertNotIn(
                    "scale(0)", block,
                    "{0} animates from scale(0)".format(path.name),
                )

    def test_principles_cover_the_required_topics(self):
        text = flat_text(self.PRINCIPLES)
        for topic in ("purpose test", "duration", "exit", "easing", "spring",
                      "interruptib", "reduced motion", "stagger", "infinite"):
            self.assertIn(topic, text, topic)

    def test_recipes_cover_the_planned_set(self):
        text = flat_text(self.RECIPES)
        for recipe in ("button press", "hover lift", "dropdown", "modal",
                       "drawer", "toast", "list add", "page transition",
                       "skeleton", "count-up", "scroll reveal"):
            self.assertIn(recipe, text, recipe)

    def test_anti_patterns_file_has_a_complete_motion_section(self):
        path = REFERENCES / "quality" / "anti-patterns.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("## Motion", text)
        section = text.split("## Motion", 1)[1].split("\n## ", 1)[0]
        rows = [line for line in section.splitlines() if line.startswith("| **")]
        self.assertGreaterEqual(len(rows), 15, "motion anti-patterns section is thin")

    def test_motion_files_are_in_the_reference_map(self):
        skill_md = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for path in MOTION_FILES + [REFERENCES / "quality" / "anti-patterns.md"]:
            relative = path.relative_to(SKILL).as_posix()
            self.assertIn(relative, skill_md, "{0} missing from reference map".format(relative))


class ArchetypeTests(unittest.TestCase):
    EXPECTED = {
        "landing", "dashboard", "analytics", "ecommerce",
        "booking", "fintech", "admin", "auth-onboarding",
    }
    FILES = sorted(
        p for p in (REFERENCES / "archetypes").glob("*.md") if p.stem != "index"
    )
    INDEX = REFERENCES / "archetypes" / "index.md"

    REQUIRED_SECTIONS = (
        "## User goals",
        "## Primary tasks",
        "## Information architecture",
        "## Key screens",
        "## Critical states",
        "## Luxury moments",
        "## Pitfalls",
        "## Recommended directions and dials",
    )

    def test_all_eight_archetypes_ship(self):
        self.assertEqual({p.stem for p in self.FILES}, self.EXPECTED)

    def test_each_uses_the_full_template(self):
        for path in self.FILES:
            text = path.read_text(encoding="utf-8")
            for heading in self.REQUIRED_SECTIONS:
                self.assertIn(heading, text, "{0} missing {1}".format(path.name, heading))

    def test_each_stays_under_two_hundred_lines(self):
        for path in self.FILES:
            lines = len(path.read_text(encoding="utf-8").splitlines())
            self.assertLess(lines, 200, "{0} is {1} lines".format(path.name, lines))

    def test_each_references_components_or_patterns(self):
        # The plan requires archetypes to link out rather than repeat guidance.
        for path in self.FILES:
            text = path.read_text(encoding="utf-8")
            links = re.findall(r"\.\./(?:components|patterns)/([a-z-]+\.md)", text)
            self.assertGreaterEqual(
                len(set(links)), 2,
                "{0} references too few component or pattern files".format(path.name),
            )

    def test_every_referenced_relative_path_exists(self):
        base = REFERENCES / "archetypes"
        for path in list(self.FILES) + [self.INDEX]:
            text = path.read_text(encoding="utf-8")
            for relative in set(re.findall(r"`(\.\./[a-z0-9./-]+\.(?:md|py))`", text)):
                self.assertTrue(
                    (base / relative).resolve().is_file(),
                    "{0} points at missing {1}".format(path.name, relative),
                )

    def test_each_recommends_dials_within_range(self):
        for path in self.FILES:
            text = path.read_text(encoding="utf-8")
            section = text.split("## Recommended directions and dials", 1)[1]
            numbers = [int(n) for n in re.findall(r"\|\s*(\d+)\s*\|", section)]
            self.assertTrue(numbers, "{0} lists no dial values".format(path.name))
            for value in numbers:
                self.assertTrue(
                    1 <= value <= 10,
                    "{0} has a dial value of {1}".format(path.name, value),
                )

    def test_index_links_every_archetype(self):
        index = self.INDEX.read_text(encoding="utf-8")
        for path in self.FILES:
            self.assertIn(
                "{0}.md".format(path.stem), index,
                "{0} missing from the archetype index".format(path.stem),
            )

    def test_index_maps_request_phrases(self):
        index = self.INDEX.read_text(encoding="utf-8").lower()
        # Phrases a user actually types, which is what the index is for.
        for phrase in ("landing page", "dashboard", "checkout", "booking",
                       "sign up", "admin", "analytics", "wallet"):
            self.assertIn(phrase, index, phrase)

    def test_every_archetype_is_in_the_reference_map(self):
        skill_md = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for path in list(self.FILES) + [self.INDEX]:
            relative = path.relative_to(SKILL).as_posix()
            self.assertIn(relative, skill_md, "{0} missing from reference map".format(relative))

    def test_no_em_dashes(self):
        offenders = [
            p.name for p in list(self.FILES) + [self.INDEX]
            if "—" in p.read_text(encoding="utf-8")
        ]
        self.assertEqual(offenders, [])


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
