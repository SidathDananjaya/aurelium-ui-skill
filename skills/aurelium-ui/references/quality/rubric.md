# Scoring rubric

Used by the audit workflow to score an interface, and available during a build
as a self-check.

The category weighting is informed by publicly described judging criteria for
web design awards, which commonly weigh design, usability, creativity, and
content. Aurelium UI is independent and is not affiliated with, endorsed by, or
connected to any awards organisation. See `../../../../CREDITS.md`.

## Weighting

| Category | Weight | What is judged |
|---|---|---|
| Design | 40% | Hierarchy, typography, colour restraint, spacing rhythm, consistency, detail precision |
| Usability | 30% | Clarity of primary actions, navigation, feedback, states, forms, accessibility |
| Creativity | 20% | Signature details, originality within convention, luxury moments |
| Content | 10% | Microcopy quality, information clarity, realistic data |

Score each 1 to 10, then weight. Give a one line justification per category
naming the specific evidence, not the impression.

## Scoring scale

Use the whole range. Most real interfaces sit between 4 and 7, and a rubric
where everything scores 8 measures nothing.

| Score | Means |
|---|---|
| 1 to 2 | Broken. Fails at the basic task or excludes users outright |
| 3 to 4 | Below standard. Works, but visibly unconsidered |
| 5 to 6 | Competent. Conventional, correct, unremarkable |
| 7 to 8 | Good. Deliberate decisions, consistent execution, few flaws |
| 9 | Excellent. Considered throughout, with real craft in the details |
| 10 | Exceptional. Reserve it. If everything is a 10, the scale is useless |

## Design, 40 percent

| Score | Looks like |
|---|---|
| 1 to 2 | No hierarchy. Arbitrary spacing. Colour applied at random |
| 3 to 4 | Some structure, but off-scale values, inconsistent components, weak contrast between levels |
| 5 to 6 | A coherent system applied consistently. Nothing wrong, nothing memorable |
| 7 to 8 | Clear hierarchy, disciplined palette, consistent rhythm, evidence of optical correction |
| 9 to 10 | Every screen reads in a deliberate order. Typography carries the brand. Details survive scrutiny at 400 percent zoom |

Evidence to cite: type scale ratios, count of hues outside neutrals, spacing
values off the scale, elevation levels in use, alignment across sections.

## Usability, 30 percent

| Score | Looks like |
|---|---|
| 1 to 2 | Primary task cannot be completed, or fails accessibility outright |
| 3 to 4 | Task completable with effort. Missing states, unclear actions, keyboard gaps |
| 5 to 6 | Conventional patterns used correctly. Main states present |
| 7 to 8 | Every state designed. Full keyboard operation. Errors name fixes |
| 9 to 10 | Complexity absorbed by the system. Forgiving input, reversible actions, nothing to learn |

Any failure in the accessibility baseline caps this category at 6, whatever
else is true.

## Creativity, 20 percent

Creativity here means considered originality, not novelty. An interface that
invents a new checkout flow scores badly. One that uses a conventional flow with
a memorable, appropriate detail scores well.

| Score | Looks like |
|---|---|
| 1 to 2 | Template output. Nothing distinguishes it from any other product |
| 3 to 4 | Generic with a colour change |
| 5 to 6 | A coherent voice, no signature |
| 7 to 8 | Recognisable character. One or two details that would be remembered |
| 9 to 10 | A distinct point of view, executed without costing usability. The luxury moments land |

Innovating on basic interaction mechanics costs points here rather than earning
them. See Jakob's law in `../doctrine/ux-laws.md`.

## Content, 10 percent

| Score | Looks like |
|---|---|
| 1 to 2 | Lorem ipsum, or data that is obviously fake |
| 3 to 4 | Real words, but vague. Errors that say "invalid" |
| 5 to 6 | Clear and correct, unremarkable |
| 7 to 8 | Specific, human, consistent voice. Errors name fixes. Empty states guide |
| 9 to 10 | Copy does real design work. The confirmation answers the question before it is asked |

## Craft checklist

Pass or fail, no partial credit. These are not scored, they gate the score.

| # | Item | Pass means |
|---|---|---|
| C1 | Semantic HTML | Correct elements, correct heading order |
| C2 | Motion quality | Purposeful, token-based, with a reduced-motion path |
| C3 | Accessibility baseline | Every item in `../doctrine/accessibility.md` |
| C4 | Performance budget | Every item in `../doctrine/performance.md` |
| C5 | Responsive | 375, 768, 1024, 1440, plus 320px reflow |
| C6 | Clean markup | No dead nodes, correct metadata, no console errors |

**A failed craft item caps its related category at 6.** C1 and C3 cap
Usability. C2 caps Design. C4 and C5 cap Usability. C6 caps Design.

An interface cannot look excellent while being unusable to a keyboard user.
The cap encodes that.

## Worked example

```
Design        7/10  Disciplined palette and consistent 4px rhythm. Loses points
                    for a flat KPI row where nothing is prioritised.
Usability     5/10  Capped at 6 by C3: the filter drawer traps focus and Esc
                    does not close it. Otherwise conventional and correct.
Creativity    6/10  Coherent voice, no signature detail. The confirmation
                    screen is the one memorable moment.
Content       8/10  Specific error copy, realistic data, good empty states.

Weighted      6.3/10

Craft         C1 pass  C2 pass  C3 FAIL  C4 pass  C5 pass  C6 pass
```

The weighted total is `(7 x 0.4) + (5 x 0.3) + (6 x 0.2) + (8 x 0.1) = 6.3`.

## Reporting a score

- Lead with the single most important finding, not the easiest to describe.
- Name evidence, not impressions. "Four competing primary buttons on the
  overview" beats "hierarchy could be stronger".
- If the interface is good, say so plainly and keep the findings short. An
  audit that manufactures problems to look thorough is worse than no audit.
- Separate what is wrong from what is merely different from your preference.

## Related references

`../../workflows/audit.md` for the full audit procedure,
`anti-patterns.md` for what to look for, `preflight.md` for the pass or fail
gate, `detail-checklist.md` for the finer craft items.
