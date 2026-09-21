# Motion principles

Motion confirms cause and effect. It is short, eased, and interruptible.
Nothing moves without a reason you can state in one sentence.

Motion is where generated interfaces most often betray themselves. The tell is
not too little animation. It is animation applied evenly to everything, which
communicates nothing because it distinguishes nothing.

## The purpose test

Before adding any animation, answer in one sentence: **what does this motion
communicate?**

| Valid purpose | Example |
|---|---|
| Cause and effect | The drawer slid from the button that opened it |
| Spatial relationship | The detail expanded from the row it belongs to |
| State change | The toggle moved, so the state moved |
| Continuity | The item kept its identity across the transition |
| Attention, once | The failed field drew the eye to itself |

If the answer is "it looks nice", "it feels modern", or "the page seemed
static", delete it. Those are not purposes. They are the absence of one.

**Check.** For every animation in the build, write its one sentence. Any
animation without one is removed before the detail pass.

## Duration by size and frequency

Two rules, and frequency beats size when they conflict.

**The more often a user sees it, the faster it must be.** A hover state seen
two hundred times a session is at the floor. A page transition seen twice is
allowed to breathe.

**The further something travels, the longer it may take.** A checkbox moves a
few pixels. A full-screen drawer crosses the viewport.

| Element | Distance | Frequency | Duration |
|---|---|---|---|
| Hover, focus, active | None | Constant | 80 to 140ms |
| Checkbox, toggle, radio | Tiny | High | 100 to 160ms |
| Tooltip, small popover | Small | High | 120 to 180ms |
| Dropdown, menu | Small | High | 150 to 220ms |
| Card expand, accordion | Medium | Medium | 200 to 280ms |
| Modal | Medium | Medium | 200 to 300ms |
| Drawer, sheet | Large | Medium | 250 to 350ms |
| Page transition | Full | Low | 300 to 450ms |

Anything above 500ms is either a deliberate, once-per-session moment or a
mistake. Almost always the second.

Durations come from the direction's motion tokens. Never write a raw
millisecond value.

## Enter and exit are not symmetrical

Exits are faster than entrances, typically 70 to 80 percent of the duration.

An entrance introduces something the user must orient to, so it can afford the
time. An exit removes something the user has already finished with, and waiting
for it is pure delay.

```css
.drawer {
  transition: transform var(--duration-base) var(--ease-entrance);
}

.drawer[data-state="closed"] {
  transform: translateX(100%);
  transition: transform var(--duration-fast) var(--ease-exit);
}
```

The easing differs too. Entrances decelerate into place. Exits accelerate away.

## Easing

Never use a bare `ease`, `ease-in-out`, or `linear` for interface motion. The
browser defaults are not designed, and `ease-in-out` in particular makes short
transitions feel sluggish at both ends.

| Token | Curve shape | Use for |
|---|---|---|
| `--ease-standard` | Fast out, slow in | Most transitions, state changes |
| `--ease-entrance` | Decelerating | Things arriving |
| `--ease-exit` | Accelerating | Things leaving |

`linear` is correct for exactly two things: continuous rotation, such as a
spinner, and colour or opacity crossfades where no spatial movement is implied.

## Springs

A spring is right when the user is manipulating something directly: a dragged
sheet, a swipe, a pull to refresh. The motion should continue the gesture's
momentum.

A spring is wrong for utility actions. A save button that bounces reads as
unserious, and bounce on a destructive confirmation is actively inappropriate.

Damping matters more than the spring itself. Overshoot beyond a few percent
reads as cheap rather than lively.

## Interruptibility

A user who changes their mind mid-animation must not wait.

- A second click reverses from the current position, not from the end state.
- Transitions on `transform` and `opacity` interrupt naturally. Keyframe
  animations usually do not, which is one reason to prefer transitions.
- Never queue animations behind one another.
- Never block input during an animation.

An interface that ignores you for 300ms because something is still moving feels
broken, not polished.

## Never animate from nothing

`scale(0)`, `height: 0`, and `opacity: 0` combined with a large translate all
produce the same problem: the element appears from nowhere, which communicates
no spatial relationship.

| Instead of | Do |
|---|---|
| `scale(0)` to `scale(1)` | `scale(0.96)` to `scale(1)` |
| `translateY(40px)` | `translateY(8px)` to `translateY(12px)` |
| `opacity: 0` alone on a moving element | Opacity with a small, related movement |

Small movements read as confident. Large ones read as a template.

## Stagger

Stagger communicates that items arrived as a group in sequence. It is right for
a list appearing for the first time, and wrong for a list the user has already
seen.

- 20 to 40ms between items.
- Cap the total: after about six items, stop staggering and show the rest.
- Never stagger on every re-render, filter change, or navigation back.

A list that re-staggers each time the user returns to it makes the product feel
slow, because it is slow.

## Performance

Animate `transform` and `opacity`. Nothing else composites cleanly. See
`../doctrine/performance.md` for the full budget.

Never animate a property that triggers layout: `width`, `height`, `top`,
`margin`, `padding`. For a height transition, use `grid-template-rows` from
`0fr` to `1fr`, or animate a transform on a wrapper.

Remove `will-change` when the animation ends. A permanently promoted layer
reserves memory for an element that is not moving.

## Reduced motion

`prefers-reduced-motion: reduce` is a request to remove **vestibular triggers**:
large movement, parallax, scaling, spinning, and autoplay. It is not a request
for a static interface.

**Every transition keeps a way to read the state change.** Replace movement
with a crossfade rather than removing the transition entirely.

```css
/* A reasonable global floor */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
    scroll-behavior: auto !important;
  }
}
```

The global rule is a safety net, not the design. Where motion carries meaning,
handle it per component:

```css
.drawer {
  transition: transform var(--duration-base) var(--ease-standard);
}

@media (prefers-reduced-motion: reduce) {
  .drawer {
    /* Crossfade instead of travel: the state change is still legible */
    transition: opacity var(--duration-fast) var(--ease-standard);
    transform: none;
  }
}
```

**Check.** Enable the setting and use the product. Every state change is still
perceivable. Nothing became ambiguous.

## Infinite animation

No animation loops forever except a live status indicator: a spinner during a
genuine wait, a pulse on a genuinely live connection.

A decorative element that loops forever consumes battery, distracts
permanently, and communicates nothing after the first cycle.

Never animate anything off screen. Pause when the tab is hidden.

## The motion dial

| Dial | What exists |
|---|---|
| 1 to 2 | State changes only: hover, focus, open, close |
| 3 to 6 | Plus page transitions, list and layout animation |
| 7 to 10 | Plus choreographed sequences, scroll-driven storytelling, shared element transitions |

The dial adds categories of motion. It never lengthens durations. A motion 9
interface has more animation than a motion 3 one, not slower animation.

## The checklist

Before the detail pass:

1. Every animation has a one sentence purpose.
2. Durations come from tokens, and match the size and frequency table.
3. Exits are faster than entrances.
4. No bare `ease`, `ease-in-out`, or `linear` outside spinners and crossfades.
5. Only `transform` and `opacity` animate.
6. Everything is interruptible.
7. Nothing animates from `scale(0)` or a large translate.
8. No infinite animation outside live status.
9. Reduced motion keeps every state change legible.
10. Nothing animates off screen or in a hidden tab.
