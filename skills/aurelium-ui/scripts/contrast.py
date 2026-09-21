#!/usr/bin/env python3
"""WCAG contrast checking for color pairs and token files.

Two modes:

  Pair mode, checks one foreground against one background::

      contrast.py --pair "#111111" "#f5f2eb"

  Token mode, parses CSS custom properties and checks every pairing named in a
  ``contrast-pairs`` comment::

      /* contrast-pairs: text:page, text-muted:page, accent-fg:accent */

      contrast.py --tokens tokens.css

Relative luminance and contrast ratio follow the WCAG 2.x definitions exactly.
Standard library only. Exit code 0 when every checked pair passes, 1 when any
pair fails, and 2 for a usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

# WCAG 2.2 thresholds.
AA_NORMAL = 4.5
AA_LARGE = 3.0
AAA_NORMAL = 7.0
AAA_LARGE = 4.5
# Non text contrast, for UI component boundaries and meaningful graphics.
AA_NON_TEXT = 3.0

HEX_PATTERN = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
RGB_PATTERN = re.compile(
    r"^rgba?\(\s*(\d+)\s*[,\s]\s*(\d+)\s*[,\s]\s*(\d+)\s*(?:[,/]\s*[\d.%]+\s*)?\)$",
    re.IGNORECASE,
)
CUSTOM_PROPERTY_PATTERN = re.compile(r"--([A-Za-z0-9_-]+)\s*:\s*([^;]+);")
VAR_REFERENCE_PATTERN = re.compile(r"var\(\s*--([A-Za-z0-9_-]+)\s*(?:,\s*([^)]+))?\)")
CONTRAST_PAIRS_PATTERN = re.compile(r"contrast-pairs\s*:\s*([^*]+)", re.IGNORECASE)

MAX_VAR_DEPTH = 10


class ColorError(ValueError):
    """Raised when a color string cannot be understood."""


# ---------------------------------------------------------------------------
# Color parsing and WCAG math
# ---------------------------------------------------------------------------


def parse_color(value: str) -> Tuple[int, int, int]:
    """Parse a hex or rgb() color into an 8 bit sRGB triple.

    Alpha is accepted and discarded. Contrast is undefined against a
    translucent color, so the caller is responsible for compositing first.
    """
    text = value.strip()

    match = HEX_PATTERN.match(text)
    if match:
        digits = match.group(1)
        if len(digits) in (3, 4):
            digits = "".join(char * 2 for char in digits)
        return (
            int(digits[0:2], 16),
            int(digits[2:4], 16),
            int(digits[4:6], 16),
        )

    match = RGB_PATTERN.match(text)
    if match:
        channels = tuple(int(match.group(index)) for index in (1, 2, 3))
        for channel in channels:
            if not 0 <= channel <= 255:
                raise ColorError("channel out of range in '{0}'".format(value))
        return channels  # type: ignore[return-value]

    raise ColorError(
        "cannot parse '{0}'. Use hex such as #1a1a1a, or rgb(26, 26, 26)".format(value)
    )


def to_hex(rgb: Sequence[int]) -> str:
    return "#{0:02x}{1:02x}{2:02x}".format(rgb[0], rgb[1], rgb[2])


def channel_luminance(channel_8bit: int) -> float:
    """Linearise one sRGB channel, per the WCAG definition."""
    srgb = channel_8bit / 255.0
    if srgb <= 0.04045:
        return srgb / 12.92
    return ((srgb + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb: Sequence[int]) -> float:
    """WCAG relative luminance: 0.2126 R + 0.7152 G + 0.0722 B, linearised."""
    red, green, blue = (channel_luminance(channel) for channel in rgb[:3])
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground: Sequence[int], background: Sequence[int]) -> float:
    """Contrast ratio between two colors, from 1.0 to 21.0."""
    light = relative_luminance(foreground)
    dark = relative_luminance(background)
    if dark > light:
        light, dark = dark, light
    return (light + 0.05) / (dark + 0.05)


def grade(ratio: float) -> Dict[str, bool]:
    """Report which WCAG thresholds a ratio clears."""
    return {
        "aa_normal": ratio >= AA_NORMAL,
        "aa_large": ratio >= AA_LARGE,
        "aaa_normal": ratio >= AAA_NORMAL,
        "aaa_large": ratio >= AAA_LARGE,
        "non_text": ratio >= AA_NON_TEXT,
    }


def round_ratio(ratio: float) -> float:
    """Round down to two places, so a reported value never overstates."""
    return int(ratio * 100) / 100.0


# ---------------------------------------------------------------------------
# CSS token parsing
# ---------------------------------------------------------------------------


def parse_custom_properties(css: str) -> Dict[str, str]:
    """Collect every custom property declaration in the file.

    A property declared more than once keeps its last value, which matches the
    cascade for declarations at equal specificity.
    """
    return {
        name: value.strip()
        for name, value in CUSTOM_PROPERTY_PATTERN.findall(css)
    }


def resolve_value(name: str, properties: Dict[str, str], depth: int = 0) -> Optional[str]:
    """Resolve a custom property, following var() references and fallbacks.

    A name that is not declared is retried with a ``color-`` prefix, so both
    ``text:page`` and ``color-text:color-page`` work in a pairs comment.
    """
    if depth > MAX_VAR_DEPTH:
        return None

    if name not in properties:
        prefixed = "color-{0}".format(name)
        if not name.startswith("color-") and prefixed in properties:
            name = prefixed
        else:
            return None

    value = properties[name].strip()
    match = VAR_REFERENCE_PATTERN.match(value)
    if not match:
        return value

    referenced = resolve_value(match.group(1), properties, depth + 1)
    if referenced is not None:
        return referenced

    fallback = match.group(2)
    return fallback.strip() if fallback else None


def parse_pair_list(text: str) -> List[Tuple[str, str]]:
    """Parse one comment's worth of 'fg:bg, fg:bg' entries."""
    pairs: List[Tuple[str, str]] = []
    for entry in text.replace("\n", " ").split(","):
        entry = entry.strip().rstrip("/").strip()
        if not entry:
            continue
        if ":" not in entry:
            raise ColorError(
                "malformed contrast pair '{0}', expected 'foreground:background'".format(
                    entry
                )
            )
        foreground, _, background = entry.partition(":")
        pairs.append((foreground.strip(), background.strip()))
    return pairs


