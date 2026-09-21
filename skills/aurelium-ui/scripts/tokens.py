#!/usr/bin/env python3
"""Turn a design direction plus dial values into design tokens.

Example::

    tokens.py --direction obsidian --opulence 4 --density 5 --motion 4 \\
        --theme auto --format css

Dials change the output:

  DENSITY  scales the spacing multiplier, the type base and the scale ratio.
  OPULENCE controls how many shadow levels and texture tokens are emitted.
  MOTION   controls which duration and easing tokens exist.

Standard library only. Exit code 0 on success, 2 for a usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DIRECTIONS_DIR = Path(__file__).resolve().parent.parent / "assets" / "directions"

DIAL_MIN = 1
DIAL_MAX = 10
DIAL_DEFAULT_OPULENCE = 4
DIAL_DEFAULT_DENSITY = 5
DIAL_DEFAULT_MOTION = 4

# Step index to token name, matching type_scale.py.
STEP_NAMES = {
    -3: "3xs",
    -2: "2xs",
    -1: "xs",
    0: "base",
    1: "lg",
    2: "xl",
    3: "2xl",
    4: "3xl",
    5: "4xl",
    6: "5xl",
    7: "6xl",
    8: "7xl",
}

SPACING_STEPS = [
    ("0", 0),
    ("1", 4),
    ("2", 8),
    ("3", 12),
    ("4", 16),
    ("5", 24),
    ("6", 32),
    ("7", 40),
    ("8", 48),
    ("9", 64),
    ("10", 80),
    ("11", 96),
    ("12", 128),
    ("13", 160),
]


class TokenError(Exception):
    """Raised when a direction cannot be loaded or a dial is out of range."""


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


def available_directions(directory: Path = DIRECTIONS_DIR) -> List[str]:
    if not directory.is_dir():
        return []
    return sorted(
        path.stem for path in directory.glob("*.json") if not path.name.startswith("_")
    )


def load_direction(name: str, directory: Path = DIRECTIONS_DIR) -> Dict[str, object]:
    path = directory / "{0}.json".format(name)
    if not path.is_file():
        known = ", ".join(available_directions(directory)) or "none found"
        raise TokenError(
            "unknown direction '{0}'. Available: {1}".format(name, known)
        )
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise TokenError("invalid JSON in {0}: {1}".format(path.name, exc))


# ---------------------------------------------------------------------------
# Dial effects
# ---------------------------------------------------------------------------


def density_multiplier(density: int) -> float:
    """Spacing multiplier. Dense tools compress, editorial layouts expand."""
    if density <= 3:
        return 1.25
    if density <= 6:
        return 1.0
    return 0.75


def density_type_adjust(density: int, base: float, ratio: float) -> Tuple[float, float]:
    """Dense layouts drop the base size a little and flatten the scale."""
    if density <= 3:
        return base + 1.0, min(ratio + 0.083, 1.5)
    if density <= 6:
        return base, ratio
    return max(base - 1.0, 15.0), max(ratio - 0.05, 1.15)


def opulence_shadow_levels(opulence: int) -> List[str]:
    """How many elevation levels the palette exposes."""
    if opulence <= 2:
        return ["e1"]
    if opulence <= 6:
        return ["e1", "e2"]
    return ["e1", "e2", "e3"]


def motion_duration_keys(motion: int) -> List[str]:
    """Which duration tokens exist at this motion level."""
    if motion <= 2:
        return ["fast"]
    if motion <= 6:
        return ["fast", "base"]
    return ["fast", "base", "slow"]


def motion_easing_keys(motion: int) -> List[str]:
    if motion <= 2:
        return ["standard"]
    if motion <= 6:
        return ["standard", "exit"]
    return ["standard", "exit", "entrance"]


def check_dial(name: str, value: int) -> int:
    if not DIAL_MIN <= value <= DIAL_MAX:
        raise TokenError(
            "{0} must be between {1} and {2}, got {3}".format(
                name, DIAL_MIN, DIAL_MAX, value
            )
        )
    return value


# ---------------------------------------------------------------------------
# Token construction
# ---------------------------------------------------------------------------


def round_to(value: float, places: int) -> float:
    quantum = 10 ** places
    return int(round(value * quantum)) / quantum


def step_name(index: int) -> str:
    if index in STEP_NAMES:
        return STEP_NAMES[index]
    return "step{0}{1}".format("m" if index < 0 else "p", abs(index))


def parse_steps(value: str) -> Tuple[int, int]:
    first, _, last = value.partition("..")
    try:
        return int(first), int(last)
    except ValueError:
        raise TokenError("malformed step range '{0}', expected -2..6".format(value))


def build_tokens(
    direction: Dict[str, object],
    opulence: int,
    density: int,
    motion: int,
) -> Dict[str, object]:
    """Assemble every token group for the given direction and dials."""
    type_spec = dict(direction.get("type") or {})
    spacing_spec = dict(direction.get("spacing") or {})

    base = float(type_spec.get("base", 16))
    ratio = float(type_spec.get("ratio", 1.25))
    base, ratio = density_type_adjust(density, base, ratio)

    first, last = parse_steps(str(type_spec.get("steps", "-2..6")))

    type_tokens = {}
    leading_tokens = {}
    tracking_tokens = {}
    for index in range(first, last + 1):
        pixels = base * (ratio ** index)
        name = step_name(index)
        type_tokens[name] = "{0}rem".format(round_to(pixels / base, 3))
        leading_tokens[name] = line_height_for(pixels)
        tracking_tokens[name] = "{0}em".format(tracking_for(pixels))

    multiplier = float(spacing_spec.get("multiplier", 1.0)) * density_multiplier(density)
    grid = float(spacing_spec.get("base", 4))
    spacing_tokens = {}
    for name, pixels in SPACING_STEPS:
        scaled = pixels * multiplier
        # Keep every value on the grid.
        snapped = round(scaled / grid) * grid if scaled else 0
        spacing_tokens[name] = "{0}rem".format(round_to(snapped / 16.0, 4))

    shadows = dict(direction.get("shadows") or {})
    shadow_tokens = {
        key: shadows[key] for key in opulence_shadow_levels(opulence) if key in shadows
    }

    motion_spec = dict(direction.get("motion") or {})
    durations = dict(motion_spec.get("durations") or {})
    easings = dict(motion_spec.get("easings") or {})
    duration_tokens = {
        key: durations[key] for key in motion_duration_keys(motion) if key in durations
    }
    easing_tokens = {
        key: easings[key] for key in motion_easing_keys(motion) if key in easings
    }

    return {
        "direction": direction.get("name"),
        "label": direction.get("label"),
        "dials": {"opulence": opulence, "density": density, "motion": motion},
        "colors": direction.get("colors") or {},
        "fonts": direction.get("fonts") or {},
        "type": {"base": base, "ratio": round_to(ratio, 4), "sizes": type_tokens},
        "leading": leading_tokens,
        "tracking": tracking_tokens,
        "spacing": spacing_tokens,
        "radii": direction.get("radii") or {},
        "shadows": shadow_tokens,
        "borders": direction.get("borders") or {},
        "motion": {"durations": duration_tokens, "easings": easing_tokens},
        "contrast_pairs": direction.get("contrast_pairs") or [],
    }


def line_height_for(pixels: float) -> float:
    if pixels >= 36:
        return 1.05
    if pixels >= 28:
        return 1.15
    if pixels >= 20:
        return 1.25
    if pixels >= 15:
        return 1.55
    return 1.45


def tracking_for(pixels: float) -> float:
    if pixels >= 40:
        return -0.03
    if pixels >= 32:
        return -0.025
    if pixels >= 24:
        return -0.015
    if pixels >= 20:
        return -0.01
    if pixels >= 15:
        return 0.0
    return 0.005


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------


def color_block(colors: Dict[str, str], indent: str = "  ") -> List[str]:
    return [
        "{0}--color-{1}: {2};".format(indent, name, value)
        for name, value in colors.items()
    ]


def contrast_comment(pairs: List[Dict[str, object]], theme: str) -> str:
    # Names are emitted with the same prefix the properties carry, so the
    # comment can be resolved directly against the declarations above it.
    names = [
        "color-{0}:color-{1}".format(pair.get("fg"), pair.get("bg"))
        for pair in pairs
        if pair.get("theme") == theme
    ]
    if not names:
        return ""
    return "  /* contrast-pairs: {0} */".format(", ".join(names))


def format_css(tokens: Dict[str, object], theme: str) -> str:
    lines: List[str] = []
    colors = tokens["colors"]
    pairs = tokens["contrast_pairs"]

    lines.append("/* {0}".format(tokens["label"]))
    dials = tokens["dials"]
    lines.append(
        "   opulence {0}, density {1}, motion {2} */".format(
            dials["opulence"], dials["density"], dials["motion"]
        )
    )
    lines.append("")
    lines.append(":root {")

    fonts = tokens["fonts"]
    if fonts.get("display"):
        lines.append('  --font-display: "{0}", Georgia, serif;'.format(fonts["display"]))
    if fonts.get("body"):
        lines.append(
            '  --font-body: "{0}", ui-sans-serif, system-ui, sans-serif;'.format(
                fonts["body"]
            )
        )
    if fonts.get("mono"):
        lines.append(
            '  --font-mono: "{0}", ui-monospace, SFMono-Regular, monospace;'.format(
                fonts["mono"]
            )
        )
    lines.append("")

    for name, value in tokens["type"]["sizes"].items():
        lines.append("  --text-{0}: {1};".format(name, value))
    lines.append("")
    for name, value in tokens["leading"].items():
        lines.append("  --leading-{0}: {1};".format(name, value))
    lines.append("")
    for name, value in tokens["tracking"].items():
        lines.append("  --tracking-{0}: {1};".format(name, value))
    lines.append("")
    for name, value in tokens["spacing"].items():
        lines.append("  --space-{0}: {1};".format(name, value))
    lines.append("")
    for name, value in tokens["radii"].items():
        lines.append("  --radius-{0}: {1};".format(name, value))
    lines.append("")
    for name, value in tokens["shadows"].items():
        lines.append("  --shadow-{0}: {1};".format(name, value))
    lines.append("")
    for name, value in tokens["borders"].items():
        lines.append("  --border-{0}: {1};".format(name, value))
    lines.append("")
    for name, value in tokens["motion"]["durations"].items():
        lines.append("  --duration-{0}: {1};".format(name, value))
    for name, value in tokens["motion"]["easings"].items():
        lines.append("  --ease-{0}: {1};".format(name, value))

    if theme in ("light", "auto"):
        lines.append("")
        comment = contrast_comment(pairs, "light")
        if comment:
            lines.append(comment)
        lines.extend(color_block(colors.get("light", {})))

    lines.append("}")

    if theme == "dark":
        lines.append("")
        lines.append(":root {")
        comment = contrast_comment(pairs, "dark")
        if comment:
            lines.append(comment)
        lines.extend(color_block(colors.get("dark", {})))
        lines.append("}")

    if theme == "auto":
        lines.append("")
        lines.append("@media (prefers-color-scheme: dark) {")
        lines.append("  :root:not([data-theme=\"light\"]) {")
        comment = contrast_comment(pairs, "dark")
        if comment:
            lines.append("  " + comment)
        lines.extend(color_block(colors.get("dark", {}), indent="    "))
        lines.append("  }")
        lines.append("}")
        lines.append("")
        lines.append('[data-theme="dark"] {')
        lines.extend(color_block(colors.get("dark", {})))
        lines.append("}")

    lines.append("")
    lines.append("@media (prefers-reduced-motion: reduce) {")
    lines.append("  :root {")
    for name in tokens["motion"]["durations"]:
        lines.append("    --duration-{0}: 1ms;".format(name))
    lines.append("  }")
    lines.append("}")

    return "\n".join(lines)


def format_tailwind(tokens: Dict[str, object]) -> str:
    """Emit a Tailwind theme that points at the CSS custom properties."""
    theme = {
        "colors": {
            name: "var(--color-{0})".format(name)
            for name in tokens["colors"].get("light", {})
        },
        "fontFamily": {
            key: ["var(--font-{0})".format(key)]
            for key in tokens["fonts"]
            if tokens["fonts"].get(key)
        },
        "fontSize": {
            name: "var(--text-{0})".format(name) for name in tokens["type"]["sizes"]
        },
        "spacing": {
            name: "var(--space-{0})".format(name) for name in tokens["spacing"]
        },
        "borderRadius": {
            name: "var(--radius-{0})".format(name) for name in tokens["radii"]
        },
        "boxShadow": {
            name: "var(--shadow-{0})".format(name) for name in tokens["shadows"]
        },
        "transitionDuration": {
            name: "var(--duration-{0})".format(name)
            for name in tokens["motion"]["durations"]
        },
        "transitionTimingFunction": {
            name: "var(--ease-{0})".format(name)
            for name in tokens["motion"]["easings"]
        },
    }
    return "module.exports = {{\n  theme: {{\n    extend: {0}\n  }}\n}};".format(
        json.dumps(theme, indent=6)
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tokens.py",
        description="Generate design tokens from a direction and dial values.",
        epilog=(
            "Example:\n"
            "  tokens.py --direction obsidian --density 5 --format css\n"
            "  tokens.py --list\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--direction", help="Direction name, such as obsidian.")
    parser.add_argument(
        "--opulence",
        type=int,
        default=DIAL_DEFAULT_OPULENCE,
        help="Ornament and richness, 1 to 10. Default {0}.".format(
            DIAL_DEFAULT_OPULENCE
        ),
    )
    parser.add_argument(
        "--density",
        type=int,
        default=DIAL_DEFAULT_DENSITY,
        help="Information per viewport, 1 to 10. Default {0}.".format(
            DIAL_DEFAULT_DENSITY
        ),
    )
    parser.add_argument(
        "--motion",
        type=int,
        default=DIAL_DEFAULT_MOTION,
        help="Animation depth, 1 to 10. Default {0}.".format(DIAL_DEFAULT_MOTION),
    )
    parser.add_argument(
        "--theme",
        choices=("light", "dark", "auto"),
        default="auto",
        help="Which theme to emit. Default auto.",
    )
    parser.add_argument(
        "--format",
        choices=("css", "json", "tailwind"),
        default="css",
        help="Output format. Default css.",
    )
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Shorthand for --format json.",
    )
    parser.add_argument(
        "--list",
        dest="list_directions",
        action="store_true",
        help="List available directions and exit.",
    )
    parser.add_argument(
        "--directions-dir",
        type=Path,
        default=DIRECTIONS_DIR,
        help="Where the direction JSON files live.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    if args.list_directions:
        for name in available_directions(args.directions_dir):
            print(name)
        return 0

    if not args.direction:
        print("error: --direction is required, or use --list", file=sys.stderr)
        return 2

    try:
        check_dial("--opulence", args.opulence)
        check_dial("--density", args.density)
        check_dial("--motion", args.motion)
        direction = load_direction(args.direction, args.directions_dir)
    except TokenError as exc:
        print("error: {0}".format(exc), file=sys.stderr)
        return 2

    tokens = build_tokens(direction, args.opulence, args.density, args.motion)
    output = "json" if args.as_json else args.format

    if output == "json":
        print(json.dumps(tokens, indent=2))
    elif output == "tailwind":
        print(format_tailwind(tokens))
    else:
        print(format_css(tokens, args.theme))

    return 0


if __name__ == "__main__":
    sys.exit(main())
