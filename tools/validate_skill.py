#!/usr/bin/env python3
"""Validate Agent Skill folders against the Aurelium UI repository rules.

Checks performed on every skill folder found under the given paths:

1. The folder contains a file named exactly ``SKILL.md``.
2. ``SKILL.md`` opens with YAML frontmatter delimited by ``---`` lines.
3. The frontmatter contains no angle brackets.
4. ``name`` is present, 1 to 64 characters, lowercase letters, digits and
   single hyphens only, and matches the folder name.
5. ``description`` is present and 1 to 1024 characters.
6. Optional keys are limited to ``license``, ``compatibility`` and ``metadata``.
   ``compatibility`` is capped at 500 characters.
7. ``SKILL.md`` is shorter than 500 lines.
8. Every relative path referenced from any Markdown file in the skill exists.
9. Every direction JSON in ``assets/directions`` carries the required keys.

Standard library only. Exit code 0 when everything passes, 1 when any check
fails, and 2 for a usage error.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import Dict, List, Optional, Tuple

SKILL_FILENAME = "SKILL.md"
MAX_SKILL_LINES = 500
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500

REQUIRED_KEYS = ("name", "description")
OPTIONAL_KEYS = ("license", "compatibility", "metadata")

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Markdown inline links, excluding images: [label](target)
MD_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)")
# Backticked paths such as `references/directions/index.md`
CODE_PATH_PATTERN = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|json|py|css|html|svg))`")

SKIP_LINK_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#", "/")

# Baseline direction token keys. Phase 4 defines the full schema in
# assets/directions/_schema.md and may extend this mapping.
REQUIRED_DIRECTION_KEYS: Dict[str, Tuple[str, ...]] = {
    "name": (),
    "colors": ("light", "dark"),
    "fonts": (),
    "type": ("base", "ratio"),
    "spacing": ("base",),
    "radii": (),
    "shadows": (),
    "borders": (),
    "motion": ("durations", "easings"),
    "contrast_pairs": (),
}


class Finding:
    """A single validation failure."""

    def __init__(self, path: Path, check: str, message: str) -> None:
        self.path = path
        self.check = check
        self.message = message

    def as_dict(self, root: Path) -> Dict[str, str]:
        return {
            "path": relative_to(self.path, root),
            "check": self.check,
            "message": self.message,
        }

    def __str__(self) -> str:
        return "{0}: [{1}] {2}".format(self.path, self.check, self.message)


def relative_to(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------


class FrontmatterError(Exception):
    """Raised when frontmatter cannot be parsed."""


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def split_frontmatter(text: str) -> Tuple[str, int]:
    """Return the raw frontmatter block and the number of lines it occupies."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError("file does not start with a '---' frontmatter delimiter")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), index + 1
    raise FrontmatterError("frontmatter is not closed by a second '---' delimiter")


