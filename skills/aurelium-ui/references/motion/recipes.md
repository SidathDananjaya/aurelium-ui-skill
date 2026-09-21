# Motion recipes

Every recipe uses tokens, animates only `transform` and `opacity`, and carries
a reduced-motion variant that keeps the state change legible.

Read `principles.md` first. These are applications of those rules, not
substitutes for them.

## Button press

The shortest motion in the product, and the most repeated.

```css
.btn {
  transition: background var(--duration-fast) var(--ease-standard);
}

/* Optical correction: a 1px press reads as tactile without reflow */
.btn:active {
  transform: translateY(1px);
}

@media (prefers-reduced-motion: reduce) {
  .btn:active { transform: none; }
}
```

Under reduced motion the background change still confirms the press, so nothing
is lost.

## Hover lift

Use sparingly. A grid where every card lifts communicates nothing.

```css
.card {
  transition:
    transform var(--duration-fast) var(--ease-standard),
    box-shadow var(--duration-fast) var(--ease-standard);
}

.card:hover {
  transform: translateY(-2px);
}

@media (prefers-reduced-motion: reduce) {
  .card:hover { transform: none; }
}
```

Two pixels, not eight. A card that leaps toward the cursor is a template
effect. Never apply a hover lift to something that is not interactive.

## Dropdown and popover

Originates from its trigger, so it must not fade in from the centre of the
screen.

```css
.popover {
  opacity: 0;
  transform: translateY(-4px) scale(0.98);
  transform-origin: top center;
  transition:
    opacity var(--duration-fast) var(--ease-exit),
    transform var(--duration-fast) var(--ease-exit);
}

.popover[data-state="open"] {
  opacity: 1;
  transform: translateY(0) scale(1);
  transition:
    opacity var(--duration-base) var(--ease-entrance),
    transform var(--duration-base) var(--ease-entrance);
}

@media (prefers-reduced-motion: reduce) {
  .popover,
  .popover[data-state="open"] {
    transform: none;
    transition: opacity var(--duration-fast) var(--ease-standard);
  }
}
```

`scale(0.98)`, not `scale(0)`. `transform-origin` anchors it to the trigger.

## Modal

```css
.modal {
  opacity: 0;
  transform: scale(0.97);
  transition:
    opacity var(--duration-fast) var(--ease-exit),
    transform var(--duration-fast) var(--ease-exit);
}

.modal[open] {
  opacity: 1;
  transform: scale(1);
  transition:
    opacity var(--duration-base) var(--ease-entrance),
    transform var(--duration-base) var(--ease-entrance);
}

.modal::backdrop {
  opacity: 0;
  transition: opacity var(--duration-fast) var(--ease-standard);
}

.modal[open]::backdrop { opacity: 1; }

@media (prefers-reduced-motion: reduce) {
  .modal,
  .modal[open] {
    transform: none;
    transition: opacity var(--duration-fast) var(--ease-standard);
  }
}
```

## Drawer

Slides from the edge it is anchored to. A drawer entering from the wrong side
breaks the spatial model.

```css
.drawer {
  transform: translateX(100%);
  transition: transform var(--duration-fast) var(--ease-exit);
}

.drawer[data-state="open"] {
  transform: translateX(0);
  transition: transform var(--duration-slow) var(--ease-entrance);
}

@media (prefers-reduced-motion: reduce) {
  .drawer {
    transform: none;
    opacity: 0;
    transition: opacity var(--duration-fast) var(--ease-standard);
  }
  .drawer[data-state="open"] { opacity: 1; }
}
```

## Toast

Enters from its resting edge, exits the way it came.

```css
.toast {
  opacity: 0;
  transform: translateY(8px);
  transition:
    opacity var(--duration-fast) var(--ease-exit),
    transform var(--duration-fast) var(--ease-exit);
}

.toast[data-state="visible"] {
  opacity: 1;
  transform: translateY(0);
  transition:
    opacity var(--duration-base) var(--ease-entrance),
    transform var(--duration-base) var(--ease-entrance);
}

@media (prefers-reduced-motion: reduce) {
  .toast,
  .toast[data-state="visible"] {
    transform: none;
    transition: opacity var(--duration-fast) var(--ease-standard);
  }
}
```

## List add and remove

Use the View Transitions API where available, and degrade to nothing rather
than to something worse.

