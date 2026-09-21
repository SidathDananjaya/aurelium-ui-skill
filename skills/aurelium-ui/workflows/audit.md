# Audit and Elevate workflow

Score an existing interface, report findings by severity, then upgrade it.

Audit the work, never the person who wrote it. Findings describe the artefact.

## 1. Reconnaissance

Before judging anything, establish what you are looking at:

| Question | How to answer |
|---|---|
| What stack? | Read the config and the markup |
| What archetype? | Identify the primary task |
| Are there tokens? | Search for custom properties, a theme file, or `DESIGN.md` |
| What direction is implied? | Palette temperature, radius, type, density |
| Who uses it, how often? | Ask, or infer from the content |

If a `DESIGN.md` exists, the audit measures the build against **its own stated
system** first, and against Aurelium's doctrine second. An inconsistency with
the project's own rules is a stronger finding than a difference from ours.

## 2. Score

Use `../references/quality/rubric.md`. Score each category 1 to 10 with a one
line justification naming specific evidence. The weighting:

| Category | Weight | Judged on |
|---|---|---|
| Design | 40% | Hierarchy, typography, colour restraint, spacing rhythm, consistency, detail precision |
| Usability | 30% | Clarity of primary actions, navigation, feedback, states, forms, accessibility |
| Creativity | 20% | Signature details, originality within convention, luxury moments |
| Content | 10% | Microcopy quality, information clarity, realistic data |

Then run the craft checklist as pass or fail, with no partial credit:

- Semantic HTML, correct heading order.
- Motion quality, and a reduced-motion path.
- Accessibility baseline in `../references/doctrine/accessibility.md`.
- Performance budget in `../references/doctrine/performance.md`.
- Responsive at 375, 768, 1024, 1440.
- Clean markup and metadata.

A failed craft item caps the related category at 6, however good it looks.

## 3. Findings

Group by severity. Within each group, order by impact.

| Severity | Means |
|---|---|
| **Critical** | Blocks the task, or excludes a user. Contrast failures, keyboard traps, unlabelled inputs, broken flows |
| **Important** | Measurably hurts quality. Weak hierarchy, missing states, inconsistent components, poor error copy |
| **Polish** | Luxury-grade refinement. Optical alignment, tracking, tabular figures, motion timing |

Every finding carries four parts, in this order:

```
Location   Checkout, step 2, the postcode field
Issue      The label is a placeholder, so it disappears once typing starts
Principle  Placeholders are not labels. accessibility.md, Forms
Fix        Add a visible label above the input, keep the placeholder for
           format guidance only, and link the error with aria-describedby
```

Report the check you ran, not just the verdict. "Tabbed the filter drawer, Esc
did not close it" is actionable. "Poor keyboard support" is not.

Do not pad the list. Twelve real findings beat forty restatements of the same
spacing problem. When one root cause produces many symptoms, report the cause
once and name the symptoms under it.

## 4. Elevation plan

Propose a direction and dials, or confirm what is already there. Changing
direction is a large intervention. Recommend it only when the current one is
incoherent or actively fights the product, and say what it will cost.

Then give the **top five changes by impact**, ordered. For each: what changes,
which findings it resolves, and roughly how much work it is.

Most interfaces improve more from fixing spacing rhythm and hierarchy than from
a new palette. Recommend accordingly, even when a repaint would be more
visible.

## 5. Apply

Only if the user asks. Critical first, then Important, then Polish.

Work in small, reviewable changes. Do not rewrite a working component to match
house style while fixing a contrast bug in it. State clearly which findings each
change resolves.

After applying, re-run `../references/quality/preflight.md` in full, and report
what now passes that did not before.

## 6. Output

A Markdown report in chat by default. Write `aurelium-audit.md` into the project
only if the user asks for a file.

Structure:

```
## Summary
Two or three sentences. The single most important thing to fix.

## Scores
The four categories with justifications, and the weighted total.

## Craft checklist
Pass or fail per item.

## Findings
Critical, then Important, then Polish.

## Elevation plan
Direction and dials, then the top five changes.
```

Lead with the most important finding, not the easiest one to describe. If the
interface is good, say so plainly and keep the findings short. An audit that
manufactures problems to look thorough is worse than no audit.
