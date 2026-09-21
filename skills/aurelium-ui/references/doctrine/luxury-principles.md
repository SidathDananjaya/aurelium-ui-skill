# The ten luxury principles

Luxury in software is the absence of friction and the presence of care.

These principles are ordered. When two conflict, the lower number wins. Every
principle states a rule you follow and a check you can run, so "is this done"
never becomes a matter of taste.

## 1. Space is the material

**Rule.** Whitespace is the primary compositional tool. Section padding scales
with viewport width. Never fill space just because it exists.

**Check.** Every margin, padding, and gap value comes from the spacing scale.
Grep the stylesheet for pixel values outside the scale. Zero results, or each
exception carries a comment explaining the optical correction.

**Do.** Give a hero section 96px to 160px of vertical padding at desktop width.
**Don't.** Add a decorative panel to balance an empty column. Leave it empty.

## 2. One hero per view

**Rule.** Each screen has exactly one primary focal point and exactly one
primary action. Everything else is secondary or tertiary.

**Check.** Count elements using the primary button style per screen. The count
is 1. Count competing visual anchors above the fold. The count is 1.

**Do.** Pair one filled primary button with text or outline secondaries.
**Don't.** Place "Get started" and "Book a demo" side by side in the same weight.

## 3. Typography carries the brand

**Rule.** Hierarchy comes from size, then weight, then spacing, and only then
color. Maximum two families, plus one monospace face for data.

**Check.** Count `font-family` declarations. Three or fewer, and the third is
monospace. Confirm each step in the type scale differs from its neighbour by
the declared ratio.

**Do.** Separate a heading from body text with size and weight alone.
**Don't.** Color a heading to make it feel important while leaving it at body size.

## 4. Restrained palette

**Rule.** Neutrals do about 90 percent of the work. One accent. Semantic colors
appear only when they carry meaning: success, warning, danger, info.

**Check.** Count distinct hues outside the neutral ramp. The maximum is one
accent plus the semantic set. Any additional hue must be justified in writing.

**Do.** Use the accent for the single primary action and for focus.
**Don't.** Assign a different color to each card in a grid.

## 5. Precision

**Rule.** Everything sits on a 4px base grid. Icons and rounded shapes get
optical alignment, not mathematical alignment. Numbers use tabular figures.

**Check.** Off-scale spacing values return zero grep results. Any element
displaying figures that change or align in columns declares
`font-variant-numeric: tabular-nums`.

**Do.** Nudge a play triangle 1px right of center so it looks centered.
**Don't.** Trust that equal padding produces optical balance for a circle.

## 6. Material and depth with intent

**Rule.** Elevation expresses layering and hierarchy, never decoration. Three
elevation levels at most: raised, overlay, and modal.

**Check.** Count distinct shadow tokens in use. Three or fewer. Every shadowed
element sits on a genuinely higher layer than its parent.

**Do.** Reserve the deepest shadow for dialogs that block the page.
**Don't.** Give every card a drop shadow because it looks richer.

## 7. Quiet motion

**Rule.** Motion confirms cause and effect. It is short, eased, and
interruptible. Nothing moves without a reason you can state in one sentence.

**Check.** No infinite animation exists except live status indicators. Every
animation has a `prefers-reduced-motion` path. Every duration comes from the
motion tokens.

**Do.** Slide a drawer from the edge it is anchored to, in 200ms to 320ms.
**Don't.** Fade and scale every card as it enters the viewport.

## 8. Care in the details

**Rule.** Empty, loading, error, and success states are designed, not left to
the framework default. Microcopy is human and specific.

**Check.** Every data-driven view ships every state in the complete-states rule:
default, loading, empty on first use, empty with no results, recoverable error,
fatal error, partial data, offline where applicable, success, long content, and
permission denied where applicable. No view renders a bare spinner as its only
loading state. No error message reads "Something went wrong" without a next step.

**Do.** Write "We could not reach the payment service. Retry, or use a different card."
**Don't.** Write "Error 500."

## 9. Effortless performance

**Rule.** Speed is part of the product, not a technical detail. A slow luxury
interface is not a luxury interface.

**Check.** Meets every budget in `performance.md`: LCP under 2.5s, INP under
200ms, CLS under 0.1.

**Do.** Animate `transform` and `opacity` only.
**Don't.** Animate `width`, `height`, `top`, or `box-shadow` on scroll.

## 10. Inclusive by default

**Rule.** Luxury that excludes is not luxury. Accessibility is a floor, not a
feature.

**Check.** Meets every requirement in `accessibility.md`, including the short
list at the end of that file.

**Do.** Give focus a visible, designed indicator that matches the brand.
**Don't.** Remove the focus outline because it interrupts the composition.

## Applying the order

When restraint argues against a signature detail, restraint wins unless the
detail serves clarity. When a visual idea costs performance, performance wins.
When accessibility constrains an aesthetic choice, accessibility wins, and the
aesthetic is solved a different way.

State the tradeoff out loud when you make one. "I dropped the parallax header
because it pushed LCP past budget" is a design decision worth reporting.