```css
@supports (view-transition-name: none) {
  .list-item { view-transition-name: attr(data-id type(custom-ident), none); }
}

.list-item {
  transition:
    opacity var(--duration-base) var(--ease-standard),
    transform var(--duration-base) var(--ease-standard);
}

.list-item[data-entering="true"] {
  opacity: 0;
  transform: translateY(4px);
}

@media (prefers-reduced-motion: reduce) {
  .list-item[data-entering="true"] { transform: none; }
}
```

Stagger only on first render. See `principles.md`.

## Accordion and expand

Height cannot be animated cleanly. `grid-template-rows` can.

```css
.accordion-panel {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows var(--duration-base) var(--ease-standard);
}

.accordion-panel[data-state="open"] {
  grid-template-rows: 1fr;
}

.accordion-panel > div {
  overflow: hidden;
}

@media (prefers-reduced-motion: reduce) {
  .accordion-panel { transition-duration: 1ms; }
}
```

This animates a layout property, which the performance budget normally forbids.
It is the accepted exception, because the alternatives are a fixed height that
breaks with real content, or a `max-height` transition that eases wrongly.

## Page transition

```css
@view-transition { navigation: auto; }

::view-transition-old(root) {
  animation: page-out var(--duration-fast) var(--ease-exit) both;
}

::view-transition-new(root) {
  animation: page-in var(--duration-base) var(--ease-entrance) both;
}

@keyframes page-out { to { opacity: 0; } }

@keyframes page-in { from { opacity: 0; } }

@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) {
    animation-duration: 1ms;
  }
}
```

Where View Transitions are unsupported, navigation is simply instant, which is
an acceptable outcome rather than a degraded one.

## Skeleton shimmer

```css
.skeleton {
  background: var(--color-border);
  border-radius: var(--radius-sm);
}

@media (prefers-reduced-motion: no-preference) {
  .skeleton {
    animation: skeleton-pulse var(--duration-slow) var(--ease-standard) infinite alternate;
  }
}

@keyframes skeleton-pulse { to { opacity: 0.55; } }
```

The animation is declared inside `prefers-reduced-motion: no-preference`, so
reduced motion gets a static placeholder with no override needed. This is the
cleanest way to write an optional animation.

Opacity, not a moving gradient. A sweeping highlight across a whole page of
skeletons is the effect most responsible for loading states feeling cheap.

## Number count-up

For a KPI on first load only, never on every update.

```css
.kpi-value {
  font-variant-numeric: tabular-nums lining-nums;
  transition: opacity var(--duration-base) var(--ease-standard);
}

@media (prefers-reduced-motion: reduce) {
  .kpi-value { transition-duration: 1ms; }
}
```

Tabular figures are mandatory here. Without them the value visibly changes
width as it counts, which is worse than no animation.

Count up only from a meaningful baseline, and never on a figure the user is
currently reading. Under reduced motion, show the final value immediately.

## Scroll reveal

Progressive enhancement. The content must be visible and readable if nothing
runs.

```css
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .reveal {
      animation: reveal-in auto var(--ease-entrance) both;
      animation-timeline: view();
      animation-range: entry 10% cover 30%;
    }
  }
}

@keyframes reveal-in {
  from { opacity: 0; transform: translateY(12px); }
}
```

Both guards matter: reduced motion gets nothing, and browsers without
scroll-driven animation get fully visible content rather than content stuck at
`opacity: 0`.

Never reveal on scroll more than once or twice per page, and never on content
the user has already scrolled past.

## Focus ring

Focus must appear instantly. Never animate a focus indicator in.

```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  transition: outline-offset var(--duration-fast) var(--ease-standard);
}

@media (prefers-reduced-motion: reduce) {
  :focus-visible { transition-duration: 1ms; }
}
```

Only the offset animates, and only for the polish of it. The ring itself is
immediate, because a keyboard user moving quickly must never outrun the
indicator.

This is the one recipe where removing the animation entirely costs nothing, so
reduced motion simply collapses the duration. The ring is already instant.

## Recipe checklist

Every recipe above satisfies all of these. Anything new must too.

1. Durations from tokens, never raw milliseconds.
2. Only `transform` and `opacity` animate, with the accordion exception noted.
3. Exits faster than entrances.
4. A reduced-motion variant that keeps the state change legible.
5. No animation from `scale(0)` or a large translate.
6. No infinite animation outside skeletons and live status.
7. Interruptible.
