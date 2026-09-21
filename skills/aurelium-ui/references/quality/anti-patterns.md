# Anti-patterns

Things that look like design decisions but are usually the absence of one.

Each entry names the pattern, why it fails, and what to do instead. Use this
during the detail pass, and as a source of findings during an audit.

Four sections: visual, UX, motion, and copy. Each foundations, component and
archetype file carries its own narrower table. This file gathers the failures
that recur across all of them.

## Visual

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| **Purple to pink gradient** on a dark hero | The default look of generated output. Dates the work instantly | One accent, flat, on a considered neutral |
| **Low contrast grey body text** | Fails AA, and reads unfinished rather than subtle | A muted step that still clears 4.5:1 |
| **A different colour per card** | Destroys hierarchy, nothing reads as primary | Neutral surfaces, one accent |
| **Gradient text for body copy** | Unreadable small, uncheckable for contrast | Solid colour |
| **Glassmorphism over busy imagery** | Contrast becomes unpredictable | Solid scrim, or blur over a controlled surface |
| **Shadow on every card** | Elevation stops meaning anything | Hairline or surface change |
| **More than three elevation levels** | Nobody perceives the difference | Three |
| **Pure black dark mode** | No room for elevation, high glare | Near-black around 13 percent lightness |
| **Inverting the light palette for dark** | Glare, and depth disappears | Lightness-based elevation |
| **Pure black on pure white** for long reading | Halation, tiring to read | Pull both ends in |
| **Pure grey neutrals** | Reads cheap. Nothing real is pure grey | Tint the whole ramp consistently |
| **Centred everything** | No structural spine, all elements equally weighted | Left-aligned structure, centre for emphasis |
| **Generic three-card feature grid** by default | The laziest layout in the genre | Structure around the argument |
| **Off-scale values** such as 13px or 37px | Rhythm breaks, nothing aligns | Use the scale |
| **Equal inner and outer spacing** | Groups dissolve | Inner always smaller |
| **Mixed aspect ratios in one grid** | Breaks the rhythm | One ratio per grid |
| **Inner radius larger than outer** | Looks broken | Concentric radii |
| **Emoji as icons** | Platform-inconsistent, wrong register, verbose to screen readers | Drawn SVG on the project grid |
| **Two icon families** | Mismatched weight and density | One family, draw what is missing |
| **Stock photography of people at laptops** | Reads as filler on sight | Real product, real place, or nothing |
| **Filling empty space with decoration** | Space was the point | Leave it |
| **Fixed heights on text containers** | Overflows with real content | Let content grow, clamp if needed |

## UX

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| **Two primary buttons in one view** | Neither reads as primary | One primary, rest secondary |
| **Only the happy path built** | The product fails on first contact with reality | Every state in `../patterns/states.md` |
| **Placeholder used as the label** | Vanishes on focus, fails accessibility | Visible label above |
| **Validating while the user first types** | Shows errors for unfinished input | Validate on blur |
| **Costs revealed at the final step** | The largest single cause of abandonment | Itemise early |
| **Forced account creation before purchase** | Loses the sale outright | Guest checkout |
| **Confirm dialog for everything** | Learned dismissal, so it protects nothing | Undo where reversible |
| **"Are you sure?" with Yes and No** | Forces re-reading the question | Name both outcomes |
| **Destructive action autofocused** | One stray Enter destroys data | Focus the safe option |
| **No focus trap in a modal** | Keyboard users tab into dead content | Trap, or use the native dialog |
| **Focus not returned on close** | The user loses their place entirely | Return it to the trigger |
| **Escape does nothing** | Breaks the most universal expectation | Always close |
| **Hidden active filters** | An empty list with no explanation | Visible removable chips |
| **Filter and query state absent from the URL** | Back button and sharing both break | Put it in the URL |
| **Losing input on error** | Punishes the user for a server fault | Preserve everything |
| **No response for two seconds** | The user clicks again and duplicates the action | Acknowledge within 400ms |
| **Optimistic confirmation of a payment** | The user believes money moved | Never optimistic for money |
| **Auto-dismissing error toast** | They may never have seen it | Persist until dismissed |
| **Hover-only menus** | Unusable on touch | Click or focus |
| **Icon-only destructive actions** | Outcome unpredictable | Add the label |
| **A div with a click handler** | Not focusable, not announced, no Enter or Space | Use a button |
| **Removing the focus outline** | Keyboard users lose their place | Design a visible ring |
| **Hamburger menu on desktop** | Hides navigation with room to spare | Show the destinations |
| **Active nav state by colour alone** | Invisible to many users | Weight plus a rule, and `aria-current` |
| **Twelve equal KPI tiles** | Nothing is prioritised, so nothing is read | One headline, three to five supporting |
| **A figure with no comparison** | Trivia, not insight | Give it context |
| **Truncated bar chart axis** | Exaggerates differences, misleads | Start at zero |
| **A div grid instead of a table** | No row or column association | Real table markup |
| **Blocking paste** in password or code fields | Breaks every password manager | Allow paste |
| **Asking everything at signup** | Every field costs completions | Ask later, in context |

