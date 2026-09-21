---
name: aurelium-ui
description: Design and build luxury-grade, premium web app UI and UX for any product type, including dashboards, SaaS, e-commerce, booking, fintech, admin tools, editorial sites, portfolios, and landing pages. Use when the user asks to build, design, redesign, polish, elevate, or review a web interface, or asks for a premium, high-end, luxury, elegant, refined, minimal, futuristic, or award-quality look. Also use to audit an existing UI for visual hierarchy, typography, spacing, motion, accessibility, and UX quality.
license: MIT
metadata:
  author: SidathDananjaya
  version: 0.1.0
---

# Aurelium UI

Design and build interfaces that feel expensive, considered, and effortless.

Luxury in software is the absence of friction and the presence of care. It is
not ornament. It is clarity, restraint, precision, material quality, and
effortlessness, in that order of priority.

## Modes

Detect the mode from the request. When both apply, audit first, then create.

| Mode | Triggers | Go to |
|---|---|---|
| **Create** | build, design, make, create, add a page, new screen, from scratch | `workflows/create.md` |
| **Audit and Elevate** | review, audit, critique, improve, polish, elevate, fix, "make this better", an existing URL or file | `workflows/audit.md` |

Default to Create when nothing in the request points to existing work.

## Non-negotiable laws

These are ordered. When two conflict, the lower number wins.

1. **Space is the material.** Spacing comes from the scale. Never fill space because it is empty.
2. **One hero per view.** Exactly one primary focal point and one primary action per screen.
3. **Typography carries the brand.** Hierarchy from size, then weight, then spacing, then colour. Two families, plus mono for data.
4. **Restrained palette.** Neutrals do 90 percent. One accent. Semantic colour only for meaning.
5. **Precision.** 4px grid. Optical alignment over mathematical. Tabular figures for numbers.
6. **Material and depth with intent.** Three elevation levels at most. Elevation means layering, never decoration.
7. **Quiet motion.** Short, eased, interruptible. Nothing moves without a statable reason.
8. **Care in the details.** Empty, loading, error, and success states are designed, not defaults.
9. **Effortless performance.** LCP under 2.5s, INP under 200ms, CLS under 0.1.
10. **Inclusive by default.** WCAG 2.2 AA is the floor. Luxury that excludes is not luxury.

**The complete-states rule.** Every data-driven view ships all of: default,
loading, empty on first use, empty with no results, recoverable error, fatal
error, partial data, offline where applicable, success, long content, and
permission denied where applicable.

State any tradeoff out loud. "I dropped the parallax header because it pushed
LCP past budget" is a design decision worth reporting.

## Dials

Read these from the request, or infer and state your choice.

| Dial | 1 | 5 | 10 |
|---|---|---|---|
| **OPULENCE** | Pure function, flat surfaces, no decorative elements | Considered accents, one signature detail per view | Layered depth, rich materials, ambient effects, still within performance budget |
| **DENSITY** | Spacious, one idea per screen, editorial rhythm | Balanced product UI | Compact rows, smaller type steps, multi-panel layouts |
| **MOTION** | State changes only: hover, focus, open, close | Plus page transitions and list animation | Plus choreographed sequences and scroll-driven storytelling |

`THEME` is `light`, `dark`, or `auto`. Auto respects `prefers-color-scheme`.

Defaults when the brief does not indicate otherwise: **opulence 4, density 5,
motion 4, theme auto.**

## Directions

Five complete systems. Pick one and commit to it. Never blend two.

| Direction | Mood | Best for |
|---|---|---|
| Quiet Luxury | Editorial, calm, warm | Hospitality, fashion, real estate, wellness, portfolios |
| Obsidian | Dark, rich, confident | Fintech, premium SaaS, automotive, watches |
| Tactile Craft | Tactile, crafted, human | Consumer apps, booking, food, lifestyle, e-commerce |
| Swiss Precision | Rational, sharp | Dev tools, analytics, agencies, architecture |
| Functional Futurism | Precise, technical, cinematic | AI, aerospace, security, energy, mission control |

Choose with the decision tables in `references/directions/index.md`, then read
that direction's own file before building.

## Generate tokens, do not invent them

```
python scripts/tokens.py --direction obsidian --opulence 4 --density 5 --motion 4 --theme auto --format css
python scripts/contrast.py --tokens tokens.css
python scripts/type_scale.py --base 16 --ratio 1.25 --steps -2..6
```

Every direction ships both themes, and every declared colour pair passes WCAG
AA in both. Hand-writing token values discards that guarantee.

Persist a `DESIGN.md` into the user's project recording direction, dials, and
token location. If one already exists, read it and follow it rather than
imposing a new system.

## Reference map

Load on demand. Do not read everything up front.

| Need | File |
|---|---|
| The ten principles in full, with checks | `references/doctrine/luxury-principles.md` |
| UX laws and how to apply them | `references/doctrine/ux-laws.md` |
| Nielsen's heuristics as binary checks | `references/doctrine/heuristics.md` |
| Contrast, focus, keyboard, targets, ARIA | `references/doctrine/accessibility.md` |
| Core Web Vitals, fonts, images, animation cost | `references/doctrine/performance.md` |
| Ramps, accents, semantics, dark mode | `references/foundations/color.md` |
| Scale, measure, leading, tracking, OFL fonts | `references/foundations/typography.md` |
| Grid, spacing scale, breakpoints, containers | `references/foundations/spacing-layout.md` |
| Elevation, borders, radius, texture, blur | `references/foundations/surfaces-depth.md` |
| Icon family, stroke, optical sizing, labels | `references/foundations/iconography.md` |
| Art direction, ratios, placeholders, alt text | `references/foundations/imagery.md` |
| Voice, buttons, errors, empty states | `references/foundations/microcopy.md` |
| Choosing a direction | `references/directions/index.md` |
| The direction token contract | `assets/directions/_schema.md` |
| Hierarchy, sizes, loading, icon buttons | `references/components/buttons.md` |
| Labels, validation timing, errors, multi-step | `references/components/forms.md` |
| Top bar, sidebar, tabs, breadcrumbs, mobile | `references/components/navigation.md` |
| When a card earns its place, grids, clamping | `references/components/cards-lists.md` |
| Density, sticky headers, sorting, bulk actions | `references/components/tables.md` |
| Modals, drawers, popovers, toasts, focus | `references/components/overlays.md` |
| KPIs, choosing a chart, chart accessibility | `references/components/data-display.md` |
| Galleries, carousels, product imagery, video | `references/components/media.md` |
| The complete-states rule, state by state | `references/patterns/states.md` |
| Optimistic UI, progress, undo over confirm | `references/patterns/feedback.md` |
| Search, filters, applied-filter chips, URL state | `references/patterns/search-filter.md` |
| Time to first value, multi-step flows, checklists | `references/patterns/onboarding.md` |

Archetypes, motion recipes, quality gates, and stack recipes are being added in
later releases. Until they land, work from the references above.

## Output contract

End every piece of work with this. No exceptions.

```
Direction   Obsidian, opulence 4, density 6, motion 3, theme auto
Files       tokens.css, index.html, dashboard.html, DESIGN.md
Pre-flight  Contrast 22/22 pass. One primary action per view. All states
            implemented. Keyboard and focus verified. Renders 375 to 1440.
Gaps        Offline state not implemented, the product has no offline mode.
            Chart colours need review against the accent at density 8.
```

Report what you did not do as clearly as what you did. A gap named is a
professional handoff. A gap hidden is a defect you shipped.

Never claim a check passed unless you ran it.
