# Accessibility baseline

Target: WCAG 2.2 level AA. This is the floor, not the goal. Every item here is
verifiable. Nothing ships that fails one.

## Contrast

| Content | Minimum ratio |
|---|---|
| Body text | 4.5:1 |
| Large text, meaning 24px regular or 18.66px bold and above | 3:1 |
| UI component boundaries and meaningful graphics | 3:1 |
| Focus indicator against the adjacent background | 3:1 |

**Check.** Run `../../scripts/contrast.py` over every declared foreground and
background pair in the token set. Every pair passes. Disabled controls are exempt from the
text minimum, but never rely on a disabled state to convey information.

Never use color alone to carry meaning. Pair every semantic color with an icon,
a text label, or a pattern.

```css
/* Not enough on its own */
.status-error { color: var(--color-danger); }

/* Sufficient: color plus a glyph and a word */
.status-error::before { content: "\26A0"; margin-inline-end: var(--space-2); }
```

## Focus

Every interactive element has a visible, designed focus indicator. Focus is
never removed, and never hidden behind a sticky header.

```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}

/* Remove the default only where a custom indicator replaces it */
:focus:not(:focus-visible) { outline: none; }

/* Keeps a focused element clear of a sticky header */
:root { scroll-padding-block-start: var(--header-height); }
```

**Check.** Tab through every screen. Every stop is visible without scrolling
manually, and the order matches the visual order.

## Target size

Minimum 24 by 24 CSS pixels for any pointer target. Aim for 44 by 44 for
primary actions and anything used on touch.

Padding counts toward the target. A 16px icon with 14px padding meets 44px.

```css
.icon-button {
  display: inline-grid;
  place-items: center;
  inline-size: 44px;
  block-size: 44px;
}
```

**Check.** Measure the smallest interactive element on each screen. Inline links
inside a paragraph are exempt.

## Keyboard operation

- Every function is reachable and operable by keyboard alone.
- Tab order follows the visual order. Avoid positive `tabindex` values.
- `Esc` closes every overlay.
- Focus is trapped inside a modal while it is open, and returned to the element
  that opened it on close.
- A skip link is the first focusable element on the page.

```html
<a class="skip-link" href="#main">Skip to content</a>
```

```css
.skip-link {
  position: absolute;
  inset-block-start: var(--space-2);
  inset-inline-start: var(--space-2);
  padding: var(--space-2) var(--space-4);
  background: var(--color-surface);
  transform: translateY(-200%);
}
.skip-link:focus-visible { transform: translateY(0); }
```

**Check.** Unplug the mouse. Complete the primary task on every screen.

## Semantic HTML first

Use the element that already carries the behaviour. Reach for ARIA only when no
element fits.

| Need | Use | Not |
|---|---|---|
| An action | `button` | `div` with a click handler |
| Navigation | `nav` with `ul` and `a` | a list of `span` elements |
| A dialog | `dialog`, or a role with full focus management | an absolutely positioned `div` |
| A data grid | `table` with `th` and `scope` | nested `div` elements |
| Grouped fields | `fieldset` with `legend` | a heading above inputs |

**Check.** Disable CSS. The page still reads as a sensible document with a
correct heading order: one `h1`, no skipped levels.

## Forms

- Every field has a visible label. A placeholder is not a label.
- Errors are specific, adjacent to the field, and linked with
  `aria-describedby`.
- The invalid field is marked with `aria-invalid` and receives focus on submit.
- Required fields are marked in text, not by color or an asterisk alone.
- Autocomplete tokens are set on personal data fields.

```html
<label for="email">Email address</label>
<input
  id="email"
  type="email"
  autocomplete="email"
  aria-describedby="email-hint email-error"
  aria-invalid="true"
/>
<p id="email-hint">We use this for your booking confirmation.</p>
<p id="email-error">Add the part after the @, for example name@example.com.</p>
```

## Motion

Respect `prefers-reduced-motion` with a real alternative, not a blanket removal.
A state change still needs to read as a change.

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Prefer per-component handling where the motion carries meaning: replace a slide
with a cross-fade rather than removing the transition entirely.

**Check.** Enable the reduced-motion setting. Every transition still
communicates its state change. Nothing becomes ambiguous.

## Reflow and zoom

Content reflows at 320 CSS pixels wide and at 200 percent zoom with no loss of
content or function, and no horizontal scrolling of the page.

**Check.** Set the viewport to 320px. Then set zoom to 200 percent at 1280px.
No horizontal scrollbar, no clipped text, no overlapping controls.

## Screen reader essentials

- Images that carry meaning have descriptive `alt`. Decorative images use
  `alt=""`.
- Icon-only buttons have an accessible name.
- Live regions announce asynchronous results once, not on every keystroke.
- `lang` is set on `html`.

```html
<button aria-label="Close dialog">
  <svg aria-hidden="true" focusable="false">...</svg>
</button>

<div role="status" aria-live="polite">Saved</div>
```

Use this utility rather than hiding text with `display: none`, which removes it
from the accessibility tree:

```css
.visually-hidden {
  position: absolute;
  inline-size: 1px;
  block-size: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
```

## The short list

Before saying a screen is done:

1. Contrast passes on every declared pair.
2. Tab through the screen, focus always visible and in order.
3. `Esc` closes every overlay, focus returns to its trigger.
4. Smallest target is at least 24 by 24.
5. Reduced motion still communicates every state change.
6. 320px wide and 200 percent zoom both reflow cleanly.
7. Every field has a visible label, every error names a fix.
8. No meaning carried by color alone.
