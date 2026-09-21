# Surfaces and depth

Elevation expresses hierarchy, never decoration. If an element is not on a
genuinely higher layer, it does not get a shadow.

## Three levels, no more

| Level | Meaning | Light mode | Dark mode |
|---|---|---|---|
| Base | The page itself | Page background, no shadow | Page background, no shadow |
| e1, raised | Sits on the page: cards, panels, sticky bars | Subtle shadow or hairline | Lighter surface, no shadow |
| e2, overlay | Floats above content: dropdowns, popovers, toasts | Medium shadow | Lighter still, plus a top highlight |
| e3, modal | Blocks the page: dialogs, drawers | Deep shadow plus a scrim | Lightest surface, plus a scrim |

**Check.** Count distinct shadow tokens in use. Three or fewer. Every shadowed
element genuinely sits above its parent in the stacking order.

## Shadows describe one light source

A shadow implies light. One light source per interface, always from above, so
every shadow offsets downward by the same proportion. Mixed directions read as a
rendering error.

Real shadows are two shadows: a tight contact shadow and a soft ambient one.

```css
:root {
  --shadow-e1:
    0 1px 2px oklch(0% 0 0 / 0.06),
    0 1px 3px oklch(0% 0 0 / 0.10);
  --shadow-e2:
    0 2px 4px oklch(0% 0 0 / 0.06),
    0 8px 16px oklch(0% 0 0 / 0.10);
  --shadow-e3:
    0 4px 8px oklch(0% 0 0 / 0.08),
    0 24px 48px oklch(0% 0 0 / 0.16);
}
```

Tint shadows toward the palette rather than using neutral black. A warm palette
takes a warm shadow. Pure black shadows on a warm page look grey and dead.

**Do.** Increase blur and vertical offset together as elevation rises.
**Don't.** Increase opacity alone. That produces a dark smudge, not height.

## Dark mode replaces shadow with lightness

A shadow against a near-black background is invisible. Express elevation by
raising surface lightness, and add a one pixel top highlight to suggest a
catching edge.

```css
[data-theme="dark"] {
  --surface-e1: var(--neutral-900);
  --surface-e2: var(--neutral-800);
  --surface-e3: var(--neutral-750, var(--neutral-800));
  --shadow-e1: none;
  --highlight: inset 0 1px 0 oklch(100% 0 0 / 0.06);
}

[data-theme="dark"] .card {
  background: var(--surface-e1);
  box-shadow: var(--highlight);
}
```

Keep the scrim behind modals in both themes. It is what makes the dialog read as
blocking.

## Borders versus shadows

Reach for these in order. Stop at the first one that works.

1. **Space.** Separate with distance. Costs nothing, always works.
2. **Surface.** A different background lightness.
3. **Hairline.** A one pixel border.
4. **Shadow.** Only when the element genuinely floats.

Most interfaces that feel busy have skipped straight to step four.

## Hairlines

A hairline is a structural line, not a decorative one. It is the lightest border
that remains visible.

```css
:root {
  --border-hairline: 1px solid var(--neutral-200);
}

[data-theme="dark"] {
  --border-hairline: 1px solid oklch(100% 0 0 / 0.08);
}
```

In dark mode, prefer a white alpha over a solid grey. It stays consistent over
any surface lightness beneath it.

For a true hairline on high density displays:

```css
@media (min-resolution: 2dppx) {
  .hairline { border-width: 0.5px; }
}
```

Borders that carry meaning, such as a focus ring or a selected state, need 3:1
contrast. Purely decorative dividers do not.

## Radius

Radius is a voice, not a decoration. Pick one scale and hold it.

| Character | Radius | Reads as |
|---|---|---|
| Sharp | 0 to 2px | Swiss, technical, precise |
| Restrained | 4 to 8px | Editorial, refined |
| Soft | 10 to 16px | Product, approachable |
| Round | 18px and above, or pill | Consumer, tactile, playful |

Nested radii must be concentric, or the gap between them looks wrong. The inner
radius equals the outer radius minus the padding between them.

```css
.card {
  --card-radius: 12px;
  border-radius: var(--card-radius);
  padding: var(--space-2);
}

.card > .media {
  /* Concentric: 12px outer minus 8px padding */
  border-radius: calc(var(--card-radius) - var(--space-2));
}
```

An inner radius larger than its outer radius is always a mistake.

## Texture

Texture is an opulence dial feature. At opulence 1 to 3 there is none. At 4 to 6
there may be one subtle treatment. At 7 and above texture can carry the surface.

The budget: any texture must be procedural or under 4KB, must not tile visibly,
and must not affect contrast enough to change a pass into a fail.

```css
.grain::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
```

**Check.** Run the contrast check with the texture applied. The result does not
change.

## Blur and translucency

Backdrop blur is expensive and makes contrast unpredictable. Use it only over a
surface you control, and always put a semi-opaque background behind it so the
content stays legible if blur is unsupported or disabled.

```css
.sticky-header {
  background: oklch(from var(--color-page) l c h / 0.85);
  backdrop-filter: blur(12px);
}

@supports not (backdrop-filter: blur(1px)) {
  .sticky-header { background: var(--color-page); }
}
```

Never blur over arbitrary user content, such as a photo gallery. The contrast
cannot be guaranteed.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| A shadow on every card | Elevation stops meaning anything | Hairline or surface change, shadow only when floating |
| More than three elevation levels | No one can perceive the difference | Three |
| Shadows in several directions | Implies several light sources | One source, from above |
| Pure black shadow on a warm page | Reads grey and dead | Tint the shadow toward the palette |
| Inverting the palette for dark mode | Glare, and depth disappears | Lightness-based elevation |
| Inner radius larger than outer | Looks broken | Concentric radii |
| Glassmorphism over busy imagery | Contrast becomes unpredictable | Solid scrim, or blur over a controlled surface |
| Visible repeating texture tile | Cheapens the surface immediately | Procedural noise, very low opacity |
