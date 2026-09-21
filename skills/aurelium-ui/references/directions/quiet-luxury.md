# Quiet Luxury

Quiet Luxury believes the most expensive thing an interface can do is leave space empty. It draws its authority from editorial print: generous margins, a high contrast serif, and a single muted accent that never raises its voice. Nothing here is trying to impress you, which is precisely why it does.

**Mood.** Editorial, calm, warm
**Best for.** Hospitality, fashion, real estate, wellness, portfolios, editorial
**Avoid for.** Dense data tools, dashboards with many simultaneous readings

Generate the tokens rather than copying the values below:

```
python scripts/tokens.py --direction quiet-luxury --theme auto --format css
```

## Colors

| Token | Light | Dark |
|---|---|---|
| `page` | `#faf8f3` | `#15130f` |
| `surface` | `#ffffff` | `#1e1c16` |
| `surface-raised` | `#ffffff` | `#27241c` |
| `text` | `#1c1a15` | `#f3f0e7` |
| `text-muted` | `#585346` | `#aaa494` |
| `border` | `#e4dfd2` | `#332f26` |
| `accent` | `#755625` | `#cba96b` |
| `accent-hover` | `#5d4419` | `#dcbd85` |
| `accent-fg` | `#ffffff` | `#15130f` |
| `focus` | `#755625` | `#cba96b` |
| `success` | `#2c6340` | `#77c795` |
| `warning` | `#7d5310` | `#d9a84e` |
| `danger` | `#93291f` | `#e4867b` |
| `info` | `#2a5580` | `#84b7e0` |

Every pair above is verified against WCAG AA in both themes by the repository
validator. Changing any value requires re-running the check.

## Typography

| Role | Family |
|---|---|
| Display | Cormorant Garamond |
| Body | Hanken Grotesk |
| Mono | IBM Plex Mono |

Cormorant Garamond carries the display sizes, where its high stroke contrast and small x-height read as bookish rather than corporate. It is too delicate below 24px, so Hanken Grotesk takes everything from body size down. The 1.333 ratio produces large jumps, which suits a layout with few elements per screen.

Base 17px, ratio 1.333.

| Step | Size | Pixels |
|---|---|---|
| `2xs` | `0.563rem` | 9.6px |
| `xs` | `0.75rem` | 12.8px |
| `base` | `1.0rem` | 17.0px |
| `lg` | `1.333rem` | 22.7px |
| `xl` | `1.777rem` | 30.2px |
| `2xl` | `2.369rem` | 40.3px |
| `3xl` | `3.157rem` | 53.7px |
| `4xl` | `4.209rem` | 71.5px |
| `5xl` | `5.61rem` | 95.4px |

## Spacing

Base grid 4px, multiplier 1.25. Inner spacing is always smaller
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
| `sm` | `2px` |
| `md` | `4px` |
| `lg` | `6px` |
| `pill` | `999px` |

## Elevation

Depth comes from hairlines, not shadows. A one pixel warm grey rule separates sections more convincingly here than any elevation would. Shadows exist for overlays only, and they stay soft enough to read as diffused daylight rather than a drop shadow.

| Level | Value |
|---|---|
| `e1` | `0 1px 2px rgba(28, 26, 21, 0.05)` |
| `e2` | `0 2px 6px rgba(28, 26, 21, 0.07), 0 8px 20px rgba(28, 26, 21, 0.06)` |
| `e3` | `0 4px 10px rgba(28, 26, 21, 0.09), 0 24px 56px rgba(28, 26, 21, 0.12)` |

## Borders

| Border | Value |
|---|---|
| `hairline` | `1px` |
| `focus-width` | `2px` |
| `focus-offset` | `2px` |

## Motion

Slow and soft. Durations run longer than any other direction because the mood is unhurried. Fades and gentle upward reveals only. Nothing springs, nothing bounces.

| Duration | Value |
|---|---|
| `fast` | `160ms` |
| `base` | `280ms` |
| `slow` | `480ms` |

| Easing | Value |
|---|---|
| `standard` | `cubic-bezier(0.25, 0, 0.15, 1)` |
| `exit` | `cubic-bezier(0.4, 0, 1, 1)` |
| `entrance` | `cubic-bezier(0, 0, 0.2, 1)` |

Every motion token collapses to 1ms under `prefers-reduced-motion`, and each
transition keeps a non-motion way to read the state change.

## Signature details

- **Rules, not boxes.** Sections divide with a hairline that stops short of the container edge, the way a printed page uses a partial rule.
- **Drop caps on the opening paragraph** of long-form content, set in the display serif at three lines deep.
- **Asymmetric hero.** Display text sits on a two-thirds column with the remaining third left deliberately empty, never filled.
- **Letterpress numerals.** Key figures set in the display serif with oldstyle figures where the face supports them, for running prose only.

## Component notes

Buttons are text-first: the primary is a filled bronze rectangle with a 2px radius, the secondary is a hairline outline, the tertiary is an underlined text link. Cards rarely have a visible boundary. Group with space, and if that is not enough, use a hairline on one edge only. Inputs are underlined rather than boxed, with the label above in small caps tracked out.

## Do

- Let a section breathe at 128px or more of vertical padding at desktop
- Use the serif only at 24px and above
- Keep the accent for the single booking or purchase action
- Set body copy at a 68 character measure

## Don't

- Add a shadow to a card because it looks empty
- Set the serif at body size, where it turns spindly
- Introduce a second accent for a secondary action
- Fill the empty third of an asymmetric hero

## Example screen

A boutique hotel landing page. The hero is a single wide photograph of the property at 16:9 with the hotel name set in Cormorant Garamond at the 5xl step, left aligned on the lower third, over a gradient scrim. Below, three stacked sections at 160px vertical rhythm: the rooms, the restaurant, the location. Each is a two-column split of one image and one short paragraph at 68 characters. The booking action is the only bronze element on the page.