def parse_frontmatter(block: str) -> Dict[str, object]:
    """Parse the small YAML subset the skill spec allows.

    Supports top level ``key: value`` pairs and one level of nesting under a
    key with an empty value. Anything else is rejected rather than guessed at.
    """
    data: Dict[str, object] = {}
    current_map: Optional[str] = None

    for lineno, raw in enumerate(block.splitlines(), start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        if "\t" in raw[:indent]:
            raise FrontmatterError("line {0}: indent with spaces, not tabs".format(lineno))

        stripped = raw.strip()
        if stripped.startswith("- "):
            raise FrontmatterError(
                "line {0}: lists are not supported in frontmatter".format(lineno)
            )
        if ":" not in stripped:
            raise FrontmatterError("line {0}: expected 'key: value'".format(lineno))

        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()

        if value in ("|", ">", "|-", ">-"):
            raise FrontmatterError(
                "line {0}: block scalars are not supported".format(lineno)
            )

        if indent == 0:
            if not value:
                data[key] = {}
                current_map = key
            else:
                data[key] = strip_quotes(value)
                current_map = None
        else:
            if current_map is None:
                raise FrontmatterError(
                    "line {0}: unexpected indented key '{1}'".format(lineno, key)
                )
            if not value:
                raise FrontmatterError(
                    "line {0}: '{1}' needs a value, nesting is limited to one level".format(
                        lineno, key
                    )
                )
            nested = data[current_map]
            if not isinstance(nested, dict):
                raise FrontmatterError(
                    "line {0}: '{1}' is not a mapping".format(lineno, current_map)
                )
            nested[key] = strip_quotes(value)

    return data


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def check_frontmatter(skill_md: Path, folder_name: str, findings: List[Finding]) -> None:
    text = skill_md.read_text(encoding="utf-8")

    line_count = len(text.splitlines())
    if line_count >= MAX_SKILL_LINES:
        findings.append(
            Finding(
                skill_md,
                "line-count",
                "{0} lines, must be under {1}. Move detail into references/.".format(
                    line_count, MAX_SKILL_LINES
                ),
            )
        )

    try:
        block, _ = split_frontmatter(text)
    except FrontmatterError as exc:
        findings.append(Finding(skill_md, "frontmatter", str(exc)))
        return

    if "<" in block or ">" in block:
        findings.append(
            Finding(skill_md, "frontmatter", "angle brackets are not allowed in frontmatter")
        )

    try:
        data = parse_frontmatter(block)
    except FrontmatterError as exc:
        findings.append(Finding(skill_md, "frontmatter", str(exc)))
        return

    for key in REQUIRED_KEYS:
        if key not in data:
            findings.append(
                Finding(skill_md, "frontmatter", "missing required key '{0}'".format(key))
            )

    unknown = set(data) - set(REQUIRED_KEYS) - set(OPTIONAL_KEYS)
    for key in sorted(unknown):
        findings.append(Finding(skill_md, "frontmatter", "unknown key '{0}'".format(key)))

    name = data.get("name")
    if isinstance(name, str):
        if not 1 <= len(name) <= MAX_NAME_LENGTH:
            findings.append(
                Finding(
                    skill_md, "name", "must be 1 to {0} characters".format(MAX_NAME_LENGTH)
                )
            )
        if not NAME_PATTERN.match(name):
            findings.append(
                Finding(
                    skill_md,
                    "name",
                    "'{0}' must be lowercase letters, digits and single hyphens, "
                    "with no leading or trailing hyphen".format(name),
                )
            )
        if name != folder_name:
            findings.append(
                Finding(
                    skill_md,
                    "name",
                    "'{0}' must match the folder name '{1}'".format(name, folder_name),
                )
            )
    elif name is not None:
        findings.append(Finding(skill_md, "name", "must be a string"))

    description = data.get("description")
    if isinstance(description, str):
        if not 1 <= len(description) <= MAX_DESCRIPTION_LENGTH:
            findings.append(
                Finding(
                    skill_md,
                    "description",
                    "{0} characters, must be 1 to {1}".format(
                        len(description), MAX_DESCRIPTION_LENGTH
                    ),
                )
            )
    elif description is not None:
        findings.append(Finding(skill_md, "description", "must be a string"))

    compatibility = data.get("compatibility")
    if isinstance(compatibility, str) and len(compatibility) > MAX_COMPATIBILITY_LENGTH:
        findings.append(
            Finding(
                skill_md,
                "compatibility",
                "{0} characters, must be at most {1}".format(
                    len(compatibility), MAX_COMPATIBILITY_LENGTH
                ),
            )
        )

    metadata = data.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        findings.append(Finding(skill_md, "metadata", "must be a mapping of keys to values"))


def candidate_paths(markdown_file: Path, skill_dir: Path, target: str) -> List[Path]:
    cleaned = target.split("#", 1)[0].split("?", 1)[0].strip()
    if not cleaned:
        return []
    return [markdown_file.parent / cleaned, skill_dir / cleaned]


def check_references(skill_dir: Path, findings: List[Finding]) -> None:
    for markdown_file in sorted(skill_dir.rglob("*.md")):
        text = markdown_file.read_text(encoding="utf-8")
        targets = set()

        for match in MD_LINK_PATTERN.finditer(text):
            target = match.group(1)
            if target.startswith(SKIP_LINK_PREFIXES):
                continue
            targets.add(target)

        for match in CODE_PATH_PATTERN.finditer(text):
            target = match.group(1)
            if target.startswith(SKIP_LINK_PREFIXES) or "/" not in target:
                continue
            targets.add(target)

        for target in sorted(targets):
            options = candidate_paths(markdown_file, skill_dir, target)
            if options and not any(option.exists() for option in options):
                findings.append(
                    Finding(
                        markdown_file,
                        "reference",
                        "referenced path '{0}' does not exist".format(target),
                    )
                )


def load_contrast_module(skill_dir: Path) -> Optional[ModuleType]:
    """Load the skill's own contrast checker, so the WCAG math is not duplicated."""
    path = skill_dir / "scripts" / "contrast.py"
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("aurelium_contrast", path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:  # noqa: BLE001 - a broken script must not crash the run
        return None
    return module


def check_contrast_pairs(
    json_file: Path,
    data: Dict[str, object],
    contrast: Optional[ModuleType],
    findings: List[Finding],
) -> None:
    """Every declared contrast pair must meet its threshold."""
    pairs = data.get("contrast_pairs")
    if not isinstance(pairs, list) or not pairs:
        return

    if contrast is None:
        findings.append(
            Finding(
                json_file,
                "contrast",
                "contrast pairs are declared but scripts/contrast.py is missing, "
                "so they cannot be verified",
            )
        )
        return

    colors = data.get("colors")
    if not isinstance(colors, dict):
        return

    for index, pair in enumerate(pairs):
        if not isinstance(pair, dict):
            findings.append(
                Finding(json_file, "contrast", "pair {0} is not an object".format(index))
            )
            continue

        theme = pair.get("theme")
        foreground = pair.get("fg")
        background = pair.get("bg")
        minimum = pair.get("min", 4.5)

        if theme not in ("light", "dark"):
            findings.append(
                Finding(
                    json_file,
                    "contrast",
                    "pair {0} has theme '{1}', expected light or dark".format(
                        index, theme
                    ),
                )
            )
            continue

        palette = colors.get(theme)
        if not isinstance(palette, dict):
            findings.append(
                Finding(
                    json_file, "contrast", "colors.{0} is not an object".format(theme)
                )
            )
            continue

        missing = [
            name for name in (foreground, background) if name not in palette
        ]
        if missing:
            findings.append(
                Finding(
                    json_file,
                    "contrast",
                    "pair {0} names undefined colors in {1}: {2}".format(
                        index, theme, ", ".join(str(name) for name in missing)
                    ),
                )
            )
            continue

        try:
            ratio = contrast.contrast_ratio(
                contrast.parse_color(palette[foreground]),
                contrast.parse_color(palette[background]),
            )
        except Exception as exc:  # noqa: BLE001 - surfaced as a finding
            findings.append(
                Finding(json_file, "contrast", "pair {0}: {1}".format(index, exc))
            )
            continue

        if ratio < float(minimum):
            findings.append(
                Finding(
                    json_file,
                    "contrast",
                    "{0} on {1} in {2} is {3:.2f}:1, below the required {4}:1".format(
                        foreground, background, theme, ratio, minimum
                    ),
                )
            )


def check_direction_tokens(skill_dir: Path, findings: List[Finding]) -> None:
    directions_dir = skill_dir / "assets" / "directions"
    if not directions_dir.is_dir():
        return

    contrast = load_contrast_module(skill_dir)

    for json_file in sorted(directions_dir.glob("*.json")):
        if json_file.name.startswith("_"):
            continue
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            findings.append(
                Finding(json_file, "direction-json", "invalid JSON: {0}".format(exc))
            )
            continue

        if not isinstance(data, dict):
            findings.append(
                Finding(json_file, "direction-json", "top level must be an object")
            )
            continue

        for key, nested_keys in REQUIRED_DIRECTION_KEYS.items():
            if key not in data:
                findings.append(
                    Finding(
                        json_file, "direction-json", "missing required key '{0}'".format(key)
                    )
                )
                continue
            if not nested_keys:
                continue
            value = data[key]
            if not isinstance(value, dict):
                findings.append(
                    Finding(
                        json_file, "direction-json", "'{0}' must be an object".format(key)
                    )
                )
                continue
            for nested in nested_keys:
                if nested not in value:
                    findings.append(
                        Finding(
                            json_file,
                            "direction-json",
                            "missing required key '{0}.{1}'".format(key, nested),
                        )
                    )

        if data.get("name") not in (None, json_file.stem):
            findings.append(
                Finding(
                    json_file,
                    "direction-json",
                    "name '{0}' must match the filename '{1}'".format(
                        data.get("name"), json_file.stem
                    ),
                )
            )

        check_contrast_pairs(json_file, data, contrast, findings)


def validate_skill(skill_dir: Path, findings: List[Finding]) -> None:
    entries = {entry.name for entry in skill_dir.iterdir() if entry.is_file()}
    if SKILL_FILENAME not in entries:
        findings.append(
            Finding(
                skill_dir, "structure", "no file named exactly '{0}'".format(SKILL_FILENAME)
            )
        )
        return

    check_frontmatter(skill_dir / SKILL_FILENAME, skill_dir.name, findings)
    check_references(skill_dir, findings)
    check_direction_tokens(skill_dir, findings)


def discover_skills(path: Path) -> List[Path]:
    """Return every skill folder at or beneath ``path``."""
    if not path.is_dir():
        return []
    if (path / SKILL_FILENAME).is_file():
        return [path]
    return sorted({found.parent for found in path.rglob(SKILL_FILENAME)})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="validate_skill.py",
        description="Validate Agent Skill folders against the Aurelium UI repository rules.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Skill folders, or a parent folder such as skills/ to search.",
    )
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Emit machine readable results instead of text.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path.cwd()

    skills: List[Path] = []
    findings: List[Finding] = []

    for path in args.paths:
        if not path.exists():
            findings.append(Finding(path, "usage", "path does not exist"))
            continue
        found = discover_skills(path)
        if not found:
            findings.append(
                Finding(
                    path,
                    "usage",
                    "no folder containing {0} was found here".format(SKILL_FILENAME),
                )
            )
            continue
        skills.extend(found)

    for skill_dir in sorted(set(skills)):
        validate_skill(skill_dir, findings)

    if args.as_json:
        payload = {
            "ok": not findings,
            "skills": [relative_to(skill, root) for skill in sorted(set(skills))],
            "findings": [finding.as_dict(root) for finding in findings],
        }
        print(json.dumps(payload, indent=2))
    else:
        for finding in findings:
            print(str(finding), file=sys.stderr)
        checked = len(set(skills))
        noun = "skill" if checked == 1 else "skills"
        if findings:
            count = len(findings)
            issue = "issue" if count == 1 else "issues"
            print(
                "FAIL: {0} {1} in {2} {3}.".format(count, issue, checked, noun),
                file=sys.stderr,
            )
        else:
            print("OK: {0} {1} passed validation.".format(checked, noun))

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
