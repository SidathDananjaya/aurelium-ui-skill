# Buttons

A button performs an action. A link navigates. Using the wrong element breaks
keyboard behaviour, middle-click, and the accessibility tree.

## Anatomy

| Part | Rule |
|---|---|
| Label | A verb naming the outcome. Sentence case |
| Icon | Optional, leading for meaning, trailing for direction |
| Target | At least 44 by 44 for primary and touch, never below 24 by 24 |
| Padding | From the spacing scale, horizontal larger than vertical |
| Radius | From the direction's radius scale |

Horizontal padding is roughly twice vertical. A pill needs more than the maths
suggests, because the round ends eat space.

## Hierarchy

Exactly one primary per view. If two actions feel equally important, one is
secondary or it belongs on another screen.

| Level | Appearance | Use for |
|---|---|---|
| Primary | Accent fill, `accent-fg` label | The single most important action |
| Secondary | Hairline border, text colour | Supporting actions |
| Tertiary | Text only, no border | Low weight actions, cancel |
| Destructive | Danger fill or danger border | Delete, revoke, cancel a subscription |

Destructive is a variant of any level, not a fourth level. A destructive
primary is a filled danger button. A destructive tertiary is danger text.

Never make the destructive action the default focus in a dialog.

## Sizes

Three at most: small, medium, large. Medium is the default and the one most of
the product uses.

Size changes padding and type step. It never changes radius, because that would
break the direction's voice.

## States

Every state is designed. None is left to the browser.

| State | Treatment |
|---|---|
| Default | Base |
| Hover | Accent shifts to `accent-hover`. No scale transform |
| Focus | Visible ring, 2px offset, never removed |
| Active | Slight darkening, or a 1px downward translate |
| Disabled | Reduced opacity, `cursor: not-allowed`, still in the tab order only if it explains itself |
| Loading | Spinner replaces the icon, width is preserved, label stays |

**Loading must not resize the button.** A label swapped for a spinner collapses
the width and moves everything after it. Reserve the width.

```html
<button class="btn btn-primary" type="button" data-loading="false">
  <span class="btn-label">Confirm booking</span>
</button>
```

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  min-block-size: 44px;
  padding: var(--space-3) var(--space-5);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  font: inherit;
  font-weight: 600;
  font-size: var(--text-xs);
  cursor: pointer;
  transition: background var(--duration-fast) var(--ease-standard);
}

.btn-primary {
  background: var(--color-accent);
  color: var(--color-accent-fg);
}

.btn-primary:hover { background: var(--color-accent-hover); }

.btn-secondary {
  background: transparent;
  color: var(--color-text);
  border-color: var(--color-border);
}

.btn-tertiary {
  background: transparent;
  color: var(--color-accent);
  border-color: transparent;
  padding-inline: var(--space-2);
}

.btn-destructive {
  background: var(--color-danger);
  color: var(--color-accent-fg);
}

.btn:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Optical correction: a 1px press gives tactile feedback without reflow */
.btn:active { transform: translateY(1px); }

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Keeps the width while the spinner replaces the label */
.btn[data-loading="true"] .btn-label { visibility: hidden; }
.btn[data-loading="true"]::after {
  content: "";
  position: absolute;
  inline-size: 1em;
  block-size: 1em;
  border: 2px solid currentColor;
  border-block-start-color: transparent;
  border-radius: var(--radius-pill);
  animation: btn-spin var(--duration-slow) linear infinite;
}

@keyframes btn-spin { to { transform: rotate(360deg); } }

@media (prefers-reduced-motion: reduce) {
  .btn[data-loading="true"]::after { animation-duration: 2s; }
  .btn:active { transform: none; }
}
```

## Icon buttons

An icon-only button always carries an accessible name. A tooltip is not a
label: it is unavailable on touch and invisible when scanning.

```html
<button class="btn btn-icon" type="button" aria-label="Close dialog">
  <svg aria-hidden="true" focusable="false" viewBox="0 0 24 24">
    <path d="M6 6l12 12M18 6L6 18" />
  </svg>
</button>
```

Pad the button to reach 44px. Never enlarge the glyph to get there.

Icon-only is acceptable for close, search, menu, back, and play. It is never
acceptable for delete, archive, share, export, or publish. See
`../foundations/iconography.md`.

## Button versus link

| Behaviour | Element |
|---|---|
| Changes data, opens a dialog, submits | `button` |
| Navigates to a URL | `a` |
| Looks like a button, navigates | `a` styled as a button |
| Looks like a link, performs an action | `button` styled as a link |

A `div` with a click handler is never correct. It is not focusable, does not
respond to Enter or Space, and is invisible to assistive technology.

## Groups

Buttons in a row read right to left in importance for confirmation dialogs, and
left to right for toolbars. Pick one convention per product and hold it.

Gap between buttons is at least `--space-3`, so a near miss does not trigger
the wrong action.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Two primary buttons in one view | Neither reads as primary | One primary, rest secondary |
| "Submit" or "OK" | Names the mechanism, not the outcome | Name the outcome |
| Scale transform on hover | Reflows neighbours, feels cheap | Change background |
| Spinner replacing the label | Button collapses, layout jumps | Reserve the width |
| Disabled with no explanation | User cannot tell why | Explain adjacent, or keep enabled and validate |
| Icon-only destructive action | Outcome unpredictable | Add the label |
| Removing the focus outline | Keyboard users lose their place | Design a visible ring |
| `div` with onclick | Not focusable, not announced | Use `button` |