## Motion

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| **Infinite pulsing** on a button or badge | Communicates nothing after the first cycle, distracts permanently, costs battery | Draw attention once, or use position and contrast |
| **Hover scale on everything** | If every card lifts, no card is distinguished. Reads as a template | Reserve lift for genuinely interactive cards, at 2px |
| **Stagger on every list render** | The product feels slow, because it is slow. A returning user waits again | Stagger on first render only, capped at about six items |
| **Bouncy springs on utility actions** | A save button that overshoots reads as unserious. Wrong for destructive confirmations | Springs for direct manipulation only, damped |
| **Motion on mount for static content** | Content the user came to read is withheld to perform an entrance | Render it |
| **Animating from zero scale** | The element appears from nowhere, communicating no spatial relationship | 0.96 to 1 |
| **Large entrance translates** | A 40px slide is a template effect, not a spatial cue | 4 to 12px |
| **Bare ease-in-out on short transitions** | Sluggish at both ends, browser default rather than a decision | Use the easing tokens |
| **Symmetrical enter and exit** | Waiting for an exit is pure delay | Exits at 70 to 80 percent of the entrance |
| **Animating width, height, or top** | Triggers layout on every frame, drops frames | Transform and opacity |
| **Blocking input during animation** | The interface ignores the user for 300ms | Interruptible transitions |
| **Queued animations** | Delay compounds, the interface falls behind the user | Reverse from the current position |
| **Sweeping gradient shimmer** across a page of skeletons | The single effect most responsible for loading feeling cheap | Opacity pulse |
| **Parallax on a content page** | Vestibular trigger, hurts reading, costs performance | Nothing, or a very small shift |
| **Scroll reveal on every section** | Slows reading, fights the content, delays what they came for | Once or twice per page at most |
| **Count-up on every data refresh** | Unreadable while it animates, and it animates constantly | First load only, with tabular figures |
| **Animating the focus ring in** | A fast keyboard user outruns the indicator | Instant ring |
| **Autoplaying background video with no reduced-motion path** | Vestibular trigger, bandwidth cost | Poster image under reduced motion |
| **Leaving `will-change` applied permanently** | Reserves memory for an element that is not moving | Remove when the animation ends |
| **Animation running off screen or in a hidden tab** | Consumes battery for nobody | Pause when not visible |
| **Removing all motion under reduced motion** | State changes become ambiguous | Crossfade instead of travel |
| **Durations over 500ms** on anything repeated | The interface feels slow within a session | Match the size and frequency table |
| **Raw millisecond values** in the stylesheet | Timing drifts between components | Motion tokens |

See `../motion/principles.md` for the rules these violate, and
`../motion/recipes.md` for implementations that satisfy them.

## Copy

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| **Lorem ipsum in a deliverable** | Hides real length and rhythm problems | Plausible real copy |
| **Fake-looking data** | "Test User 1" undermines the whole review | Realistic names, amounts, dates |
| **Exclamation marks** | Reads nervous, undercuts confidence | A period |
| **"Oops" or "Uh oh"** | Trivialises a failure the user cares about | State what happened |
| **"Something went wrong" alone** | Gives the user nothing to act on | What happened, why, what next |
| **A raw status code as the message** | Meaningless and alarming | Plain language, reference code after |
| **"Submit" or "OK"** | Names the mechanism, not the outcome | Name the outcome |
| **"Click here"** | Meaningless out of context, poor for screen readers | Name the destination |
| **Title Case Everywhere** | Dated, harder to scan | Sentence case |
| **Blaming the user** | "You entered an invalid email" | "The email address was not recognised" |
| **Internal vocabulary** | "Payload", "entity", "sync job" mean nothing to users | The user's words |
| **"No data" as a whole empty state** | Explains nothing, offers nothing | Explain and offer the action |
| **One empty state for both cases** | First use and no results need different copy | Two states |
| **Ambiguous dates** | "04/03/2026" reads two ways | "4 Mar 2026" |
| **Unstated currency or unit** | "1,240" is not a price | Always state it |
| **"Cancel up to 24 hours before"** | Requires mental arithmetic | Give the date and time |
| **False urgency and fake scarcity** | Cheapens the brand, erodes trust | Only true information |
| **Em-dashes in generated copy** | Agents propagate the style into everything | Periods, commas, colons |
| **Success message reading only "Success"** | Wastes the peak-end moment | What happened, what next |
| **Hedging and apology** | "We are sorry, but you may need to possibly try again" | Calm, confident, specific |

## Using this file

During a build, walk it at the detail pass. During an audit, use it as the
source of findings, graded by the severity levels in `rubric.md`:

- Blocks the task or excludes a user: **Critical**.
- Measurably hurts quality: **Important**.
- Costs refinement only: **Polish**.

Report the specific instance, not the category. "Four competing primary buttons
on the overview" is actionable. "Weak hierarchy" is not.
