# Detail checklist

The craft pass. These are the refinements that separate competent from
considered.

**This is not the gate.** `preflight.md` holds the pass or fail checks. Walk
that first. This list covers the finer items that are judgement rather than
compliance, and it is where the last two points of a score are won.

Work through it with the build open. Most items take seconds to check and
seconds to fix.

## Typography

| # | Check |
|---|---|
| T1 | Every size comes from the scale. No in-between values |
| T2 | Line height follows the size band. Display tighter, body looser |
| T3 | Reading text sits between 60 and 75 characters per line |
| T4 | Display sizes carry negative tracking. Small caps carry positive |
| T5 | Body text has zero tracking. Lowercase is never tracked out |
| T6 | `text-wrap: balance` on headings, `pretty` on paragraphs |
| T7 | No heading ends on a single orphaned word |
| T8 | No heading breaks mid-word |
| T9 | Tabular figures on every number that changes or aligns |
| T10 | Proportional figures in running prose |
| T11 | No faux bold or faux italic. The real weight is loaded |
| T12 | Body text is at least 16px on mobile |
| T13 | Sentence case throughout. No Title Case, no all-caps sentences |
| T14 | Long unbroken strings wrap, such as emails and identifiers |

## Spacing and layout

| # | Check |
|---|---|
| S1 | Every spacing value is a token |
| S2 | Inner gaps smaller than outer gaps, everywhere, no exceptions |
| S3 | Space above a heading exceeds space below it |
| S4 | `gap` used on parents rather than margins on children |
| S5 | Optical corrections applied where maths and eye disagree |
| S6 | Every optical correction carries a comment explaining it |
| S7 | Content has a maximum width. Nothing runs bezel to bezel |
| S8 | Edges align across sections on one grid |
| S9 | No fixed heights on containers holding text |
| S10 | Nested radii are concentric |
| S11 | Empty space is left empty, not filled with decoration |

## Colour and surface

| # | Check |
|---|---|
| C1 | Neutrals are tinted, not pure grey |
| C2 | Not pure black on pure white for body text |
| C3 | One accent outside neutrals and semantics |
| C4 | Semantic colour appears only where it carries meaning |
| C5 | Dark mode raises surface lightness rather than inverting |
| C6 | Dark mode reduces accent chroma |
| C7 | Dark mode page is not pure black |
| C8 | Shadows tinted toward the palette, not neutral black |
| C9 | One light source. All shadows offset the same direction |
| C10 | Three elevation levels at most |
| C11 | Separation uses space first, surface second, border third, shadow last |

## Interaction

| # | Check |
|---|---|
| I1 | Hover, focus, active, and disabled all designed |
| I2 | Focus indicator matches the brand rather than the browser default |
| I3 | Loading states preserve the control's width |
| I4 | Disabled controls explain why, adjacent |
| I5 | Cursor matches the affordance |
| I6 | Hit areas extend beyond small glyphs via padding |
| I7 | Adjacent targets separated so a near miss does not misfire |
| I8 | Transitions interruptible |
| I9 | Nothing moves under the pointer as the user reaches for it |
| I10 | Scroll position preserved on back navigation |
| I11 | Text selection not disabled on content |
| I12 | Autofocus used only where it genuinely helps, never on destructive actions |

## Content and copy

| # | Check |
|---|---|
| N1 | Buttons name outcomes, not mechanisms |
| N2 | Errors state what happened, why, and what to do next |
| N3 | Empty states explain and offer the action |
| N4 | First-use and no-results empty states differ |
| N5 | No exclamation marks outside a genuine peak moment |
| N6 | No "Oops", "Uh oh", or apologetic filler |
| N7 | Dates unambiguous. "4 Mar 2026", not "04/03/2026" |
| N8 | Currency and unit always stated |
| N9 | Numbers rounded to a sensible precision |
| N10 | Realistic content, never lorem ipsum, never "Test User 1" |
| N11 | Confirmation copy says what happens next |
| N12 | No internal vocabulary in user-facing strings |

## Responsive

| # | Check |
|---|---|
| R1 | Renders cleanly at 375, 768, 1024, 1440 |
| R2 | Reflows at 320px with no horizontal scroll |
| R3 | Usable at 200 percent zoom |
| R4 | Tables have a stated responsive strategy, applied consistently |
| R5 | Sticky headers stay short on small viewports |
| R6 | Primary action reachable with one thumb on mobile |
| R7 | Images serve a size appropriate to their slot |
| R8 | Breakpoints exist where content breaks, not where devices exist |

## Imagery and icons

| # | Check |
|---|---|
| M1 | One icon family, one stroke weight throughout |
| M2 | Icons inherit `currentColor` |
| M3 | Decorative icons hidden from assistive technology |
| M4 | No emoji used as icons |
| M5 | One aspect ratio per image grid |
| M6 | Every image reserves its space before loading |
| M7 | Text over imagery has a verified contrast floor |
| M8 | Placeholders match final dimensions |

## The last mile

The items most often missed, gathered for a final sweep:

1. Tab through the whole build once, slowly.
2. Resize from 1440 to 320 continuously and watch for the break.
3. Turn on reduced motion and repeat the primary task.
4. Replace the shortest content with the longest realistic content.
5. Read every string aloud.
6. Look at it in the other theme.
7. Open the console.

Each takes under a minute and each reliably finds something.

## Related references

`preflight.md` for the pass or fail gate, `anti-patterns.md` for what to avoid,
`rubric.md` for scoring, and the foundations files for the reasoning behind each
rule.