def parse_declared_pairs(css: str) -> List[Tuple[str, str]]:
    """Read every 'contrast-pairs' comment into (foreground, background) names."""
    pairs: List[Tuple[str, str]] = []
    for block in CONTRAST_PAIRS_PATTERN.findall(css):
        pairs.extend(parse_pair_list(block))
    return pairs


def enclosing_block(css: str, index: int) -> str:
    """Return the text of the rule block containing the character at ``index``.

    A stylesheet that declares light and dark palettes flattens into a single
    property map, so the last theme in the file would silently be checked
    twice. Scoping each pairs comment to its own block checks what the comment
    actually refers to.
    """
    depth = 0
    start = -1
    for position in range(index, -1, -1):
        char = css[position]
        if char == "}":
            depth += 1
        elif char == "{":
            if depth == 0:
                start = position + 1
                break
            depth -= 1
    if start == -1:
        return css

    depth = 0
    for position in range(start, len(css)):
        char = css[position]
        if char == "{":
            depth += 1
        elif char == "}":
            if depth == 0:
                return css[start:position]
            depth -= 1
    return css[start:]


# ---------------------------------------------------------------------------
# Checking
# ---------------------------------------------------------------------------


class Result:
    """One checked pair."""

    def __init__(
        self,
        foreground_name: str,
        background_name: str,
        foreground: Optional[Tuple[int, int, int]],
        background: Optional[Tuple[int, int, int]],
        threshold: float,
        error: Optional[str] = None,
    ) -> None:
        self.foreground_name = foreground_name
        self.background_name = background_name
        self.foreground = foreground
        self.background = background
        self.threshold = threshold
        self.error = error
        self.ratio = (
            contrast_ratio(foreground, background)
            if foreground is not None and background is not None
            else 0.0
        )

    @property
    def passed(self) -> bool:
        return self.error is None and self.ratio >= self.threshold

    def as_dict(self) -> Dict[str, object]:
        payload: Dict[str, object] = {
            "foreground": self.foreground_name,
            "background": self.background_name,
            "threshold": self.threshold,
            "pass": self.passed,
        }
        if self.error:
            payload["error"] = self.error
        else:
            payload["ratio"] = round_ratio(self.ratio)
            payload["foreground_hex"] = to_hex(self.foreground or (0, 0, 0))
            payload["background_hex"] = to_hex(self.background or (0, 0, 0))
            payload["grades"] = grade(self.ratio)
        return payload

    def __str__(self) -> str:
        if self.error:
            return "FAIL  {0} on {1}: {2}".format(
                self.foreground_name, self.background_name, self.error
            )
        return "{0}  {1} on {2}: {3:.2f}:1 (needs {4}:1)".format(
            "PASS " if self.passed else "FAIL ",
            self.foreground_name,
            self.background_name,
            round_ratio(self.ratio),
            self.threshold,
        )


