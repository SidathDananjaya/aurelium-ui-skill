# Create workflow

Brief to shipped UI. Work the steps in order. Do not skip to writing code.

## 1. Infer the brief

Extract, from what the user gave you:

| Field | If missing |
|---|---|
| Product type and audience | Infer from context, state the assumption |
| Archetype | Infer from the primary task |
| Brand cues | Assume none, use a direction's defaults |
| Stack | Default to HTML and CSS |
| Existing tokens or `DESIGN.md` | Search the project before assuming none |
| Success metric | Infer the one action that matters most |

**Ask at most one question, and only when a wrong guess would waste real work.**
Which archetype it is, or what the primary action is, can justify a question.
Colour preference does not. Otherwise state your assumptions in two to four
lines and proceed.

If the project already contains a `DESIGN.md`, read it and follow it. An
existing system outranks your preference, even when you would have chosen
differently. Say so if you disagree, then comply.

## 2. Choose direction and dials

Pick one direction using `../references/directions/index.md`. Set the three
dials. State the choice and a one sentence reason.

> Obsidian at opulence 4, density 6, motion 3. A payments dashboard needs
> restraint and dense figures, and the audience reads it daily.

Defaults when nothing in the brief points either way: opulence 4, density 5,
motion 4, theme auto.

## 3. Generate the design system

```
python scripts/tokens.py --direction obsidian --opulence 4 --density 6 --motion 3 --theme auto --format css
```

Write the result to the project as a stylesheet. Never hand-write token values
that the script can produce.

Then persist a `DESIGN.md` at the project root recording the direction, the
dials, the token file location, and any project specific decisions. Later
sessions read it instead of guessing, which is what keeps a product coherent
across conversations.

## 4. Information architecture

Before any markup, list:

- Every screen.
- The single primary action per screen.
- The navigation model, and where the user is at each point.
- What data each screen needs, and what happens when it is absent.

One primary action per screen. If a screen seems to need two, one of them is
secondary, or it is two screens.

## 5. Layout

Set the grid and the breakpoints: 375, 768, 1024, 1440. For each screen name
the single focal point, and confirm the reading order runs headline, then key
figure or action, then supporting content.

Apply the rules in `../references/foundations/spacing-layout.md`. Inner spacing
smaller than outer spacing, every time.

## 6. Build components

Tokens only. No hard-coded colour, size, radius, shadow, or duration anywhere
in the markup or stylesheet.

**Check.** Grep your output for hex colours and raw pixel values. Every hit is
either a token definition or a bug.

Follow `../references/foundations/` for each building block, and the chosen
direction's file for its specific component notes.

## 7. Implement every state

For each data-driven view, build all of these. This is not optional and it is
the step most often skipped:

| State | Requirement |
|---|---|
| Default | The normal case |
| Loading | A skeleton matching the real content's dimensions, not a spinner |
| Empty, first use | Explains the feature and offers the primary action |
| Empty, no results | Names what was searched and offers to clear filters |
| Error, recoverable | What happened, why, what to do next, with a retry |
| Error, fatal | Plain explanation, a way out, and what was preserved |
| Partial data | Renders what loaded, marks what did not |
| Offline | Where applicable, with recovery behaviour |
| Success | Confirms what happened and what comes next |
| Long content | Very long names, many items, no overflow or clipping |
| Permission denied | Where applicable, explaining who can grant access |

Write the copy for each state using `../references/foundations/microcopy.md`.

## 8. Motion pass

Add motion to the level the MOTION dial sets, and no more.

- Every animation has a stated purpose. If you cannot say what it communicates
  in one sentence, remove it.
- `transform` and `opacity` only.
- Every transition has a `prefers-reduced-motion` alternative that still
  communicates the state change.
- No infinite animation except a live status indicator.

## 9. Detail pass

Walk this before you consider the work finished:

- Optical alignment corrected where maths and eye disagree.
- `font-variant-numeric: tabular-nums` on every figure that changes or aligns.
- `text-wrap: balance` on headings, `pretty` on paragraphs.
- Focus visible on every interactive element, never removed.
- Hover, active, and disabled states designed, not defaults.
- No orphaned words in headings, no clipped text at any breakpoint.
- Microcopy: buttons are verbs, errors name a fix, no exclamation marks.
- Realistic content. Never lorem ipsum, never obviously fake data.

## 10. Pre-flight

Run the contrast check on the token set:

```
python scripts/contrast.py --tokens tokens.css
```

Then confirm, by actually checking rather than assuming:

1. Every contrast pair passes AA.
2. Exactly one primary action per view.
3. Every state from step 7 exists.
4. Tab through each screen: focus always visible, order matches the visual
   order, `Esc` closes overlays.
5. Smallest interactive target is at least 24 by 24, primaries at least 44.
6. Reduced motion still communicates every state change.
7. Renders at 375, 768, 1024, and 1440 with no horizontal scroll.
8. Reflows at 320px and at 200 percent zoom.
9. No console errors.
10. Every image has reserved dimensions.

## 11. Report

Close with the output contract from `../SKILL.md`: direction and dials, files
changed, pre-flight results, and known gaps stated plainly.

Report what you did not do as clearly as what you did. A known gap named is a
professional handoff. A known gap hidden is a defect you shipped.
