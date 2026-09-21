# Anti-patterns

Things that look like design decisions but are usually the absence of one.

Each entry names the pattern, why it fails, and what to do instead. Use this
during the detail pass, and as a source of findings during an audit.

The visual, UX, and copy sections are being expanded in a later release. The
motion section below is complete.

## Motion

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| **Infinite pulsing** on a button or badge | Communicates nothing after the first cycle, distracts permanently, costs battery | Draw attention once, or use position and contrast |
| **Hover scale on everything** | If every card lifts, no card is distinguished. Reads as a template | Reserve lift for genuinely interactive cards, at 2px |
| **Stagger on every list render** | The product feels slow, because it is slow. A returning user waits again | Stagger on first render only, capped at about six items |
| **Bouncy springs on utility actions** | A save button that overshoots reads as unserious. Wrong for destructive confirmations | Springs for direct manipulation only, damped |
| **Motion on mount for static content** | Content the user came to read is withheld to perform an entrance | Render it |
| **Animating from `scale(0)`** | The element appears from nowhere, communicating no spatial relationship | `scale(0.96)` to `scale(1)` |
| **Large entrance translates** | A 40px slide is a template effect, not a spatial cue | 4 to 12px |
| **Bare `ease-in-out` on short transitions** | Sluggish at both ends, browser default rather than a decision | Use the easing tokens |
| **Symmetrical enter and exit** | Waiting for an exit is pure delay | Exits at 70 to 80 percent of the entrance |
| **Animating `width`, `height`, `top`** | Triggers layout on every frame, drops frames | `transform` and `opacity` |
| **Blocking input during animation** | The interface ignores the user for 300ms | Interruptible transitions |
| **Queued animations** | Delay compounds, the interface falls behind the user | Reverse from the current position |
| **Sweeping gradient shimmer** across a page of skeletons | The single effect most responsible for loading feeling cheap | Opacity pulse |
| **Parallax on a content page** | Vestibular trigger, hurts reading, costs performance | Nothing, or a very small shift |
| **Scroll reveal on every section** | Slows reading, fights the content, delays what they came for | Once or twice per page at most |
| **Count-up on every data refresh** | Unreadable while it animates, and it animates constantly | First load only, with tabular figures |
| **Animating the focus ring in** | A fast keyboard user outruns the indicator | Instant ring |
| **Autoplaying background video with no reduced-motion path** | Vestibular trigger, bandwidth cost | Poster image under reduced motion |
| **`will-change` left applied permanently** | Reserves memory for an element that is not moving | Remove when the animation ends |
| **Animation running off screen or in a hidden tab** | Consumes battery for nobody | Pause when not visible |
| **Removing all motion under `prefers-reduced-motion`** | State changes become ambiguous | Crossfade instead of travel |
| **Durations over 500ms** on anything repeated | The interface feels slow within a session | Match the size and frequency table |
| **Raw millisecond values** in the stylesheet | Timing drifts between components | Motion tokens |

See `../motion/principles.md` for the rules these violate, and
`../motion/recipes.md` for implementations that satisfy them.

## Visual

Expanded in a later release. Until then, the anti-patterns tables at the end of
each foundations file cover this ground:

- `../foundations/color.md` for palette and dark mode failures.
- `../foundations/typography.md` for scale, measure, and figure failures.
- `../foundations/spacing-layout.md` for rhythm and grid failures.
- `../foundations/surfaces-depth.md` for elevation and radius failures.
- `../foundations/iconography.md` for icon family and labelling failures.
- `../foundations/imagery.md` for art direction and alt text failures.

## UX

Expanded in a later release. Until then, see the anti-patterns tables in each
component and pattern file, and the pitfalls table in each archetype file.

## Copy

Expanded in a later release. Until then, `../foundations/microcopy.md` carries
the full list.