def check_tokens(css: str, threshold: float) -> List[Result]:
    """Check every pair declared in the stylesheet's contrast-pairs comments.

    Each comment is resolved against its own rule block first, then against the
    whole stylesheet, so a file carrying both a light and a dark palette is
    checked once per theme rather than twice against whichever came last.
    """
    global_properties = parse_custom_properties(css)
    results: List[Result] = []

    scoped: List[Tuple[str, str, Dict[str, str]]] = []
    for match in CONTRAST_PAIRS_PATTERN.finditer(css):
        block = enclosing_block(css, match.start())
        block_properties = parse_custom_properties(block)
        for foreground_name, background_name in parse_pair_list(match.group(1)):
            scoped.append((foreground_name, background_name, block_properties))

    for foreground_name, background_name, block_properties in scoped:
        properties = dict(global_properties)
        properties.update(block_properties)

        foreground_value = resolve_value(foreground_name, properties)
        background_value = resolve_value(background_name, properties)

        missing = [
            name
            for name, value in (
                (foreground_name, foreground_value),
                (background_name, background_value),
            )
            if value is None
        ]
        if missing:
            results.append(
                Result(
                    foreground_name,
                    background_name,
                    None,
                    None,
                    threshold,
                    "undefined custom property: {0}".format(", ".join(missing)),
                )
            )
            continue

        try:
            foreground = parse_color(foreground_value or "")
            background = parse_color(background_value or "")
        except ColorError as exc:
            results.append(
                Result(foreground_name, background_name, None, None, threshold, str(exc))
            )
            continue

        results.append(
            Result(foreground_name, background_name, foreground, background, threshold)
        )

    return results


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="contrast.py",
        description="Check WCAG contrast for a color pair or a token file.",
        epilog=(
            "Examples:\n"
            '  contrast.py --pair "#111111" "#f5f2eb"\n'
            "  contrast.py --tokens tokens.css --json\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--pair",
        nargs=2,
        metavar=("FOREGROUND", "BACKGROUND"),
        help="Two colors as hex or rgb().",
    )
    mode.add_argument(
        "--tokens",
        type=Path,
        metavar="PATH",
        help="A CSS file declaring custom properties and contrast-pairs comments.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=AA_NORMAL,
        help="Minimum ratio for token mode. Default {0} for AA body text.".format(
            AA_NORMAL
        ),
    )
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Emit machine readable results.",
    )
    return parser


def report_pair(foreground_raw: str, background_raw: str, as_json: bool) -> int:
    try:
        foreground = parse_color(foreground_raw)
        background = parse_color(background_raw)
    except ColorError as exc:
        print("error: {0}".format(exc), file=sys.stderr)
        return 2

    ratio = contrast_ratio(foreground, background)
    grades = grade(ratio)

    if as_json:
        print(
            json.dumps(
                {
                    "foreground": to_hex(foreground),
                    "background": to_hex(background),
                    "ratio": round_ratio(ratio),
                    "grades": grades,
                },
                indent=2,
            )
        )
    else:
        print(
            "{0} on {1}: {2:.2f}:1".format(
                to_hex(foreground), to_hex(background), round_ratio(ratio)
            )
        )
        print("  AA  normal text (4.5:1)  {0}".format("pass" if grades["aa_normal"] else "FAIL"))
        print("  AA  large text  (3.0:1)  {0}".format("pass" if grades["aa_large"] else "FAIL"))
        print("  AAA normal text (7.0:1)  {0}".format("pass" if grades["aaa_normal"] else "FAIL"))
        print("  AAA large text  (4.5:1)  {0}".format("pass" if grades["aaa_large"] else "FAIL"))
        print("  Non text        (3.0:1)  {0}".format("pass" if grades["non_text"] else "FAIL"))

    return 0 if grades["aa_normal"] else 1


def report_tokens(path: Path, threshold: float, as_json: bool) -> int:
    if not path.is_file():
        print("error: no such file: {0}".format(path), file=sys.stderr)
        return 2

    css = path.read_text(encoding="utf-8")
    try:
        results = check_tokens(css, threshold)
    except ColorError as exc:
        print("error: {0}".format(exc), file=sys.stderr)
        return 2

    if not results:
        print(
            "error: no contrast-pairs comment found in {0}".format(path),
            file=sys.stderr,
        )
        return 2

    failures = [result for result in results if not result.passed]

    if as_json:
        print(
            json.dumps(
                {
                    "file": path.as_posix(),
                    "threshold": threshold,
                    "ok": not failures,
                    "results": [result.as_dict() for result in results],
                },
                indent=2,
            )
        )
    else:
        for result in results:
            stream = sys.stderr if not result.passed else sys.stdout
            print(str(result), file=stream)
        if failures:
            print(
                "FAIL: {0} of {1} pairs below {2}:1.".format(
                    len(failures), len(results), threshold
                ),
                file=sys.stderr,
            )
        else:
            print("OK: {0} pairs pass {1}:1.".format(len(results), threshold))

    return 1 if failures else 0


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    if args.pair:
        return report_pair(args.pair[0], args.pair[1], args.as_json)
    return report_tokens(args.tokens, args.threshold, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
