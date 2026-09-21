"""Tests for tokens.py and type_scale.py, and for the shipped direction files."""

import importlib.util
import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "aurelium-ui"
DIRECTIONS_DIR = SKILL / "assets" / "directions"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tokens = load("tokens", SKILL / "scripts" / "tokens.py")
type_scale = load("type_scale", SKILL / "scripts" / "type_scale.py")
contrast = load("contrast_for_tokens", SKILL / "scripts" / "contrast.py")

DIRECTION_NAMES = tokens.available_directions(DIRECTIONS_DIR)


def run(module, *argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = module.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class DirectionFileTests(unittest.TestCase):
    def test_five_directions_ship(self):
        self.assertEqual(len(DIRECTION_NAMES), 5, DIRECTION_NAMES)

    def test_schema_file_is_not_treated_as_a_direction(self):
        self.assertNotIn("_schema", DIRECTION_NAMES)

    def test_every_direction_has_both_themes_with_matching_keys(self):
        for name in DIRECTION_NAMES:
            data = tokens.load_direction(name, DIRECTIONS_DIR)
            light = set(data["colors"]["light"])
            dark = set(data["colors"]["dark"])
            self.assertEqual(light, dark, "{0} themes differ".format(name))

    def test_every_direction_name_matches_its_filename(self):
        for name in DIRECTION_NAMES:
            data = tokens.load_direction(name, DIRECTIONS_DIR)
            self.assertEqual(data["name"], name)

    def test_every_color_is_six_digit_hex(self):
        for name in DIRECTION_NAMES:
            data = tokens.load_direction(name, DIRECTIONS_DIR)
            for theme in ("light", "dark"):
                for token, value in data["colors"][theme].items():
                    self.assertRegex(
                        value,
                        r"^#[0-9a-f]{6}$",
                        "{0}/{1}/{2} is {3}".format(name, theme, token, value),
                    )

    def test_every_declared_contrast_pair_passes(self):
        for name in DIRECTION_NAMES:
            data = tokens.load_direction(name, DIRECTIONS_DIR)
            for pair in data["contrast_pairs"]:
                palette = data["colors"][pair["theme"]]
                ratio = contrast.contrast_ratio(
                    contrast.parse_color(palette[pair["fg"]]),
                    contrast.parse_color(palette[pair["bg"]]),
                )
                self.assertGreaterEqual(
                    ratio,
                    pair.get("min", 4.5),
                    "{0} {1}: {2} on {3} is {4:.2f}".format(
                        name, pair["theme"], pair["fg"], pair["bg"], ratio
                    ),
                )

    def test_body_base_size_is_never_below_15(self):
        for name in DIRECTION_NAMES:
            data = tokens.load_direction(name, DIRECTIONS_DIR)
            self.assertGreaterEqual(data["type"]["base"], 15, name)

    def test_spacing_base_is_the_four_pixel_grid(self):
        for name in DIRECTION_NAMES:
            data = tokens.load_direction(name, DIRECTIONS_DIR)
            self.assertEqual(data["spacing"]["base"], 4, name)

    def test_at_most_three_elevation_levels(self):
        for name in DIRECTION_NAMES:
            data = tokens.load_direction(name, DIRECTIONS_DIR)
            self.assertLessEqual(len(data["shadows"]), 3, name)

    def test_every_direction_has_a_markdown_file(self):
        for name in DIRECTION_NAMES:
            path = SKILL / "references" / "directions" / "{0}.md".format(name)
            self.assertTrue(path.is_file(), "missing {0}".format(path.name))

    def test_index_links_every_direction(self):
        index = (SKILL / "references" / "directions" / "index.md").read_text(
            encoding="utf-8"
        )
        for name in DIRECTION_NAMES:
            self.assertIn("{0}.md".format(name), index)


class LoadingTests(unittest.TestCase):
    def test_unknown_direction_raises_with_a_helpful_message(self):
        with self.assertRaises(tokens.TokenError) as caught:
            tokens.load_direction("does-not-exist", DIRECTIONS_DIR)
        self.assertIn("Available", str(caught.exception))

    def test_dial_range_is_enforced(self):
        for value in (0, 11, -1):
            with self.assertRaises(tokens.TokenError):
                tokens.check_dial("--density", value)

    def test_dial_bounds_are_inclusive(self):
        self.assertEqual(tokens.check_dial("--density", 1), 1)
        self.assertEqual(tokens.check_dial("--density", 10), 10)


class DialTests(unittest.TestCase):
    def setUp(self):
        self.direction = tokens.load_direction("obsidian", DIRECTIONS_DIR)

    def build(self, opulence=4, density=5, motion=4):
        return tokens.build_tokens(self.direction, opulence, density, motion)

    def test_density_compresses_spacing(self):
        spacious = self.build(density=2)["spacing"]["5"]
        balanced = self.build(density=5)["spacing"]["5"]
        dense = self.build(density=9)["spacing"]["5"]
        self.assertGreater(float(spacious[:-3]), float(balanced[:-3]))
        self.assertGreater(float(balanced[:-3]), float(dense[:-3]))

    def test_density_changes_the_type_base(self):
        self.assertGreater(
            self.build(density=2)["type"]["base"], self.build(density=9)["type"]["base"]
        )

    def test_opulence_controls_elevation_count(self):
        self.assertEqual(len(self.build(opulence=1)["shadows"]), 1)
        self.assertEqual(len(self.build(opulence=5)["shadows"]), 2)
        self.assertEqual(len(self.build(opulence=9)["shadows"]), 3)

    def test_motion_controls_token_count(self):
        self.assertEqual(len(self.build(motion=1)["motion"]["durations"]), 1)
        self.assertEqual(len(self.build(motion=5)["motion"]["durations"]), 2)
        self.assertEqual(len(self.build(motion=9)["motion"]["durations"]), 3)

    def test_spacing_stays_on_the_grid_at_every_density(self):
        for density in range(1, 11):
            for value in self.build(density=density)["spacing"].values():
                pixels = float(value[:-3]) * 16
                self.assertAlmostEqual(
                    pixels % 4, 0, places=6, msg="{0} is off grid".format(value)
                )


class CssOutputTests(unittest.TestCase):
    def test_every_direction_and_theme_produces_balanced_css(self):
        for name in DIRECTION_NAMES:
            for theme in ("light", "dark", "auto"):
                code, out, err = run(
                    tokens, "--direction", name, "--theme", theme, "--format", "css"
                )
                self.assertEqual(code, 0, err)
                self.assertEqual(
                    out.count("{"), out.count("}"), "{0}/{1}".format(name, theme)
                )
                self.assertIn("--color-page", out)

    def test_auto_theme_emits_both_schemes(self):
        _, out, _ = run(tokens, "--direction", "obsidian", "--theme", "auto")
        self.assertIn("prefers-color-scheme: dark", out)
        self.assertIn('[data-theme="dark"]', out)

    def test_reduced_motion_block_is_always_present(self):
        for name in DIRECTION_NAMES:
            _, out, _ = run(tokens, "--direction", name)
            self.assertIn("prefers-reduced-motion: reduce", out)

    def test_generated_css_passes_its_own_contrast_check(self):
        for name in DIRECTION_NAMES:
            for theme in ("light", "dark"):
                _, css, _ = run(tokens, "--direction", name, "--theme", theme)
                results = contrast.check_tokens(css, contrast.AA_NORMAL)
                self.assertTrue(results, "{0}/{1} declared no pairs".format(name, theme))
                for result in results:
                    self.assertTrue(
                        result.passed,
                        "{0}/{1}: {2}".format(name, theme, result),
                    )

    def test_json_output_is_valid(self):
        code, out, _ = run(tokens, "--direction", "quiet-luxury", "--format", "json")
        payload = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(payload["direction"], "quiet-luxury")

    def test_tailwind_output_uses_the_v4_theme_directive(self):
        code, out, _ = run(tokens, "--direction", "obsidian", "--format", "tailwind")
        self.assertEqual(code, 0)
        # Tailwind v4 is CSS first. A JavaScript config would be the v3 shape.
        self.assertIn("@theme inline", out)
        self.assertNotIn("module.exports", out)

    def test_tailwind_theme_layer_references_rather_than_copies(self):
        # Without "inline" Tailwind copies the value and freezes the light
        # palette, so theme switching silently stops working.
        _, out, _ = run(tokens, "--direction", "obsidian", "--format", "tailwind")
        layer = out.split("@theme inline", 1)[1]
        self.assertIn("--color-page: var(--au-color-page);", layer)
        self.assertIn("--spacing-4: var(--au-space-4);", layer)
        self.assertIn("--radius-md: var(--au-radius-md);", layer)

    def test_tailwind_raw_tokens_are_namespaced(self):
        # The au- prefix keeps Tailwind's own --color-* namespace free.
        _, out, _ = run(tokens, "--direction", "obsidian", "--format", "tailwind")
        root = out.split("@theme inline", 1)[0]
        self.assertIn("--au-color-page:", root)
        self.assertNotIn("\n  --color-page:", root)

    def test_tailwind_output_still_carries_both_themes(self):
        _, out, _ = run(tokens, "--direction", "obsidian", "--format", "tailwind")
        self.assertIn("prefers-color-scheme: dark", out)
        self.assertIn('[data-theme="dark"]', out)

    def test_tailwind_output_passes_its_own_contrast_check(self):
        for name in DIRECTION_NAMES:
            _, out, _ = run(tokens, "--direction", name, "--format", "tailwind")
            results = contrast.check_tokens(out, contrast.AA_NORMAL)
            self.assertTrue(results, "{0} declared no pairs".format(name))
            for result in results:
                self.assertTrue(result.passed, "{0}: {1}".format(name, result))

    def test_css_format_is_unaffected_by_the_prefix_change(self):
        _, out, _ = run(tokens, "--direction", "obsidian", "--format", "css")
        self.assertIn("--color-page:", out)
        self.assertNotIn("--au-", out)

    def test_list_prints_every_direction(self):
        code, out, _ = run(tokens, "--list")
        self.assertEqual(code, 0)
        for name in DIRECTION_NAMES:
            self.assertIn(name, out)

    def test_missing_direction_exits_two(self):
        code, _, err = run(tokens, "--format", "css")
        self.assertEqual(code, 2)
        self.assertIn("--direction is required", err)

    def test_out_of_range_dial_exits_two(self):
        code, _, err = run(tokens, "--direction", "obsidian", "--density", "42")
        self.assertEqual(code, 2)
        self.assertIn("between 1 and 10", err)


class TypeScaleTests(unittest.TestCase):
    def test_base_step_equals_one_rem(self):
        scale = type_scale.build_scale(16, 1.25, 0, 0)
        self.assertEqual(scale[0]["rem"], 1.0)
        self.assertEqual(scale[0]["px"], 16.0)

    def test_ratio_is_applied_per_step(self):
        scale = {entry["step"]: entry for entry in type_scale.build_scale(16, 1.25, -1, 2)}
        self.assertAlmostEqual(scale[1]["px"], 20.0, places=2)
        self.assertAlmostEqual(scale[2]["px"], 25.0, places=2)
        self.assertAlmostEqual(scale[-1]["px"], 12.8, places=2)

    def test_line_height_falls_as_size_rises(self):
        body = type_scale.line_height_for(16)
        heading = type_scale.line_height_for(30)
        display = type_scale.line_height_for(56)
        self.assertGreater(body, heading)
        self.assertGreater(heading, display)

    def test_tracking_tightens_as_size_rises(self):
        self.assertGreater(type_scale.tracking_for(12), 0)
        self.assertEqual(type_scale.tracking_for(16), 0.0)
        self.assertLess(type_scale.tracking_for(48), 0)

    def test_step_names_are_stable(self):
        scale = type_scale.build_scale(16, 1.25, -2, 6)
        names = [entry["name"] for entry in scale]
        self.assertEqual(names[0], "2xs")
        self.assertEqual(names[2], "base")
        self.assertEqual(names[-1], "5xl")

    def test_documented_negative_range_is_accepted(self):
        # "--steps -2..6" is the documented spelling and must not be read as a flag.
        code, out, err = run(type_scale, "--base", "16", "--ratio", "1.25", "--steps", "-2..6")
        self.assertEqual(code, 0, err)
        self.assertIn("2xs", out)

    def test_equals_spelling_also_works(self):
        code, out, err = run(type_scale, "--steps=-1..1")
        self.assertEqual(code, 0, err)
        self.assertIn("base", out)

    def test_reversed_range_is_rejected(self):
        with self.assertRaises(Exception):
            type_scale.parse_steps("6..-2")

    def test_malformed_range_is_rejected(self):
        with self.assertRaises(Exception):
            type_scale.parse_steps("two to six")

    def test_ratio_at_or_below_one_exits_two(self):
        code, _, err = run(type_scale, "--ratio", "1.0")
        self.assertEqual(code, 2)
        self.assertIn("above 1.0", err)

    def test_base_at_or_below_zero_exits_two(self):
        code, _, err = run(type_scale, "--base", "0")
        self.assertEqual(code, 2)

    def test_css_output_declares_three_token_families(self):
        code, out, _ = run(type_scale, "--format", "css")
        self.assertEqual(code, 0)
        self.assertIn("--text-base", out)
        self.assertIn("--leading-base", out)
        self.assertIn("--tracking-base", out)

    def test_json_output_is_valid(self):
        code, out, _ = run(type_scale, "--json")
        payload = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(payload["base"], 16.0)

    def test_tokens_and_type_scale_agree_on_line_height(self):
        # The two scripts must not drift apart on the size bands.
        for pixels in (10, 14, 16, 20, 24, 30, 36, 48, 64):
            self.assertEqual(
                tokens.line_height_for(pixels), type_scale.line_height_for(pixels)
            )
            self.assertEqual(
                tokens.tracking_for(pixels), type_scale.tracking_for(pixels)
            )


if __name__ == "__main__":
    unittest.main()
