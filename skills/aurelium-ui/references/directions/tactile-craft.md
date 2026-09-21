# Tactile Craft

Tactile Craft treats an interface as an object with weight, not a diagram of one. Stone and clay neutrals, soft radii, and diffused shadows give surfaces the sense of resting on something rather than floating above it. Motion here has mass: things settle rather than snap.

**Mood.** Tactile, crafted, human
**Best for.** Consumer apps, booking, food, lifestyle, e-commerce, community
**Avoid for.** Enterprise admin, dense analytics, anything demanding severity

Generate the tokens rather than copying the values below:

```
python scripts/tokens.py --direction tactile-craft --theme auto --format css
```

## Colors

| Token | Light | Dark |
|---|---|---|
| `page` | `#f6f3ee` | `#1a1714` |
| `surface` | `#fffdfa` | `#24201c` |
| `surface-raised` | `#ffffff` | `#2e2924` |
| `text` | `#22201c` | `#f4f0ea` |
| `text-muted` | `#5b554c` | `#aaa398` |
| `border` | `#e0d9cd` | `#3a342d` |
| `accent` | `#8a4423` | `#e08a5f` |
| `accent-hover` | `#6f3519` | `#eda47c` |
| `accent-fg` | `#ffffff` | `#1a1714` |
| `focus` | `#8a4423` | `#e08a5f` |
| `success` | `#2f6440` | `#77c795` |
| `warning` | `#7d5310` | `#d9a84e` |
| `danger` | `#96291f` | `#e4867b` |
| `info` | `#2a5580` | `#84b7e0` |

Every pair above is verified against WCAG AA in both themes by the repository
validator. Changing any value requires re-running the check.

## Typography

| Role | Family |
|---|---|
| Display | Figtree |
| Body | Figtree |
| Mono | IBM Plex Mono |

Figtree does both display and body. A single humanist family is the right call here because the warmth comes from the palette and the shapes, not from a typographic contrast. It stays friendly at large sizes without turning novelty, and its round terminals agree with the soft radii.

Base 16px, ratio 1.25.

| Step | Size | Pixels |
|---|---|---|
| `2xs` | `0.64rem` | 10.2px |
| `xs` | `0.8rem` | 12.8px |
| `base` | `1.0rem` | 16.0px |
| `lg` | `1.25rem` | 20.0px |
| `xl` | `1.562rem` | 25.0px |
| `2xl` | `1.953rem` | 31.2px |
| `3xl` | `2.441rem` | 39.1px |
| `4xl` | `3.052rem` | 48.8px |
| `5xl` | `3.815rem` | 61.0px |

## Spacing

Base grid 4px, multiplier 1.0. Inner spacing is always smaller
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
| `sm` | `12px` |
| `md` | `16px` |
| `lg` | `20px` |
| `pill` | `999px` |

## Elevation

The only direction where shadows do most of the work. They are soft, multi-layer, and tinted toward the warm neutral rather than black, which is what keeps them feeling like daylight on clay instead of a drop shadow in a graphics program.

| Level | Value |
|---|---|
| `e1` | `0 1px 3px rgba(34, 32, 28, 0.07)` |
| `e2` | `0 3px 8px rgba(34, 32, 28, 0.09), 0 10px 24px rgba(34, 32, 28, 0.08)` |
| `e3` | `0 6px 14px rgba(34, 32, 28, 0.11), 0 28px 60px rgba(34, 32, 28, 0.14)` |

## Borders

| Border | Value |
|---|---|
| `hairline` | `1px` |
| `focus-width` | `2px` |
| `focus-offset` | `3px` |

## Motion

Physical and weighted. The standard easing has a pronounced deceleration so elements arrive and settle. Slightly longer than Swiss or Futurism, slightly shorter than Quiet Luxury. Gestures may use a spring, utility actions never do.

| Duration | Value |
|---|---|
| `fast` | `140ms` |
| `base` | `240ms` |
| `slow` | `400ms` |

| Easing | Value |
|---|---|
| `standard` | `cubic-bezier(0.32, 0.72, 0, 1)` |
| `exit` | `cubic-bezier(0.4, 0, 1, 1)` |
| `entrance` | `cubic-bezier(0.05, 0.7, 0.1, 1)` |

Every motion token collapses to 1ms under `prefers-reduced-motion`, and each
transition keeps a non-motion way to read the state change.

## Signature details

- **Settled arrival.** Elements enter with a decelerating ease that reads as weight coming to rest, never as a bounce.
- **Nested concentric radii.** Media inside a card uses the outer radius minus the padding, so the curves stay parallel.
- **Warm shadow.** Every shadow is tinted toward the clay neutral, so no surface ever looks grey.
- **Generous targets.** Touch targets run to 48px, above the 44px recommendation, because the audience is usually on a phone.

## Component notes

Buttons are pill or 16px radius, with a terracotta fill for primary and a filled neutral surface for secondary rather than an outline. Cards are the primary container: a warm surface, 16px radius, soft shadow, 24px padding. Inputs are filled rather than outlined, with a 12px radius and a visible label above.

## Do

- Tint shadows toward the warm neutral
- Keep nested radii concentric
- Use filled secondary buttons rather than outlines
- Run touch targets to 48px

## Don't

- Use pure black shadows, which turn the palette grey
- Mix a 20px card radius with a 4px button radius
- Apply a spring to a utility action such as save
- Let the soft radii drift larger on every new component

## Example screen

A restaurant booking flow. Step one is a date strip of pill-shaped day buttons that scroll horizontally, with the selected day filled in terracotta. Step two is a grid of time slots as cards, unavailable ones at reduced opacity with a strikethrough rather than color alone. The confirmation screen is a single card holding the restaurant name, the party size, the time in tabular figures, and a calm line stating when the booking can be changed until.
