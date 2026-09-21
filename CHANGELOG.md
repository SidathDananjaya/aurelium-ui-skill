# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Repository structure, license, contributing guide, credits, and agent instructions.
- Line ending normalization via `.gitattributes` and a project `.gitignore`.
- Pull request and issue templates.
- `tools/validate_skill.py`, a standard library validator for skill frontmatter, reference links, file length, and direction token files.
- `tests/test_validate_skill.py` with fixtures covering one valid skill and six deliberately broken ones.
- Skeleton `skills/aurelium-ui/SKILL.md` carrying the real frontmatter.
- GitHub Actions CI running the test suite and the validator on Python 3.9 and 3.13.
- Doctrine references: the ten luxury principles, fourteen UX laws, Nielsen's ten heuristics restated as binary checks, the WCAG 2.2 AA accessibility baseline, and the Core Web Vitals performance budget.
- Source attribution for the doctrine material in `CREDITS.md`.

### Fixed

- The validator line count test no longer rewrites a tracked fixture, which corrupted its line endings on Windows. It now builds its sample in a temporary directory, and a new test guards against the regression.

[Unreleased]: https://github.com/SidathDananjaya/aurelium-ui-skill/commits/main
