# Analytics and data

Analytics differs from a dashboard: a dashboard reports status, analytics
supports investigation. The user arrives with a question and needs to interrogate
the data until it is answered.

## User goals

Understand what happened, why it happened, and whether it is still happening.
Users here are patient and technical, but their patience is for the data, not
for the interface.

## Primary tasks

| Task | Served by |
|---|---|
| Ask a question | Filters, segments, date ranges |
| Compare | Period over period, segment against segment |
| Find the cause | Breakdown by dimension, drill-down |
| Confirm the number is real | Raw data access, methodology, timestamps |
| Share the finding | A URL that reproduces the exact view |

That last one is the most neglected and the most valuable.

## Information architecture

1. **Overview.** Headline metrics with comparison.
2. **Explore.** Chart plus controls plus the underlying table.
3. **Segments.** Saved definitions, reusable.
4. **Reports.** Saved views, scheduled where useful.

## Key screens

- Metric overview.
- Explore, the core screen.
- Data table with export.
- Saved report list.

## The explore screen

This is where the product lives. Its layout is a solved problem, so do not
innovate on it:

- Controls above, chart in the middle, table below.
- The table shows the same data as the chart, so the user can verify it.
- Changing a control updates both, without moving the page.
- The current query is visible and readable at all times.

Never make the user rebuild a query because they navigated away. Query state
belongs in the URL.

## Filters and query state

Follow `../patterns/search-filter.md`. In analytics specifically:

- Applied filters are always visible as removable chips.
- The result scope is stated: "12,480 events, 4 to 31 March".
- Comparison periods are explicit, never implied.
- The URL reproduces the view exactly. This is what makes findings shareable.

## Critical states

| State | Requirement |
|---|---|
| Loading | Skeleton at the chart's real dimensions |
| Empty, no data collected | Explain what produces data and how to start |
| Empty, filtered to nothing | Name the filters, offer to relax them |
| Partial | Render what loaded, mark the gap explicitly |
| Sampled | Say so, state the sample rate |
| Still processing | Say when it will be complete |
| Too much data | Offer aggregation rather than failing |
| Error | Preserve the query, explain, retry |

**Sampled and partial data are not optional states here.** A user who acts on
sampled data believing it complete has been misled by the interface.

## Trust

Analytics products live or die on whether the numbers are believed.

- State the timezone. An unstated timezone makes every daily figure ambiguous.
- Say when data was last processed.
- Explain the methodology where a metric is derived, not measured.
- Let the user reach the raw rows behind any figure.
- Never round in a way that hides a meaningful difference.
- Never interpolate across a gap silently.

A product that shows a confident number it cannot justify is worse than one
that admits uncertainty.

## Charts

Follow `../components/data-display.md`, with emphasis:

- Bar charts start at zero, always.
- Label series directly, not with a legend.
- Annotate the anomaly, the deploy, the campaign.
- Show data density honestly. Do not smooth until the line implies readings
  that were never taken.
- Offer "view as table" on every chart. It serves screen reader users and
  anyone who wants exact values.

## Export

- CSV at minimum, matching exactly what is on screen.
- Say what the export contains and its row count.
- For large exports, do it asynchronously and notify. Never freeze the page.
- Include the query parameters in the file, so a spreadsheet months later is
  still interpretable.

## Density

Density 6 to 8. This audience wants information, not air. But density is not
crowding: the grid must stay strict, and groups must still separate.

## Luxury moments

**The shareable finding.** A URL that reproduces the exact view, filters and
comparison included, turns a private discovery into something a team can act on.
It costs little and is the feature analysts talk about.

**The fast query.** An investigation is a sequence of questions. When each one
returns quickly, the user keeps going. When each takes eight seconds, they stop
at the third and never find the answer.

**Honest uncertainty.** Saying "sampled at 10 percent" or "processing, complete
by 14:00" builds more trust than a confident number the product cannot justify.

## Pitfalls

| Pitfall | Why it fails | Instead |
|---|---|---|
| Query state not in the URL | Findings cannot be shared or bookmarked | Put it in the URL |
| Unstated timezone | Every daily figure is ambiguous | State it |
| Silent sampling | User acts on incomplete data as though complete | Say so, with the rate |
| Truncated bar axis | Exaggerates differences, misleads | Start at zero |
| Chart with no underlying table | Numbers cannot be verified | Always offer the table |
| Smoothing across gaps | Invents measurements | Show the gap |
| Losing the query on navigation | Rebuilding is where users give up | Preserve it |
| Freezing the page on export | Blocks all work | Async, then notify |
| Comparison period implied | User assumes the wrong baseline | State it explicitly |
| Twelve charts on one screen | Nothing is read | One question per view |

## Recommended directions and dials

| Product | Direction | Opulence | Density | Motion |
|---|---|---|---|---|
| Product analytics, BI | Swiss Precision | 2 | 7 | 2 |
| Observability, infrastructure | Functional Futurism | 3 | 8 | 3 |
| Executive reporting | Obsidian | 4 | 5 | 2 |

Opulence stays low. Decoration in an analytics product actively competes with
the data, and motion beyond state changes makes rapid iteration feel sluggish.

## Related references

`../components/data-display.md`, `../components/tables.md`,
`../patterns/search-filter.md`, `../patterns/states.md`,
`../foundations/typography.md`.
