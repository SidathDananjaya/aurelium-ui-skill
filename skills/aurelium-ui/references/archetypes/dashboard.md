# SaaS dashboard

A dashboard answers "is everything alright, and what needs me?" If it cannot
answer that in five seconds, it is a report, not a dashboard.

## User goals

Users open a dashboard repeatedly, often daily, usually while doing something
else. They are scanning for change, not reading.

## Primary tasks

| Task | Served by |
|---|---|
| Check status at a glance | One headline figure, above the fold |
| Spot what changed | Comparison against a period, not raw values |
| Find what needs action | A clear, short list of items requiring them |
| Go deeper | A route from any figure to its detail |
| Act | The one or two actions done most often |

## Information architecture

1. **Overview.** The default view. One headline insight, supporting figures,
   then what needs attention.
2. **Detail views.** One per entity, reachable from any figure.
3. **Settings.** Account, team, billing, integrations.

Depth beats breadth. Three well-designed views beat twelve shallow ones.

## Key screens

- Overview.
- Entity list, with filters.
- Entity detail.
- Settings.

## The first-load overview

This is the screen the user sees most often in the product's lifetime. It
deserves the most care.

- **One headline insight**, not a wall of equal tiles. Something should be
  larger and first.
- Three to five supporting figures. Never twelve.
- Every figure carries a comparison. A number alone is trivia.
- What needs attention appears without scrolling.
- Default to the period the user actually cares about, usually this month or
  the last 30 days, and remember their choice.

**Check.** Show the overview to someone unfamiliar for five seconds, then hide
it. Ask what the most important thing was. If they cannot say, the hierarchy is
flat.

## Critical states

| State | Requirement |
|---|---|
| Loading | Skeletons at the real dimensions. Never a full-page spinner |
| Empty, new account | Explain what will appear and how to make it appear |
| Empty, no activity this period | Different from new. Say so, offer another period |
| Partial | Render what loaded, mark what failed, offer retry for the rest |
| Error | Keep the layout, explain in place, retry |
| Stale data | Say when it was last updated. Never show old data as current |
| Permission denied | Name who can grant access |

Stale data is the state most often missed and the most damaging. A figure with
no timestamp is a figure the user cannot trust.

## Luxury moments

**The first load.** Fast, with one clear insight rather than a grid of equal
weight. The difference between a dashboard that feels expensive and one that
feels generated is whether anything is prioritised.

**The drill-down.** Every figure leads somewhere. A number the user cannot
interrogate is a dead end, and dead ends feel cheap.

**The empty account.** The first thing a new customer sees. Treat it as
onboarding, not as an error.

## Density and layout

Dashboards run denser than marketing pages and lighter than admin tables.
Density 5 to 7 is usual.

- Align everything to one grid. Misalignment is more visible here than anywhere
  because the eye scans in columns.
- Group by question answered, not by data source.
- Keep the figure and its label close, and the groups far apart.
- Do not fill the viewport for its own sake. Empty space below the fold is
  better than a chart nobody asked for.

## Charts

Follow `../components/data-display.md`. In a dashboard specifically:

- Prefer one well-chosen chart over four decorative ones.
- Annotate the thing that matters: the target line, the anomaly.
- Label series directly rather than with a legend.
- Never use a donut chart for more than three segments.

## Refresh and real time

- Say when data was last updated.
- Live updates must not shift the layout. Use tabular figures and reserved
  widths.
- Never animate a figure changing while the user is reading it.
- Offer manual refresh. Automatic refresh that resets scroll or selection is
  hostile.

## Pitfalls

| Pitfall | Why it fails | Instead |
|---|---|---|
| Twelve equal KPI tiles | Nothing is prioritised, so nothing is read | One headline, three to five supporting |
| Figures with no comparison | Trivia, not insight | Compare to a period |
| No timestamp on data | User cannot tell if it is current | Always say when |
| Charts chosen for variety | Decoration, not communication | Choose by the question |
| Full-page spinner | Layout unknown until it resolves | Skeletons |
| Dead-end figures | Nowhere to interrogate | Every figure drills down |
| Layout shift on live update | Unreadable while updating | Reserve width, tabular figures |
| Same empty state for new and quiet | Two different situations | Two states |
| Defaulting to "all time" | Rarely the question being asked | Default to the useful period |
| Twelve navigation destinations | Exceeds comfortable scanning | Group, or cut |

## Recommended directions and dials

| Product | Direction | Opulence | Density | Motion |
|---|---|---|---|---|
| Premium B2B SaaS | Obsidian | 4 | 6 | 3 |
| Analytics, BI | Swiss Precision | 3 | 7 | 2 |
| Infrastructure, AI, security | Functional Futurism | 4 | 7 | 3 |
| Consumer-facing SaaS | Tactile Craft | 4 | 5 | 4 |

Motion stays low. A dashboard opened twenty times a day must not animate on
every load.

## Related references

`../components/data-display.md`, `../components/tables.md`,
`../components/navigation.md`, `../patterns/states.md`,
`../patterns/feedback.md`.
