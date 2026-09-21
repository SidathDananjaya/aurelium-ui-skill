# Tables

A table compares values across records. If the user is not comparing, a list
reads better.

## Structure

Use real table markup. A grid of `div` elements is not a table to a screen
reader, and loses row and column association entirely.

```html
<table class="table">
  <caption class="visually-hidden">Recent transactions</caption>
  <thead>
    <tr>
      <th scope="col">Date</th>
      <th scope="col">Description</th>
      <th scope="col" class="num">Amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">4 Mar 2026</th>
      <td>Harbour Suite, 2 nights</td>
      <td class="num">480.00</td>
    </tr>
  </tbody>
</table>
```

`scope` on headers is what associates a cell with its column and row. The
caption names the table, and may be visually hidden when a heading above it
already says the same thing.

## Alignment

| Content | Alignment |
|---|---|
| Text | Start |
| Numbers | End, with tabular figures |
| Dates | Start, one format throughout |
| Status | Start, with an icon and a word |
| Actions | End |

Numbers align on the decimal, which end alignment plus tabular figures gives
you. This is the single biggest legibility win in a data table.

```css
.table {
  inline-size: 100%;
  border-collapse: collapse;
  font-size: var(--text-xs);
}

.table th,
.table td {
  text-align: start;
  padding: var(--space-3) var(--space-4);
  border-block-end: 1px solid var(--color-border);
}

.table thead th {
  color: var(--color-text-muted);
  font-weight: 600;
  position: sticky;
  inset-block-start: 0;
  background: var(--color-surface);
  z-index: 1;
}

.table .num {
  text-align: end;
  font-variant-numeric: tabular-nums lining-nums;
}

.table tbody tr:hover { background: var(--color-page); }
```

No vertical rules. Horizontal hairlines are enough, and vertical lines make a
table look like a spreadsheet rather than a considered view.

Zebra striping is a workaround for rows that are too tall or too tightly
spaced. Fix the spacing instead. Reserve striping for tables wider than the
viewport.

## Density

| Density dial | Row height | Padding |
|---|---|---|
| 1 to 3 | 56px and above | `--space-4` |
| 4 to 6 | 44 to 52px | `--space-3` |
| 7 to 10 | 32 to 40px | `--space-2` |

Offer a density control in professional tools and remember the choice. Never
go below 32px rows, where the eye loses the line.

## Sticky headers

The header stays visible while the body scrolls. Give it an opaque background,
or content shows through as it passes underneath.

If the first column identifies the row, make it sticky too when the table
scrolls horizontally.

## Sorting

- The sortable header is a button inside the `th`, not a click handler on the
  cell.
- The current sort is announced with `aria-sort`.
- The direction is shown with a glyph, not colour.
- Sorting preserves selection and scroll position where possible.

```html
<th scope="col" aria-sort="descending">
  <button type="button">Amount</button>
</th>
```

## Selection and bulk actions

- The header checkbox selects the current page, and says so.
- When a page is selected, offer "Select all 312 matching" explicitly.
- The bulk action bar appears without shifting the table, by overlaying or by
  occupying reserved space.
- The bar states the count: "3 selected".
- Destructive bulk actions name the count in the confirmation: "Delete 3
  bookings".

## Responsive strategy

Pick one and apply it consistently. There is no universally right answer.

| Strategy | Works when | Cost |
|---|---|---|
| Horizontal scroll | Many columns, comparison matters | Some columns hidden initially |
| Column priority | A few columns matter most | Hidden data needs a detail view |
| Stack into cards | Few columns, scanning not comparing | Comparison becomes impossible |

If you scroll horizontally, say so. A table that scrolls with no visible
affordance reads as clipped content.

```css
.table-scroll {
  overflow-x: auto;
  /* Prevents a focused cell being scrolled under the sticky header */
  scroll-padding-block-start: 3rem;
}
```

## Actions per row

One action per row inline, the rest in a menu. A row with four icon buttons is
noise, and each one needs an accessible name anyway.

The menu button carries the row's identity: `aria-label="Actions for Harbour
Suite"`, not `aria-label="Actions"` repeated forty times.

## States

- **Loading**: skeleton rows matching the real row height, not a spinner.
- **Empty, first use**: explain what will appear and offer the action.
- **Empty, filtered**: name the filter and offer to clear it.
- **Error**: keep the header, explain in the body, offer retry.
- **Long content**: a 200 character description must not break the layout.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| `div` grid instead of `table` | No row or column association | Real table markup |
| Proportional figures in number columns | Columns visibly wobble | `tabular-nums` |
| Numbers aligned to the start | Decimals do not line up | Align to the end |
| Vertical rules everywhere | Reads as a spreadsheet | Horizontal hairlines only |
| Zebra striping by default | Patching a spacing problem | Fix spacing |
| Transparent sticky header | Content shows through | Opaque background |
| Sort direction by colour only | Invisible to many users | Glyph plus `aria-sort` |
| Four icon buttons per row | Noisy, ambiguous | One inline, rest in a menu |
| "Select all" that only selects the page | Users delete the wrong scope | State the count explicitly |
