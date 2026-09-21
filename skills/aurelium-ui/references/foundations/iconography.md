# Iconography

Icons are a typeface, not a collection. They come from one family, share one
stroke weight, and sit on one optical grid.

## One family, no exceptions

Pick a single open-licensed icon set and use only that set. Mixing families is
the fastest way to make an interface look assembled rather than designed,
because stroke weight, corner radius, and optical density never match.

**Check.** Open every SVG in the project. Every icon shares the same stroke
width, the same cap and join style, and the same nominal grid size.

If the set lacks an icon you need, draw it on the same grid with the same stroke
values. Never import one icon from elsewhere.

## Stroke and grid

| Property | Rule |
|---|---|
| Grid | One nominal size for the set, commonly 24 by 24 |
| Stroke width | One value, commonly 1.5px or 2px at 24px |
| Cap and join | `round` throughout, or `butt` and `miter` throughout |
| Corner radius | Consistent across the set |
| Alignment | Strokes sit on half-pixel centres so they render crisply |

Stroke width does not scale linearly with size. An icon drawn at 24px with a
1.5px stroke, scaled to 48px, has an apparent 3px stroke and looks heavy.
Redraw, or use a variable icon font with an optical size axis.

```css
.icon {
  inline-size: 1.25em;
  block-size: 1.25em;
  stroke-width: 1.5;
  /* Scales with the text it sits beside */
  vertical-align: -0.125em;
}
```

Use `currentColor` for stroke and fill so icons inherit text color, including in
dark mode and inside a button's hover state.

```html
<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
     stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
     aria-hidden="true" focusable="false">
  <path d="M5 12h14M13 6l6 6-6 6" />
</svg>
```

## Optical sizing, not mathematical sizing

Icons of the same declared size do not look the same size. A filled circle looks
larger than an outlined square at identical dimensions. Adjust the artwork, not
the box.

- Circular and round forms are drawn 2 to 4 percent larger than square ones.
- A triangle pointing right is nudged right of centre, because its visual mass
  sits left.
- Diagonal forms need slightly more bounding box than orthogonal ones.

Every correction carries a comment so a later reader does not undo it.

## Alignment with text

An icon beside a label aligns on the cap height of the text, not on the text
box and not on the baseline.

```css
.button {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
}
```

Flexbox centring handles most cases. When it does not, nudge with `transform`,
never with `margin`, so the layout box stays honest.

Icon and label gap is `--space-2` at body size, tightening to `--space-1` in
dense UI.

## Icons never replace labels for critical actions

An icon alone is ambiguous for anything except a small set of universally
understood symbols: close, search, menu, back, and play.

| Action | Icon alone | Icon plus label |
|---|---|---|
| Close a dialog | Acceptable | Better |
| Search | Acceptable | Better |
| Delete, archive, share, export, publish | **Never** | Required |
| Primary action of any kind | **Never** | Required |
| Toolbar action in a dense professional tool | Acceptable with a tooltip **and** an accessible name | Better |

**Check.** Cover every label in a screenshot. Any action whose meaning becomes
ambiguous needs its label back.

A tooltip is not a label. It is unavailable on touch, delayed on pointer, and
invisible to a user scanning quickly.

## Accessibility

Decorative icons are hidden from assistive technology. Meaningful icons carry a
name.

```html
<!-- Decorative: the label beside it already says everything -->
<button>
  <svg aria-hidden="true" focusable="false">...</svg>
  Export
</button>

<!-- Meaningful: the icon is the only content -->
<button aria-label="Close dialog">
  <svg aria-hidden="true" focusable="false">...</svg>
</button>
```

`focusable="false"` matters because some engines make SVG focusable by default,
which inserts phantom tab stops.

Icon-only buttons still need a 44 by 44 target. Pad the button, do not enlarge
the glyph.

## Never use emoji as icons

Emoji render differently on every platform, cannot inherit color, cannot match
stroke weight, are announced verbosely by screen readers, and carry a casual
register that undermines premium work.

**Do.** A drawn SVG on the project grid.
**Don't.** A rocket, sparkles, or a check mark emoji in a button, heading, or
empty state.

This applies to generated copy as well as to components.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Two or more icon families | Mismatched weight and density | One family, draw missing icons to match |
| Scaling a 24px icon to 48px | Apparent stroke doubles | Redraw, or use optical size axis |
| Emoji in place of icons | Platform inconsistency, wrong register | Drawn SVG |
| Icon-only destructive action | Users cannot predict the outcome | Add the label |
| Tooltip used as the only label | Unavailable on touch, invisible when scanning | Visible label, or an accessible name plus tooltip |
| Hard-coded icon color | Breaks in dark mode and on hover | `currentColor` |
| Enlarging the glyph to reach 44px | Icon looks oversized | Pad the button instead |
| Icons at arbitrary sizes | Optical inconsistency across the product | Size from the type scale |
