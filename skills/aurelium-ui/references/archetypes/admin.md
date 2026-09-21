# Admin and data tables

An internal tool used for hours a day by people who know it well. Speed and
density matter more than delight. Being slow to operate is the failure mode.

## User goals

Find records, change them correctly, and do it quickly. These users are
experts. Treat them as such.

## Primary tasks

| Task | Served by |
|---|---|
| Find records | Search and filter that are fast and precise |
| Scan many at once | A dense, well-aligned table |
| Inspect one | A detail view that does not lose the list |
| Change one | Inline editing or a drawer |
| Change many | Bulk actions with a clear scope |
| Undo a mistake | Reversible actions, visible history |

## Information architecture

1. **List.** The home screen. Filters, table, bulk actions.
2. **Detail.** A drawer beside the list, or a full page for complex records.
3. **Audit.** Who changed what, when.

Keep the list as the centre of gravity. Every route leads back to it without
losing scroll, filters, or selection.

## Key screens

- Record list, with filters and bulk actions.
- Record detail, as a drawer beside the list.
- Create and edit forms.
- Audit or activity history.

## The list

Density 7 to 9. This is the one archetype where compression is correct.

- Rows 32 to 40px.
- Tabular figures on every numeric column.
- Sticky header, and a sticky first column when scrolling horizontally.
- Column visibility and order configurable, and remembered.
- Density toggle, remembered.
- Result count and active filters always visible.

See `../components/tables.md` for the full treatment.

## Keyboard

The defining quality of a good admin tool. Users will operate it all day.

| Key | Action |
|---|---|
| `/` or `Ctrl K` | Focus search or open the command palette |
| Arrow up and down | Move between rows |
| `Enter` | Open the focused row |
| `Space` | Select the focused row |
| `Shift` plus arrow | Extend selection |
| `Esc` | Close drawer, clear selection |
| `?` | Show shortcuts |

Rules:

- Every shortcut is discoverable, via `?` and in menus beside the action.
- Shortcuts never fire while typing in a field.
- Focus is visible at all times and never lost after an action.
- After deleting a row, focus moves to the next row, not to the page body.

That last point is the difference between a tool that feels fast and one that
feels broken.

## Bulk actions

- The scope is unambiguous. "All 50 on this page" and "All 1,284 matching" are
  different, and the interface must distinguish them explicitly.
- The action bar states the count and never shifts the table when it appears.
- Destructive bulk actions confirm with the count and the scope: "Delete 1,284
  records matching this filter".
- Show progress for long operations, and report partial failures honestly:
  "1,280 updated, 4 failed" with a route to the failures.

A bulk operation that silently half-succeeds is the worst outcome in this
archetype.

## Detail drawer

- Opens beside the list, preserving context, which is why it beats a full page.
- The list stays visible and the current row is marked.
- Keyboard navigation moves between records without closing.
- Unsaved changes warn before closing, including on `Esc`.
- Deep-linkable, so a record can be shared.

See `../components/overlays.md` for the focus rules.

## Editing

- Inline editing for single fields, with an explicit save or a clear
  auto-save indicator.
- Optimistic updates with visible revert on failure.
- Validate at the field, not only on submit.
- Show who last changed a record and when.
- Never silently discard a change because another user saved first. Say so and
  offer the choice.

## Critical states

| State | Requirement |
|---|---|
| Loading | Skeleton rows at the real height |
| Empty, no records | Explain and offer creation |
| Empty, filtered | Name the filters, offer to clear |
| Too many results | Paginate or virtualise, state the total |
| Save conflict | Explain, show both versions, let the user choose |
| Partial bulk failure | Count of each, route to the failures |
| Permission denied | Name who can grant it |
| Long values | A 200 character field must not break the row |

## Luxury moments

**Fast keyboard operation.** A user who can work without touching the mouse
feels the tool respects their time. This is the luxury of an internal product.

**Undo.** Reversibility removes the fear that makes people slow and cautious.

**The honest bulk report.** Telling the user exactly what succeeded and what
did not, with a route to fix the rest, is the mark of a tool built by someone
who has used one.

## Pitfalls

| Pitfall | Why it fails | Instead |
|---|---|---|
| Consumer spacing in an admin tool | Constant scrolling, fewer records visible | Density 7 to 9 |
| Losing filters on navigation | Rebuilding state all day | Preserve in the URL |
| Ambiguous bulk scope | The wrong 1,284 records get deleted | State the scope explicitly |
| Silent partial failure | User believes it worked | Report both counts |
| No keyboard support | Slow for the only people who use it | Full keyboard operation |
| Focus lost after an action | Keyboard flow breaks every time | Move focus deliberately |
| Confirm dialog on every action | Learned dismissal | Undo where possible |
| Full page reload for detail | Loses scroll and context | Drawer |
| Last write silently wins | Data lost without anyone knowing | Surface the conflict |
| Non-resizable, non-hideable columns | Every user has different needs | Configurable and remembered |

## Recommended directions and dials

| Tool | Direction | Opulence | Density | Motion |
|---|---|---|---|---|
| General internal admin | Swiss Precision | 2 | 8 | 2 |
| Infrastructure, ops | Functional Futurism | 3 | 8 | 2 |
| Customer-facing back office | Obsidian | 3 | 7 | 2 |

Opulence and motion both stay at the floor. An internal tool used for six hours
a day should be quiet. Ornament that is charming once is irritating on the
three-hundredth repetition.

## Related references

`../components/tables.md`, `../components/overlays.md`,
`../components/forms.md`, `../patterns/search-filter.md`,
`../patterns/feedback.md`, `../patterns/states.md`.
