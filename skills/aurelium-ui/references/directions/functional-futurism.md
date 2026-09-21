# Functional Futurism

Functional Futurism is instrumentation, not science fiction. It assumes the user is monitoring something real and consequential, so every glow, every figure, and every transition reports state rather than decorating it. The result feels advanced because it is dense with meaning, not because it is dark and has a gradient.

**Mood.** Precise, technical, cinematic
**Best for.** AI products, aerospace, security, energy, logistics, mission control
**Avoid for.** Content-heavy reading experiences, editorial, long-form anything

Generate the tokens rather than copying the values below:

```
python scripts/tokens.py --direction functional-futurism --theme auto --format css
```

## Colors

| Token | Light | Dark |
|---|---|---|
| `page` | `#f4f5f6` | `#08090a` |
| `surface` | `#ffffff` | `#101315` |
| `surface-raised` | `#ffffff` | `#181c1f` |
| `text` | `#101214` | `#e9edf0` |
| `text-muted` | `#53585e` | `#98a1a9` |
| `border` | `#dcdfe3` | `#22272b` |
| `accent` | `#00636b` | `#35e0d0` |
| `accent-hover` | `#004c52` | `#6aeade` |
| `accent-fg` | `#ffffff` | `#08090a` |
| `focus` | `#00636b` | `#35e0d0` |
| `success` | `#1f6b45` | `#4fd18a` |
| `warning` | `#7a5200` | `#e0b24f` |
| `danger` | `#a52218` | `#ff6b5c` |
| `info` | `#12547f` | `#6bb6f0` |

Every pair above is verified against WCAG AA in both themes by the repository
validator. Changing any value requires re-running the check.

## Typography

| Role | Family |
|---|---|
| Display | Space Grotesk |
| Body | Space Grotesk |
| Mono | JetBrains Mono |

Space Grotesk for display and body, whose slightly irregular letterforms keep a technical interface from reading as sterile. JetBrains Mono for every figure, identifier, coordinate, and timestamp, which in this direction is most of the text on screen. The 1.2 ratio supports the many close steps a dense panel layout needs.

Base 15px, ratio 1.2.

| Step | Size | Pixels |
|---|---|---|
| `2xs` | `0.694rem` | 10.4px |
| `xs` | `0.833rem` | 12.5px |
| `base` | `1.0rem` | 15.0px |
| `lg` | `1.2rem` | 18.0px |
| `xl` | `1.44rem` | 21.6px |
| `2xl` | `1.728rem` | 25.9px |
| `3xl` | `2.074rem` | 31.1px |
| `4xl` | `2.488rem` | 37.3px |
| `5xl` | `2.986rem` | 44.8px |

## Spacing

Base grid 4px, multiplier 0.875. Inner spacing is always smaller
than outer spacing.

| Purpose | Token |
|---|---|
| Label to control | `--space-2` |
| Rows within a container | `--space-3` to `--space-4` |
| Sibling components | `--space-5` to `--space-6` |
| Section to section | `--space-9` and above |

## Radius

| Radius | Value |
|---|---|
| `none` | `0` |
| `sm` | `0` |
| `md` | `2px` |
| `lg` | `4px` |
| `pill` | `999px` |

## Elevation

Layers rather than elevation. Surfaces are near-black steps, separated by a one pixel border rather than a shadow. Glow is reserved strictly for live state: an active connection, a streaming response, a current reading. A glow that is not reporting something is a bug.

| Level | Value |
|---|---|
| `e1` | `0 1px 2px rgba(0, 0, 0, 0.20)` |
| `e2` | `0 2px 6px rgba(0, 0, 0, 0.26), 0 8px 18px rgba(0, 0, 0, 0.22)` |
| `e3` | `0 4px 12px rgba(0, 0, 0, 0.30), 0 22px 50px rgba(0, 0, 0, 0.36)` |

## Borders

| Border | Value |
|---|---|
| `hairline` | `1px` |
| `focus-width` | `2px` |
| `focus-offset` | `2px` |

## Motion

Telemetric. The fastest durations in the set, because the interface is meant to feel instrumented and responsive. Transitions confirm that data arrived. Any startup or boot sequence is skippable, and skipped permanently once dismissed.

| Duration | Value |
|---|---|
| `fast` | `90ms` |
| `base` | `150ms` |
| `slow` | `260ms` |

| Easing | Value |
|---|---|
| `standard` | `cubic-bezier(0.2, 0, 0, 1)` |
| `exit` | `cubic-bezier(0.5, 0, 1, 1)` |
| `entrance` | `cubic-bezier(0, 0, 0.15, 1)` |

Every motion token collapses to 1ms under `prefers-reduced-motion`, and each
transition keeps a non-motion way to read the state change.

## Signature details

- **Bracket frames.** Corner brackets rather than full borders on the focused or selected panel, which reads as a viewfinder.
- **Glow as state only.** The teal accent glows when something is live, and is flat the rest of the time. The difference is the information.
- **Ambient grid.** A very low contrast grid layer behind content, never above it, never animated.
- **Monospaced telemetry.** Every changing figure in mono with tabular numerals, so a value updating in place never shifts the layout.
- **Skippable boot.** Any initialisation sequence can be skipped, and is not shown again once dismissed.

## Component notes

Buttons are square with a 2px radius, primary in teal with near-black text, secondary as a one pixel border that brightens on hover. Panels replace cards: a surface step, a one pixel border, a small mono label in the top left, and optional corner brackets when active. Status indicators always pair the color with a glyph and a word. Data tables are dense, mono, and right aligned for figures.

## Do

- Reserve glow strictly for live state
- Put every changing figure in mono with tabular numerals
- Pair every status color with a glyph and a word
- Make any boot or initialisation sequence skippable

## Don't

- Glow anything that is not reporting a live reading
- Animate the ambient grid
- Use this direction for a reading-heavy interface
- Add scanline or CRT effects, which are costume rather than function

## Example screen

A drone fleet mission control view. A left panel lists active units as rows of mono identifiers with a status glyph, a battery figure, and a signal reading. The centre is a map with the ambient grid behind it and each unit marked with a bracket frame when selected. The right panel shows the selected unit's telemetry as a label and value list, all mono, all tabular, updating in place without shifting. Only the units currently transmitting carry the teal glow.
