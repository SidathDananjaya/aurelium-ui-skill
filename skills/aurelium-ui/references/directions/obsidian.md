# Obsidian

Obsidian is what confidence looks like when it stops explaining itself. It builds on a warm near-black that reads as material rather than as an absence of light, layering surfaces by lightness so depth is felt rather than drawn. The champagne accent appears rarely enough that when it does, it means something.

**Mood.** Dark, rich, confident
**Best for.** Fintech, premium SaaS, automotive, watches, music, private banking
**Avoid for.** Children's products, medical intake, anything needing daylight warmth

Generate the tokens rather than copying the values below:

```
python scripts/tokens.py --direction obsidian --theme auto --format css
```

## Colors

| Token | Light | Dark |
|---|---|---|
| `page` | `#f7f6f4` | `#101010` |
| `surface` | `#ffffff` | `#191817` |
| `surface-raised` | `#ffffff` | `#232221` |
| `text` | `#171614` | `#f5f3ef` |
| `text-muted` | `#55524c` | `#a5a19a` |
| `border` | `#e2e0db` | `#2c2b29` |
| `accent` | `#6b5423` | `#d8bd7f` |
| `accent-hover` | `#54401a` | `#e6d09a` |
| `accent-fg` | `#ffffff` | `#101010` |
| `focus` | `#6b5423` | `#d8bd7f` |
| `success` | `#2b6140` | `#6fc48f` |
| `warning` | `#7a5310` | `#dba94f` |
| `danger` | `#8f2a22` | `#e58a7e` |
| `info` | `#28527c` | `#82b6e2` |

Every pair above is verified against WCAG AA in both themes by the repository
validator. Changing any value requires re-running the check.

## Typography

| Role | Family |
|---|---|
| Display | Fraunces |
| Body | Manrope |
| Mono | JetBrains Mono |

Fraunces at display sizes brings optical sizing and a slight wedge to the serifs that keeps it from feeling generic. Manrope handles body and UI: geometric enough to feel engineered, humanist enough to read well at 14px. JetBrains Mono carries figures in tables and transaction lists.

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
| `sm` | `8px` |
| `md` | `10px` |
| `lg` | `12px` |
| `pill` | `999px` |

## Elevation

In light mode, two shadow levels and a hairline. In dark mode, shadows stop working, so elevation is expressed entirely through surface lightness, with a one pixel top highlight at six percent white to suggest an edge catching light. This is the direction where the dark mode rule from the foundations matters most.

| Level | Value |
|---|---|
| `e1` | `0 1px 2px rgba(0, 0, 0, 0.18)` |
| `e2` | `0 2px 6px rgba(0, 0, 0, 0.22), 0 8px 20px rgba(0, 0, 0, 0.20)` |
| `e3` | `0 4px 12px rgba(0, 0, 0, 0.26), 0 24px 56px rgba(0, 0, 0, 0.32)` |

## Borders

| Border | Value |
|---|---|
| `hairline` | `1px` |
| `focus-width` | `2px` |
| `focus-offset` | `2px` |

## Motion

Precise and damped. Fast enough to feel responsive, never springy. Overshoot is wrong here. Think of a well-weighted door closing on a damper rather than a spring.

| Duration | Value |
|---|---|
| `fast` | `120ms` |
| `base` | `220ms` |
| `slow` | `360ms` |

| Easing | Value |
|---|---|
| `standard` | `cubic-bezier(0.2, 0, 0, 1)` |
| `exit` | `cubic-bezier(0.4, 0, 1, 1)` |
| `entrance` | `cubic-bezier(0.05, 0.7, 0.1, 1)` |

Every motion token collapses to 1ms under `prefers-reduced-motion`, and each
transition keeps a non-motion way to read the state change.

## Signature details

- **Lightness layering.** Three surface steps in dark mode, each a measurable step up, with no shadow anywhere.
- **The champagne hairline.** A one pixel accent rule under the active navigation item, and nowhere else.
- **Tabular everything.** Every figure in the product uses tabular lining numerals, so columns never shift.
- **Deliberate reveal.** Sensitive figures such as balances start masked and reveal on an explicit action, which reads as discretion rather than as a security feature.

## Component notes

The primary button is a champagne fill with near-black text, which is the only high-chroma area on most screens. Secondary is a hairline outline in border color. Cards use surface lightness plus the top highlight, never a shadow in dark mode. Tables are the workhorse: hairline row separators, tabular figures, right-aligned numbers, and a sticky header that keeps the hairline.

## Do

- Express dark mode elevation with lightness and a top highlight
- Reserve champagne for the single primary action per view
- Use tabular figures for every number in the product
- Keep the near-black warm, never pure #000000

## Don't

- Apply drop shadows to dark mode cards, where they are invisible
- Use champagne for decorative accents or dividers
- Let more than one element per screen carry the accent
- Add zebra striping to tables when hairlines will do

## Example screen

A private banking overview. The balance sits at the 4xl step in Fraunces on the page background with no card around it, masked until revealed. Below it, a row of three accounts as surface-level cards, each with a label, a tabular figure, and a change indicator that uses an arrow glyph as well as color. The transaction list runs full width with hairline separators and no zebra striping. One champagne button reads Transfer.
