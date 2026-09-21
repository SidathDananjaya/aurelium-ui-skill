# Swiss Precision

Swiss Precision holds that structure is the design and decoration is what you add when the structure is not working. It uses pure neutrals, a single saturated signal color, and a grid strict enough that alignment carries the hierarchy by itself. Everything is flat, because depth would be another variable and this direction wants fewer.

**Mood.** Rational, sharp, confident
**Best for.** Developer tools, analytics, agencies, architecture, documentation
**Avoid for.** Warm lifestyle brands, anything needing softness or comfort

Generate the tokens rather than copying the values below:

```
python scripts/tokens.py --direction swiss-precision --theme auto --format css
```

## Colors

| Token | Light | Dark |
|---|---|---|
| `page` | `#ffffff` | `#0d0d0d` |
| `surface` | `#ffffff` | `#161616` |
| `surface-raised` | `#ffffff` | `#1f1f1f` |
| `text` | `#111111` | `#f5f5f5` |
| `text-muted` | `#595959` | `#a3a3a3` |
| `border` | `#e0e0e0` | `#2a2a2a` |
| `accent` | `#c01515` | `#ff5a4d` |
| `accent-hover` | `#9c1010` | `#ff7a70` |
| `accent-fg` | `#ffffff` | `#0d0d0d` |
| `focus` | `#c01515` | `#ff5a4d` |
| `success` | `#1f6b3a` | `#5fc27e` |
| `warning` | `#7a5200` | `#d9a84e` |
| `danger` | `#c01515` | `#ff5a4d` |
| `info` | `#12547f` | `#6fb0e6` |

Every pair above is verified against WCAG AA in both themes by the repository
validator. Changing any value requires re-running the check.

## Typography

| Role | Family |
|---|---|
| Display | Schibsted Grotesk |
| Body | Schibsted Grotesk |
| Mono | IBM Plex Mono |

Schibsted Grotesk for both display and body, because a neo-grotesk at several weights is a complete system on its own. The 1.2 ratio keeps steps close together, which is what a dense interface needs: many distinguishable sizes rather than a few dramatic ones. IBM Plex Mono for all figures and code.

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
| `lg` | `2px` |
| `pill` | `999px` |

## Elevation

Flat. Structure comes from the grid and from one pixel rules. The e1 shadow is a single hairline offset downward rather than a blur, which reads as a printed rule rather than elevation. Only overlays get a real shadow, and only because they must separate from what is behind them.

| Level | Value |
|---|---|
| `e1` | `0 1px 0 rgba(17, 17, 17, 0.08)` |
| `e2` | `0 2px 4px rgba(17, 17, 17, 0.08), 0 6px 12px rgba(17, 17, 17, 0.06)` |
| `e3` | `0 4px 8px rgba(17, 17, 17, 0.10), 0 20px 40px rgba(17, 17, 17, 0.12)` |

## Borders

| Border | Value |
|---|---|
| `hairline` | `1px` |
| `focus-width` | `2px` |
| `focus-offset` | `2px` |

## Motion

Minimal and fast. The shortest durations of any direction. Linear-feeling eases, no overshoot, no stagger. Motion exists to confirm a state change and then get out of the way.

| Duration | Value |
|---|---|
| `fast` | `100ms` |
| `base` | `160ms` |
| `slow` | `240ms` |

| Easing | Value |
|---|---|
| `standard` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| `exit` | `cubic-bezier(0.4, 0, 1, 1)` |
| `entrance` | `cubic-bezier(0, 0, 0.2, 1)` |

Every motion token collapses to 1ms under `prefers-reduced-motion`, and each
transition keeps a non-motion way to read the state change.

## Signature details

- **Visible grid.** Content aligns to a 12 column grid whose edges are perceptible through consistent alignment, not through drawn lines.
- **Rules as structure.** One pixel rules divide content in place of cards, spanning the full column width.
- **Mono for every figure.** All numbers, IDs, timestamps, and code in IBM Plex Mono, which makes data scannable without any color.
- **One signal.** The red accent appears exactly once per view, and its absence on a screen is itself information.

## Component notes

Buttons are square cornered, with a 2px radius at most. Primary is a red fill, secondary is a one pixel border, tertiary is text. Cards are mostly absent: use a rule and a heading instead. Tables are dense, with 32px rows, hairline separators, a sticky header, and no vertical rules. Inputs are square boxes with a one pixel border that thickens on focus.

## Do

- Use rules and alignment instead of cards
- Put every figure in the monospace face
- Keep the accent to one appearance per view
- Label chart series directly rather than with a legend

## Don't

- Add shadows to create separation when a rule will do
- Round corners beyond 2px
- Use the signal red for anything that is not the single action
- Stagger list animations

## Example screen

An analytics overview. A four-column row of KPI figures across the top, each a label at the xs step, a figure at the 3xl step in mono, and a change value with an arrow glyph. A one pixel rule separates it from the chart below, which is a single line chart with direct labels at the line ends rather than a legend. The filter bar sits above the chart as square inputs. The only red on the page is the Export button.
