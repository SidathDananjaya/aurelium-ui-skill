# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- `CLAUDE.md` is no longer tracked. It is a local development file, and the Agent Skills spec constraints it carried have moved into `CONTRIBUTING.md` so contributors still have them.

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
- Foundations references: color, typography, spacing and layout, surfaces and depth, iconography, imagery, and microcopy.
- A verified list of twelve SIL Open Font License families, with the verification method recorded in `CREDITS.md`.
- Five design directions: Quiet Luxury, Obsidian, Tactile Craft, Swiss Precision, and Functional Futurism, each with a JSON token file, a reference document, and both themes.
- `assets/directions/_schema.md` defining the direction token contract.
- `references/directions/index.md` with decision tables by archetype and by brand mood.
- `scripts/contrast.py`, WCAG contrast checking for colour pairs and token files.
- `scripts/type_scale.py`, modular type scale generation with line height and tracking.
- `scripts/tokens.py`, turning a direction plus dial values into CSS, JSON, or a Tailwind theme.
- `tools/build_specimens.py`, rendering swatch and type specimen pages into `gallery/specimens/`.
- Validator now enforces that every declared contrast pair meets its threshold, and that a direction's name matches its filename.
- `SKILL.md` router: mode detection, the ten non-negotiable laws, the complete-states rule, dials, direction summary, reference map, and the output contract.
- `workflows/create.md` and `workflows/audit.md`.
- `tests/test_skill_structure.py` guarding the router's frontmatter, sections, reference map, and house style.
- Component references: buttons, forms, navigation, cards and lists, tables, overlays, data display, and media.
- Pattern references: states, feedback, search and filter, and onboarding.
- `tests/test_reference_snippets.py`, checking every guidance snippet uses tokens rather than hard-coded colour, spacing, radius, or duration.
- Reference map in `SKILL.md` now covers all twelve component and pattern files.
- Archetype references: marketing and landing, SaaS dashboard, analytics, e-commerce, booking, fintech, admin, and auth and onboarding, plus an index mapping request phrases to archetypes.
- Archetype tests enforcing the eight-section template, the 200 line limit, dial ranges, and cross-references to component and pattern files.
- `motion/principles.md`: the purpose test, duration by size and frequency, enter and exit asymmetry, easing tokens, springs, interruptibility, stagger, and reduced-motion alternatives.
- `motion/recipes.md`: thirteen recipes, each using tokens and each carrying a reduced-motion variant.
- `quality/anti-patterns.md` with a complete motion section. The visual, UX, and copy sections land in a later release.
- Motion tests enforcing a reduced-motion path per recipe, token-only durations, no bare easing keywords, and no animation from `scale(0)`.
- `quality/preflight.md`, the authoritative gate: 59 numbered checks across eleven groups, each stating how to run it.
- `quality/rubric.md` with the 40/30/20/10 weighting, a scoring scale, a six item craft checklist that caps categories on failure, and a worked example.
- `quality/detail-checklist.md`, 76 craft checks grouped by typography, spacing, colour, interaction, content, responsive, and imagery.
- `quality/anti-patterns.md` completed: 22 visual, 30 UX, 23 motion, and 20 copy entries.
- `assets/templates/DESIGN.md`, the design system template persisted into user projects.
- `tests/test_quality_layer.py`, guarding the gate's structure and the one-source-per-rule rule.

### Changed

- The create and audit workflows now point at `preflight.md`, `detail-checklist.md`, and `rubric.md` rather than restating them, so each rule has one source.
- Restored the last two Phase 2 cross-links: `heuristics.md` to `quality/rubric.md` and `luxury-principles.md` to `quality/preflight.md`. The reference map debt is now clear.

### Fixed

- The rubric's worked example gave 6.4 for a weighted total that is 6.3. Wrong arithmetic in a scoring rubric, caught by a test that recomputes it.
- The reference snippet test parsed CSS line by line, so a declaration wrapped across several lines was read as having an empty value and skipped. It now parses whole blocks and catches multi-line violations.
- Restored the cross-links in `luxury-principles.md` and `accessibility.md` that were written as prose in Phase 2 because their targets did not yet exist.
- `contrast.py` checked a stylesheet carrying two palettes against whichever theme appeared last, twice, and never checked the other. Pairs are now resolved against their own rule block, so a light and dark file is checked once per theme.

- The validator line count test no longer rewrites a tracked fixture, which corrupted its line endings on Windows. It now builds its sample in a temporary directory, and a new test guards against the regression.

[Unreleased]: https://github.com/SidathDananjaya/aurelium-ui-skill/commits/main
