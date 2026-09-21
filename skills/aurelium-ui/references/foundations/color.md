# Color

Neutrals do about 90 percent of the work. One accent. Semantic colors only when
they carry meaning. Color is the last tool you reach for to create hierarchy,
after size, weight, and spacing.

## The palette structure

Every Aurelium palette has exactly four parts.

| Part | Count | Purpose |
|---|---|---|
| Neutral ramp | 10 to 12 steps | Backgrounds, surfaces, borders, text |
| Accent | 1 hue, 3 to 5 steps | The single primary action, focus, selection |
| Semantic | 4 hues | Success, warning, danger, info |
| Alpha overlays | 2 to 4 | Scrims, hover washes, dividers |

**Check.** Count distinct hues outside the neutral ramp and the semantic set.
The answer is 1.

## Neutrals are never pure grey

A neutral ramp built from pure grey looks cheap because nothing in the physical
world is pure grey. Tint every step toward a hue and keep the tint consistent
across the ramp.

| Temperature | Tint toward | Reads as | Suits |
|---|---|---|---|
| Warm | Yellow or red, hue 30 to 60 | Paper, stone, linen | Hospitality, editorial, fashion, wellness |
| Cool | Blue, hue 210 to 240 | Glass, steel, screen | Fintech, dev tools, analytics, security |

**Do.** Build the ramp in a perceptual space so steps feel evenly spaced.

```css
:root {
  /* Warm neutral ramp, constant hue and chroma, lightness stepped */
  --neutral-50:  oklch(98.2% 0.006 70);
  --neutral-100: oklch(96.0% 0.008 70);
  --neutral-200: oklch(91.5% 0.010 70);
  --neutral-300: oklch(84.0% 0.011 70);
  --neutral-400: oklch(71.0% 0.012 70);
  --neutral-500: oklch(58.5% 0.012 70);
  --neutral-600: oklch(47.5% 0.011 70);
  --neutral-700: oklch(38.0% 0.010 70);
  --neutral-800: oklch(27.5% 0.009 70);
  --neutral-900: oklch(19.0% 0.008 70);
  --neutral-950: oklch(13.0% 0.007 70);
}
```

**Don't.** Mix a warm ramp with a cool accent without deciding that the clash is
the point. Most of the time it reads as an accident.

## Never pure black on pure white

`#000000` text on `#ffffff` at body size produces halation that tires the eye
over long reading. Pull both ends in.

**Do.** Text at `--neutral-900`, page at `--neutral-50`. Roughly 16:1, which is
still far above AA.
**Don't.** `#000` on `#fff` for anything longer than a label.

Pure white is still correct for a raised surface sitting on a tinted page.

## Choosing the accent

The accent marks the one thing that matters on a screen. Pick it by what it must
survive, not by what looks appealing in isolation.

1. It must reach 4.5:1 against the page background when used as text.
2. It must reach 3:1 as a fill behind white or near-white label text.
3. It must remain distinguishable from the danger color for a viewer with
   deuteranopia or protanopia. Never let the accent sit near red if danger does.
4. It needs a usable dark mode counterpart, which usually means raising
   lightness and cutting chroma.

**Do.** Deep bronze, forest, oxblood, slate blue, or champagne for restrained
work. A single saturated signal color for Swiss or futurist work.
**Don't.** Use a gradient as the accent. A gradient cannot be a token, cannot be
contrast checked reliably, and cannot be reused at small sizes.

## Semantic colors

Four meanings, and only these four. Each needs a text-safe step and a
surface-safe step.

```css
:root {
  --color-success: oklch(52% 0.13 150);
  --color-success-surface: oklch(96% 0.03 150);
  --color-warning: oklch(58% 0.14 75);
  --color-warning-surface: oklch(96% 0.04 75);
  --color-danger: oklch(53% 0.19 25);
  --color-danger-surface: oklch(96% 0.04 25);
  --color-info: oklch(55% 0.11 240);
  --color-info-surface: oklch(96% 0.03 240);
}
```

Semantic color never appears for decoration. A green card that is not reporting
success is a bug.

**Never carry meaning by color alone.** Pair every semantic color with an icon
or a word. See `../doctrine/accessibility.md`.

## Dark mode is not an inversion

Inverting a light palette produces glare and destroys depth. Build dark mode on
a different principle: in light mode elevation comes from shadow, in dark mode
elevation comes from lightness.

| Layer | Light mode | Dark mode |
|---|---|---|
| Page | `--neutral-50` | `--neutral-950` |
| Surface | white, plus shadow | `--neutral-900`, no shadow needed |
| Raised surface | white, deeper shadow | `--neutral-800` |
| Border | `--neutral-200` | `--neutral-800`, or a white alpha |

Rules that hold in every dark palette:

- The page is never `#000000`. Use a near-black around 13 percent lightness so
  surfaces have somewhere to go.
- Body text is never pure white. Around 92 to 95 percent lightness.
- Reduce accent chroma by roughly 20 to 30 percent. Saturated hues vibrate
  against dark backgrounds.
- Shadows mostly stop working. Express elevation with lightness and a 1px top
  highlight instead.

```css
:root {
  --color-page: var(--neutral-50);
  --color-surface: #ffffff;
  --color-text: var(--neutral-900);
  --shadow-e1: 0 1px 2px oklch(0% 0 0 / 0.08);
}

[data-theme="dark"] {
  --color-page: var(--neutral-950);
  --color-surface: var(--neutral-900);
  --color-text: var(--neutral-100);
  --shadow-e1: none;
  --highlight-top: inset 0 1px 0 oklch(100% 0 0 / 0.06);
}
```

## Declaring contrast pairs

Every foreground and background combination the product actually uses is
declared, so it can be checked mechanically rather than by eye.

```css
/* contrast-pairs: text:page, text-muted:page, text:surface, accent-fg:accent */
```

**Check.** Every declared pair meets the minimum in `../doctrine/accessibility.md`.
Muted text is the pair that fails most often. If `--text-muted` cannot reach
4.5:1, it is too light, regardless of how it looks.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Purple to pink gradient on a dark hero | The default look of generic AI output. Instantly dates the work | One accent, flat, on a considered neutral |
| Low contrast grey body text | Fails AA, and reads as unfinished rather than subtle | Use a muted step that still clears 4.5:1 |
| A different color per card or category | Destroys hierarchy, nothing reads as primary | Neutral surfaces, one accent on the primary action |
| Gradient text for body copy | Unreadable at small sizes, uncheckable for contrast | Solid color. Reserve gradients for large display type, if at all |
| Glassmorphism over a busy background | Contrast becomes unpredictable and uncheckable | Blur over a controlled surface, or use a solid scrim |
| Semantic red used as a brand accent | Users cannot tell an error from a button | Choose an accent far from the danger hue |
| Pure `#000` dark mode | No room for elevation, high glare | Near-black around 13 percent lightness |

## Format guidance

Author tokens in `oklch()` where the toolchain allows. Perceptual lightness means
a ramp built by stepping the first value actually looks evenly stepped, and
holding chroma constant while changing hue keeps intensity consistent.

Provide a hex or `rgb()` fallback when supporting older engines:

```css
:root {
  --accent: #8a6d2f;
}

@supports (color: oklch(50% 0.1 70)) {
  :root {
    --accent: oklch(52% 0.075 78);
  }
}
```
