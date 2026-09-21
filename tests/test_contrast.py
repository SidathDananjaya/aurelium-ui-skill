"""Tests for skills/aurelium-ui/scripts/contrast.py."""

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "skills" / "aurelium-ui" / "scripts" / "contrast.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


contrast = load("contrast", SCRIPT)


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = contrast.main(list(argv))
    return code, out.getvalue(), err.getvalue()


def ratio(foreground, background):
    return contrast.contrast_ratio(
        contrast.parse_color(foreground), contrast.parse_color(background)
    )


class ReferenceValueTests(unittest.TestCase):
    """Published WCAG values. These anchor the whole palette system."""

    def test_black_on_white_is_the_maximum(self):
        self.assertAlmostEqual(ratio("#000000", "#ffffff"), 21.0, places=2)

    def test_identical_colors_are_the_minimum(self):
        self.assertAlmostEqual(ratio("#4a7b2c", "#4a7b2c"), 1.0, places=6)

    def test_canonical_aa_boundary_grey(self):
        # #767676 on white is the standard example of a colour that just passes AA.
        self.assertAlmostEqual(ratio("#767676", "#ffffff"), 4.54, places=2)

    def test_canonical_aaa_boundary_grey(self):
        self.assertAlmostEqual(ratio("#595959", "#ffffff"), 7.00, places=2)

    def test_one_step_lighter_fails_aa(self):
        self.assertLess(ratio("#777777", "#ffffff"), contrast.AA_NORMAL)

    def test_order_does_not_matter(self):
        self.assertAlmostEqual(
            ratio("#123456", "#fedcba"), ratio("#fedcba", "#123456"), places=9
        )

    def test_luminance_endpoints(self):
        self.assertAlmostEqual(contrast.relative_luminance((255, 255, 255)), 1.0, places=9)
        self.assertAlmostEqual(contrast.relative_luminance((0, 0, 0)), 0.0, places=9)

    def test_green_dominates_luminance(self):
        green = contrast.relative_luminance((0, 255, 0))
        red = contrast.relative_luminance((255, 0, 0))
        blue = contrast.relative_luminance((0, 0, 255))
        self.assertGreater(green, red)
        self.assertGreater(red, blue)

    def test_low_channel_uses_the_linear_segment(self):
        # Values at or below 0.04045 use the divide-by-12.92 branch.
        self.assertAlmostEqual(contrast.channel_luminance(10), (10 / 255) / 12.92, places=12)


class ParsingTests(unittest.TestCase):
    def test_six_digit_hex(self):
        self.assertEqual(contrast.parse_color("#1a2b3c"), (26, 43, 60))

    def test_hex_without_hash(self):
        self.assertEqual(contrast.parse_color("1a2b3c"), (26, 43, 60))

    def test_three_digit_hex_expands(self):
        self.assertEqual(contrast.parse_color("#abc"), (170, 187, 204))

    def test_eight_digit_hex_drops_alpha(self):
        self.assertEqual(contrast.parse_color("#1a2b3cff"), (26, 43, 60))

    def test_uppercase_hex(self):
        self.assertEqual(contrast.parse_color("#FFAA00"), (255, 170, 0))

    def test_rgb_function(self):
        self.assertEqual(contrast.parse_color("rgb(12, 34, 56)"), (12, 34, 56))

    def test_rgba_drops_alpha(self):
        self.assertEqual(contrast.parse_color("rgba(12, 34, 56, 0.5)"), (12, 34, 56))

    def test_rejects_nonsense(self):
        for value in ("", "#12345", "chartreuse", "rgb(1,2)", "#gggggg"):
            with self.assertRaises(contrast.ColorError):
                contrast.parse_color(value)

    def test_rejects_out_of_range_channel(self):
        with self.assertRaises(contrast.ColorError):
            contrast.parse_color("rgb(300, 0, 0)")

    def test_to_hex_round_trips(self):
        self.assertEqual(contrast.to_hex(contrast.parse_color("#0a0b0c")), "#0a0b0c")


class RoundingTests(unittest.TestCase):
    def test_reported_ratio_never_overstates(self):
        # 4.549 must report as 4.54, not 4.55, so a near miss is never shown as a pass.
        self.assertEqual(contrast.round_ratio(4.549), 4.54)
        self.assertEqual(contrast.round_ratio(20.999), 20.99)


