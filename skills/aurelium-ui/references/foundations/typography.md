# Typography

Typography carries the brand. Hierarchy comes from size, then weight, then
spacing, and only then color. Maximum two families, plus one monospace face for
data.

## The type scale

Build the scale from a base size and a ratio. Every size in the product comes
from the scale. There are no in-between values.

| Density dial | Base | Ratio | Character |
|---|---|---|---|
| 1 to 3, spacious | 17 to 18px | 1.333 | Editorial, few sizes per screen, large jumps |
| 4 to 6, balanced | 16px | 1.25 | Product default |
| 7 to 10, dense | 14 to 15px | 1.2 | Professional tool, many steps close together |

```css
:root {
  --text-xs:   0.79rem;  /* 12.6px */
  --text-sm:   0.889rem; /* 14.2px */
  --text-base: 1rem;     /* 16px   */
  --text-lg:   1.125rem; /* 18px   */
  --text-xl:   1.266rem; /* 20.3px */
  --text-2xl:  1.424rem; /* 22.8px */
  --text-3xl:  1.802rem; /* 28.8px */
  --text-4xl:  2.281rem; /* 36.5px */
  --text-5xl:  2.887rem; /* 46.2px */
  --text-6xl:  3.653rem; /* 58.5px */
}
```

**Check.** Grep for `font-size` values that are not scale tokens. Zero results.

Body text is never below 16px on mobile. Anything smaller triggers zoom on iOS
input focus and fails readability for many users.

## Fluid display sizes

Display type should scale with the viewport rather than jump at breakpoints.
Clamp between a mobile minimum and a desktop maximum.

```css
:root {
  --text-display: clamp(2.5rem, 1.6rem + 4.2vw, 4.5rem);
}
```

Never let the minimum fall below what is readable at 320px, and never let the
maximum exceed what fits the measure at 1440px.

## Line height by size

Line height is inversely proportional to size. Large text needs proportionally
less leading, small text needs more.

| Size range | Line height |
|---|---|
| Display, 36px and above | 1.0 to 1.1 |
| Headings, 20 to 36px | 1.15 to 1.3 |
| Body, 15 to 19px | 1.5 to 1.65 |
| Small and captions, 12 to 14px | 1.4 to 1.5 |

**Do.** Set `line-height: 1.55` on body copy and `1.05` on a 56px hero.
**Don't.** Apply one line height to the whole document.

## Measure

Reading text sits between 60 and 75 characters per line. Below 45 the eye jumps
too often. Above 85 it loses the line return.

```css
.prose {
  max-inline-size: 68ch;
}
```

**Check.** Paste a paragraph at desktop width and count characters in one line.
Between 60 and 75 for article text. UI text in cards may run shorter.

## Tracking

Tracking is a function of size. Large type needs negative tracking, small
uppercase needs positive.

| Context | Letter spacing |
|---|---|
| Display, 40px and above | -0.02em to -0.03em |
| Headings, 20 to 36px | -0.01em to -0.02em |
| Body | 0 |
| Small caps and uppercase labels | 0.04em to 0.10em |

**Don't.** Track out lowercase body text to fill a space. It damages word shape
recognition.

## Weight

Hierarchy needs no more than four weights across the entire product. Two is
often enough.

- Body: 400.
- Emphasis and UI labels: 500 or 600.
- Headings: 600 or 700.
- Display: whatever the face is strongest at, often 300 for a high contrast
  serif or 700 for a grotesk.

Never synthesise a weight. If the face lacks 600, use 500 or 700, and never let
the browser create a faux bold. Never use faux italic.

## Numbers

Any figure that changes, aligns in a column, or sits in a table uses tabular
lining figures. Otherwise digits shift width and the column appears to wobble.

```css
.metric,
.data-table td,
.timer {
  font-variant-numeric: tabular-nums lining-nums;
  font-feature-settings: "tnum" 1, "lnum" 1;
}
```

**Check.** Watch a live-updating number. No horizontal movement.

Use proportional figures for running prose, where tabular digits look spaced out.

## Text wrapping

Progressive enhancement. These improve ragging where supported and do nothing
where not.

```css
h1, h2, h3, .headline {
  text-wrap: balance;
}

p, li {
  text-wrap: pretty;
}
```

Prevent single-word last lines in short headings, and never let a heading break
mid-word. Use `hyphens: none` for headings and `overflow-wrap: anywhere` only on
user-generated strings that could be unbroken, such as a long email address.

## Pairing families

The pairing rule is contrast in structure, harmony in proportion. Pair a serif
with a grotesk, or a grotesk with a mono. Never pair two faces from the same
classification, which reads as a mistake rather than a choice.

Match x-height and apparent size between the two faces. If the body face looks
smaller at the same declared size, adjust by a step rather than accepting the
mismatch.

### Verified font list

Every face below is distributed under the **SIL Open Font License, Version 1.1**
and is available on Google Fonts. Licences were verified against the
`google/fonts` repository, where each family directory carries its own
`OFL.txt`, on 21 September 2026.

| Family | Classification | Use for |
|---|---|---|
| Cormorant Garamond | High contrast serif | Editorial display, hospitality, fashion |
| Instrument Serif | Display serif | Large headlines with personality |
| Newsreader | Text serif | Long-form reading |
| Fraunces | Variable display serif | Expressive headlines with optical sizing |
| Hanken Grotesk | Neo-grotesk | Body and UI, neutral and precise |
| Manrope | Geometric grotesk | Body and UI, warm and modern |
| Figtree | Humanist sans | Consumer products, friendly tone |
| Schibsted Grotesk | Neo-grotesk | Swiss and editorial UI |
| Geist | Grotesk | Technical products and dev tools |
| Space Grotesk | Grotesk with quirk | Futurist and technical headlines |
| IBM Plex Mono | Monospace | Data, code, tabular labels |
| JetBrains Mono | Monospace | Data and code, tall x-height |

Before adding any face to this list, confirm its licence at the source. A font
being free on a webfont host does not make it OFL.

## Loading

Two families maximum, four total weights and styles maximum. Prefer variable
fonts, which deliver a weight range in one file.

```css
@font-face {
  font-family: "Body";
  src: url("/fonts/body-variable.woff2") format("woff2-variations");
  font-weight: 300 700;
  font-display: swap;
}

:root {
  --font-body: "Body", ui-sans-serif, system-ui, -apple-system, "Segoe UI",
    sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
}
```

Always declare a fallback stack with similar metrics, and tune the swap with
`size-adjust` so no layout shift occurs. See `../doctrine/performance.md`.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Three or more display families | Reads as indecision | Two families, plus mono for data |
| Body text under 16px on mobile | Triggers zoom, fails readability | 16px minimum |
| Centered long-form paragraphs | Ragged left edge destroys the line return | Left align body, centre only short display text |
| All-caps for a full sentence | Removes word shape, slows reading | Sentence case, reserve caps for short labels |
| Uniform line height everywhere | Headings look loose, body looks cramped | Line height by size band |
| Proportional figures in a data table | Columns wobble | `tabular-nums` |
| Letter spacing on lowercase body | Damages word recognition | Zero tracking at body size |
| Faux bold or faux italic | Distorted letterforms | Load the real weight, or restyle |
