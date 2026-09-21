# Overlays

Modals, drawers, popovers, and toasts. Every one of them interrupts. Use the
lightest interruption that does the job.

## Choosing

| Overlay | Use for | Blocks the page |
|---|---|---|
| Modal | A decision that must happen now | Yes |
| Drawer | Detail or editing beside context | Usually |
| Popover | A small menu or supplementary control | No |
| Tooltip | A label supplement, never the only label | No |
| Toast | Confirmation of something already done | No |
| Inline expansion | Detail that belongs in the flow | No |

**Prefer inline over overlay, and undo over confirm.** A confirmation dialog
interrupts everyone to protect against a rare mistake, and users learn to
dismiss it unread.

Confirm only when the action is genuinely irreversible or expensive.

## Focus management

This is what separates a working overlay from a broken one.

1. On open, move focus into the overlay, to the first meaningful element or the
   overlay container. Never to the close button by default, and never to a
   destructive action.
2. Trap focus while open. `Tab` from the last element returns to the first.
3. `Esc` closes, every time, with no exceptions.
4. On close, return focus to the element that opened it.
5. Content behind is inert and not reachable by `Tab`.

```html
<dialog class="modal" id="confirm">
  <h2 id="confirm-title">Delete 3 bookings</h2>
  <p>This cannot be undone. Guests will be notified.</p>
  <div class="modal-actions">
    <button type="button" class="btn btn-secondary" autofocus>Cancel</button>
    <button type="button" class="btn btn-destructive">Delete 3 bookings</button>
  </div>
</dialog>
```

```css
.modal {
  max-inline-size: min(32rem, calc(100vw - var(--space-8)));
  padding: var(--space-6);
  border: none;
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  color: var(--color-text);
  box-shadow: var(--shadow-e3, none);
}

.modal::backdrop {
  background: rgba(0, 0, 0, 0.5);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  margin-block-start: var(--space-6);
}
```

The native `dialog` element with `showModal()` gives focus trapping, `Esc`, and
inert background for free. Reach for a custom implementation only when it
genuinely cannot serve.

Note `autofocus` sits on Cancel, not on Delete. The destructive action is never
the default.

## Modals

- One decision per modal. A modal containing a multi-step flow should be a page.
- The title states the action and its object: "Delete 3 bookings", not
  "Confirm".
- Buttons name their outcome. Never "Yes" and "No".
- Never open a modal from a modal.
- The modal scrolls internally if it is tall, with the actions always visible.

## Drawers

- Slide from the edge they are anchored to.
- Width is content-driven, up to about 40rem, full width on mobile.
- Keep the triggering context visible where possible, which is the reason to
  use a drawer rather than a modal.
- Unsaved changes prompt before closing, including on `Esc`.

## Popovers and menus

- Positioned relative to the trigger, flipping when near a viewport edge.
- Close on `Esc`, on outside click, and on selection.
- Arrow keys move between items, `Home` and `End` jump to the ends.
- Never on hover alone. Hover menus are unusable on touch and hostile to
  imprecise pointers.

```html
<button type="button" aria-expanded="false" aria-controls="row-menu" aria-haspopup="menu">
  Actions for Harbour Suite
</button>
<div role="menu" id="row-menu" hidden>
  <button role="menuitem" type="button">Edit</button>
  <button role="menuitem" type="button">Duplicate</button>
</div>
```

`aria-expanded` must reflect the real state. A static `false` is worse than
nothing.

## Toasts

A toast confirms something that already happened. It never asks a question and
never holds the only copy of important information.

- Position consistently, usually bottom or top end.
- Auto-dismiss after roughly 5 seconds for confirmations. **Never auto-dismiss
  an error.**
- Pause the timer on hover and on focus.
- Stack a small number, then collapse: "3 more".
- Announce with `role="status"` for confirmations, `role="alert"` for errors.
- If the toast carries an action such as Undo, give it long enough to be used,
  and make the action reachable by keyboard.

A toast is not a place for anything the user must act on. If they must act, it
is not a toast.

## Tooltips

- Supplement a label, never replace it.
- Appear on hover **and** on focus.
- Never contain interactive content.
- Never on touch as the only route to the information.

## Scroll and layout

Lock background scroll while a modal is open, without shifting the layout when
the scrollbar disappears:

```css
.scroll-locked {
  overflow: hidden;
  scrollbar-gutter: stable;
}
```

## Motion

Overlays enter faster than they feel and exit faster still. Entry around
200ms, exit around 150ms. Always provide a reduced-motion path, which for a
drawer is a cross-fade rather than no transition at all.

```css
@media (prefers-reduced-motion: reduce) {
  .modal,
  .drawer {
    transition-duration: 1ms;
  }
}
```

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| No focus trap | Keyboard users tab into dead content | Trap, or use `dialog` |
| Focus not returned on close | User loses their place entirely | Return to the trigger |
| `Esc` does nothing | Breaks the most universal expectation | Always close |
| Destructive action autofocused | One stray Enter destroys data | Focus the safe option |
| Modal opening a modal | Nowhere to go back to | Make it a page |
| "Are you sure?" with Yes and No | Forces re-reading the question | Name both outcomes |
| Hover-only menu | Unusable on touch | Click or focus |
| Auto-dismissing error toast | The user may never have seen it | Persist until dismissed |
| Toast holding the only Undo | Disappears before it is read | Keep the action available |
| Layout shift on scroll lock | Page jumps sideways | `scrollbar-gutter: stable` |