class CssTokenTests(unittest.TestCase):
    CSS = """
    :root {
      /* contrast-pairs: color-text:color-page, color-muted:color-page */
      --color-page: #ffffff;
      --color-text: #111111;
      --color-muted: #767676;
    }
    """

    def test_parses_custom_properties(self):
        properties = contrast.parse_custom_properties(self.CSS)
        self.assertEqual(properties["color-page"], "#ffffff")
        self.assertEqual(properties["color-text"], "#111111")

    def test_parses_declared_pairs(self):
        pairs = contrast.parse_declared_pairs(self.CSS)
        self.assertEqual(
            pairs, [("color-text", "color-page"), ("color-muted", "color-page")]
        )

    def test_all_pairs_pass(self):
        results = contrast.check_tokens(self.CSS, contrast.AA_NORMAL)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(result.passed for result in results))

    def test_failing_pair_is_reported(self):
        css = self.CSS.replace("#767676", "#bbbbbb")
        results = contrast.check_tokens(css, contrast.AA_NORMAL)
        self.assertFalse(results[1].passed)

    def test_unprefixed_names_resolve_to_color_prefix(self):
        css = """
        :root {
          /* contrast-pairs: text:page */
          --color-page: #ffffff;
          --color-text: #111111;
        }
        """
        results = contrast.check_tokens(css, contrast.AA_NORMAL)
        self.assertTrue(results[0].passed)

    def test_var_reference_is_followed(self):
        css = """
        :root {
          /* contrast-pairs: color-ink:color-page */
          --color-page: #ffffff;
          --base-ink: #111111;
          --color-ink: var(--base-ink);
        }
        """
        results = contrast.check_tokens(css, contrast.AA_NORMAL)
        self.assertTrue(results[0].passed)

    def test_var_fallback_is_used_when_target_is_missing(self):
        css = """
        :root {
          /* contrast-pairs: color-ink:color-page */
          --color-page: #ffffff;
          --color-ink: var(--not-defined, #111111);
        }
        """
        results = contrast.check_tokens(css, contrast.AA_NORMAL)
        self.assertTrue(results[0].passed)

    def test_undefined_property_is_an_error_not_a_crash(self):
        css = """
        :root {
          /* contrast-pairs: color-ghost:color-page */
          --color-page: #ffffff;
        }
        """
        results = contrast.check_tokens(css, contrast.AA_NORMAL)
        self.assertFalse(results[0].passed)
        self.assertIn("undefined", results[0].error)

    def test_circular_var_reference_terminates(self):
        css = """
        :root {
          /* contrast-pairs: color-a:color-b */
          --color-a: var(--color-b);
          --color-b: var(--color-a);
        }
        """
        results = contrast.check_tokens(css, contrast.AA_NORMAL)
        self.assertFalse(results[0].passed)

    def test_malformed_pair_raises(self):
        with self.assertRaises(contrast.ColorError):
            contrast.parse_declared_pairs("/* contrast-pairs: textpage */")


class CommandLineTests(unittest.TestCase):
    def test_passing_pair_exits_zero(self):
        code, out, _ = run("--pair", "#111111", "#ffffff")
        self.assertEqual(code, 0)
        self.assertIn("pass", out)

    def test_failing_pair_exits_one(self):
        code, _, _ = run("--pair", "#cccccc", "#ffffff")
        self.assertEqual(code, 1)

    def test_bad_color_exits_two(self):
        code, _, err = run("--pair", "not-a-color", "#ffffff")
        self.assertEqual(code, 2)
        self.assertIn("cannot parse", err)

    def test_json_pair_output(self):
        code, out, _ = run("--pair", "#767676", "#ffffff", "--json")
        payload = json.loads(out)
        self.assertEqual(code, 0)
        self.assertEqual(payload["ratio"], 4.54)
        self.assertTrue(payload["grades"]["aa_normal"])
        self.assertFalse(payload["grades"]["aaa_normal"])

    def test_missing_file_exits_two(self):
        code, _, err = run("--tokens", str(REPO_ROOT / "nope.css"))
        self.assertEqual(code, 2)
        self.assertIn("no such file", err)

    def test_file_without_pairs_comment_exits_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tokens.css"
            with open(path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(":root { --color-page: #fff; }")
            code, _, err = run("--tokens", str(path))
        self.assertEqual(code, 2)
        self.assertIn("no contrast-pairs", err)

    def test_token_file_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tokens.css"
            with open(path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(CssTokenTests.CSS)
            code, out, _ = run("--tokens", str(path))
        self.assertEqual(code, 0)
        self.assertIn("OK", out)


if __name__ == "__main__":
    unittest.main()
