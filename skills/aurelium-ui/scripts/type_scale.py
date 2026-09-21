#!/usr/bin/env python3
"""Generate a modular type scale with line heights and tracking.

Example::

    type_scale.py --base 16 --ratio 1.25 --steps -2..6

Each step reports a rem size, a pixel equivalent, a line height chosen from the
size band, and letter spacing that tightens as size grows. The bands follow
``references/foundations/typography.md``.

Standard library only. Exit code 0 on success, 2 for a usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Dict, List, Optional, Tuple

STEP_RANGE_PATTERN = re.compile(r"^(-?\d+)\.\.(-?\d+)$")

# Step index to token name, centred on 0 for the base size.
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


def line_height_for(pixels: float) -> float:
    """Line height by size band. Large text needs proportionally less leading."""
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
    """Letter spacing in em. Negative for display, zero at body, positive below."""
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


def round_to(value: float, places: int) -> float:
    quantum = 10 ** places
    return int(round(value * quantum)) / quantum


def step_name(index: int) -> str:
    if index in STEP_NAMES:
        return STEP_NAMES[index]
    return "step{0}{1}".format("m" if index < 0 else "p", abs(index))


def build_scale(base: float, ratio: float, first: int, last: int) -> List[Dict[str, object]]:
    """Return one entry per step, from ``first`` to ``last`` inclusive."""
    steps: List[Dict[str, object]] = []
    for index in range(first, last + 1):
        pixels = base * (ratio ** index)
        rem = pixels / base
        steps.append(
            {
                "step": index,
                "name": step_name(index),
                "px": round_to(pixels, 2),
                "rem": round_to(rem, 3),
                "line_height": line_height_for(pixels),
                "letter_spacing": tracking_for(pixels),
            }
        )
    return steps


def parse_steps(value: str) -> Tuple[int, int]:
    match = STEP_RANGE_PATTERN.match(value.strip())
    if not match:
        raise argparse.ArgumentTypeError(
            "expected a range such as -2..6, got '{0}'".format(value)
        )
    first, last = int(match.group(1)), int(match.group(2))
    if first > last:
        raise argparse.ArgumentTypeError(
            "range start {0} is above its end {1}".format(first, last)
        )
    if last - first > 24:
        raise argparse.ArgumentTypeError("range is too wide, use 24 steps or fewer")
    return first, last


def format_css(steps: List[Dict[str, object]]) -> str:
    lines = [":root {"]
    for entry in steps:
        lines.append(
            "  --text-{0}: {1}rem; /* {2}px */".format(
                entry["name"], entry["rem"], entry["px"]
            )
        )
    lines.append("")
    for entry in steps:
        lines.append(
            "  --leading-{0}: {1};".format(entry["name"], entry["line_height"])
        )
    lines.append("")
    for entry in steps:
        spacing = entry["letter_spacing"]
        lines.append(
            "  --tracking-{0}: {1}em;".format(entry["name"], spacing)
        )
    lines.append("}")
    return "\n".join(lines)


def format_table(steps: List[Dict[str, object]], base: float, ratio: float) -> str:
    lines = [
        "Base {0}px, ratio {1}".format(round_to(base, 2), ratio),
        "",
        "{0:>5}  {1:<6} {2:>9} {3:>9} {4:>8} {5:>10}".format(
            "step", "name", "rem", "px", "leading", "tracking"
        ),
        "-" * 54,
    ]
    for entry in steps:
        lines.append(
            "{0:>5}  {1:<6} {2:>8}r {3:>8}p {4:>8} {5:>9}e".format(
                entry["step"],
                entry["name"],
                entry["rem"],
                entry["px"],
                entry["line_height"],
                entry["letter_spacing"],
            )
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="type_scale.py",
        description="Generate a modular type scale with line heights and tracking.",
        epilog="Example:\n  type_scale.py --base 16 --ratio 1.25 --steps -2..6\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--base", type=float, default=16.0, help="Base font size in px. Default 16."
    )
    parser.add_argument(
        "--ratio", type=float, default=1.25, help="Scale ratio. Default 1.25."
    )
    parser.add_argument(
        "--steps",
        type=parse_steps,
        default=(-2, 6),
        help="Inclusive step range, such as -2..6. Default -2..6.",
    )
    parser.add_argument(
        "--format",
        choices=("table", "css", "json"),
        default="table",
        help="Output format. Default table.",
    )
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Shorthand for --format json.",
    )
    return parser


def normalise_argv(argv: List[str]) -> List[str]:
    """Join an option with a following value that begins with a hyphen.

    argparse treats "-2..6" as an option string, so "--steps -2..6" fails even
    though it is the documented spelling. Rewriting it to "--steps=-2..6"
    keeps the documented form working without changing anything else.
    """
    joined: List[str] = []
    index = 0
    while index < len(argv):
        token = argv[index]
        if (
            token == "--steps"
            and index + 1 < len(argv)
            and argv[index + 1].startswith("-")
        ):
            joined.append("{0}={1}".format(token, argv[index + 1]))
            index += 2
            continue
        joined.append(token)
        index += 1
    return joined


def main(argv: Optional[List[str]] = None) -> int:
    raw = list(sys.argv[1:]) if argv is None else list(argv)
    args = build_parser().parse_args(normalise_argv(raw))

    if args.base <= 0:
        print("error: --base must be above zero", file=sys.stderr)
        return 2
    if args.ratio <= 1.0:
        print("error: --ratio must be above 1.0", file=sys.stderr)
        return 2

    first, last = args.steps
    steps = build_scale(args.base, args.ratio, first, last)
    output = "json" if args.as_json else args.format

    if output == "json":
        print(
            json.dumps(
                {"base": args.base, "ratio": args.ratio, "steps": steps}, indent=2
            )
        )
    elif output == "css":
        print(format_css(steps))
    else:
        print(format_table(steps, args.base, args.ratio))

    return 0


if __name__ == "__main__":
    sys.exit(main())
