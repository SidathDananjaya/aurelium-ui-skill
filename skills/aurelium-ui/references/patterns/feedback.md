# Feedback

Every action gets a response within about 400ms, even when the work is not
finished. Silence is the failure mode users hate most.

## The response ladder

Match the feedback to the wait.

| Wait | Response |
|---|---|
| Under 100ms | Nothing. It feels instant |
| 100 to 400ms | Immediate state change on the control |
| 400ms to 2s | Skeleton or inline progress |
| 2s to 10s | Progress with a sense of advancement |
| Over 10s | Progress plus what is happening, and let the user leave |

Never let a control look inert after a click. A button that appears to do
nothing gets clicked again, which is how duplicate orders happen.

## Optimistic updates

For reversible, likely-to-succeed actions, update immediately and reconcile
afterwards.

```
User taps favourite
  -> Icon fills instantly
  -> Request sent
  -> Success: nothing more to do
  -> Failure: revert, and say why
```

Suitable for: toggles, favourites, reordering, marking read, adding a tag.

**Not suitable for**: payments, deletions, anything irreversible, anything the
user would act on believing it succeeded. Never show a payment as complete
before it is.

When an optimistic update fails, the revert must be visible and explained. A
silent revert makes the user doubt what they saw.

## Progress

| Type | Use when |
|---|---|
| Indeterminate | Duration unknown, under about 10 seconds |
| Determinate | Duration or steps known |
| Stepped | A multi-stage process, naming the current stage |

A determinate bar that sticks at 90 percent is worse than an indeterminate one.
If you cannot estimate honestly, do not pretend to.

For long work, say what is happening: "Uploading 3 of 12" beats a bare bar.

```html
<div class="progress">
  <div
    class="progress-bar"
    role="progressbar"
    aria-valuenow="40"
    aria-valuemin="0"
    aria-valuemax="100"
    aria-label="Uploading photographs"
  ></div>
</div>
<p role="status">Uploading 3 of 12</p>
```

```css
.progress {
  block-size: var(--space-2);
  background: var(--color-border);
  border-radius: var(--radius-pill);
  overflow: hidden;
}

.progress-bar {
  block-size: 100%;
  inline-size: 40%;
  background: var(--color-accent);
  transition: inline-size var(--duration-base) var(--ease-standard);
}
```

## Undo over confirm

A confirmation dialog interrupts everyone to prevent a rare mistake, and users
learn to dismiss it without reading. Undo interrupts nobody and actually works.

| Action | Pattern |
|---|---|
| Delete one item, recoverable | Do it, offer undo |
| Archive, hide, mark read | Do it, offer undo |
| Delete permanently | Confirm, naming the count |
| Irreversible or expensive | Confirm, stating what is lost |
| Bulk destructive | Confirm, naming the count and scope |

Undo needs enough time to be noticed and used. Roughly 8 to 10 seconds, paused
on hover and focus, and reachable by keyboard.

If undo is impossible, confirm. If confirmation is required, name the object
and the count: "Delete 3 bookings", never "Are you sure?".

## Announcing changes

Visual feedback alone excludes screen reader users.

| Change | Mechanism |
|---|---|
| Status, non-urgent | `role="status"`, polite |
| Error, urgent | `role="alert"`, assertive |
| Progress | `role="progressbar"` with values |
| Result count after filtering | `role="status"` |

The live region must exist in the DOM before the content changes. Inserting an
element that already contains text often announces nothing.

Announce once. A region updating on every keystroke produces a stream of
interruptions, so debounce it.

## Inline over global

Put feedback where the action happened.

- A field error belongs beside the field.
- A row action's result belongs on the row.
- A toast is for something already done, elsewhere on screen.
- A banner is for something affecting the whole page.

A toast reporting a field validation error is feedback in the wrong place.

## Duplicate submission

Disable the control while a request is in flight, or make the operation
idempotent. Preferably both. Preserve the control's width so the layout does
not shift. See `../components/buttons.md`.

## Motion in feedback

Motion confirms cause and effect, so feedback is where it earns its place.

- The change originates where the user acted.
- Short: 120 to 240ms.
- Interruptible. A second action must not wait for the first animation.
- Reduced motion gets a cross-fade, not the removal of the signal.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| No response for 2 seconds | User clicks again, duplicates the action | Acknowledge within 400ms |
| Spinner with no context | No sense of progress or scale | Say what is happening |
| Fake determinate progress | Sticks at 90 percent, destroys trust | Indeterminate, honestly |
| Optimistic payment confirmation | User believes money moved | Never optimistic for money |
| Silent revert on failure | User doubts what they saw | Revert visibly, explain |
| Confirm dialog for everything | Learned dismissal, no protection | Undo where possible |
| Undo that vanishes in 3 seconds | Gone before it is read | 8 to 10 seconds |
| Toast for a field error | Feedback far from the cause | Inline beside the field |
| Live region on every keystroke | Constant interruption | Debounce |
| Success toast for a flow's ending | Underweights the peak moment | Give the confirmation the screen |
