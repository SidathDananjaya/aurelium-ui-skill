# Search and filter

Search finds a known item. Filter narrows an unknown set. They solve different
problems and often belong together.

## Search

| Decision | Rule |
|---|---|
| Placement | Where the content is, not hidden behind an icon on desktop |
| Trigger | Debounced live results, or explicit submit for expensive queries |
| Debounce | 200 to 300ms. Shorter floods, longer feels laggy |
| Minimum length | 2 characters before querying |
| Scope | Stated. "Search bookings" not "Search" |

```html
<form role="search" class="search">
  <label for="q" class="visually-hidden">Search bookings</label>
  <input
    id="q"
    type="search"
    name="q"
    placeholder="Guest name or reference"
    autocomplete="off"
    aria-describedby="q-count"
  />
  <p id="q-count" role="status" class="visually-hidden">24 results</p>
</form>
```

```css
.search input {
  inline-size: 100%;
  min-block-size: 44px;
  padding: var(--space-3) var(--space-4);
  font: inherit;
  color: var(--color-text);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.search input:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

The visible label may be hidden when the placeholder and context make the
purpose obvious, but the label element must still exist. Here the placeholder
gives examples rather than repeating the label, which is what placeholders are
for.

Announce the result count in a live region. Sighted users see the list change.
Everyone else needs to be told.

Rules:

- Be forgiving: ignore case, trim whitespace, tolerate misspellings where you
  can, match on partial words.
- Search what the user knows: guest name, reference, email, not internal IDs
  only.
- Preserve the query in the URL so results can be shared and the back button
  works.
- A clear button appears once there is a query, and returns focus to the input.

## Autocomplete and suggestions

- Suggestions are navigable with arrow keys, selectable with Enter, dismissed
  with `Esc`.
- The input keeps focus throughout. Focus never jumps into the list.
- Highlight the matched substring, and never highlight with colour alone.
- Show at most about seven suggestions.
- Recent searches are useful. Say they are recent.

```html
<input role="combobox" aria-expanded="true" aria-controls="suggestions" aria-autocomplete="list" />
<ul role="listbox" id="suggestions">
  <li role="option" aria-selected="false">Harbour Suite</li>
</ul>
```

## Filters

| Filter kind | Control |
|---|---|
| A few exclusive options | Segmented control or radio |
| Many non-exclusive options | Checkbox list |
| Range | Two inputs, or a slider with numeric inputs beside it |
| Date range | A picker with sensible presets |
| Many values | Searchable multi-select |

Always pair a slider with numeric inputs. A slider alone cannot be operated
precisely, and is difficult with a trackpad or by keyboard.

## Applied filters must be visible

The single most common filter failure is a user seeing an empty list with no
idea why.

- Show applied filters as removable chips above the results.
- Show the result count at all times.
- Provide "Clear all" once more than one filter is applied.
- Never hide an active filter inside a collapsed panel with no indicator.

```html
<div class="chips" aria-label="Applied filters">
  <button type="button" class="chip">
    Sea view
    <span aria-hidden="true">&#215;</span>
    <span class="visually-hidden">Remove sea view filter</span>
  </button>
</div>
<p role="status">24 of 312 properties</p>
```

Each chip's accessible name says what removing it does. A bare multiplication
sign announces nothing useful.

## Apply immediately or on submit

| Approach | Use when |
|---|---|
| Immediate | Cheap queries, few filters, desktop |
| Explicit apply | Expensive queries, many filters, mobile sheets |

Pick one per surface. Mixing them, where some filters apply instantly and
others need a button, is reliably confusing.

If applying immediately, do not move the results under the user's pointer as
they work.

## URL state

Filters and search belong in the URL. This gives sharing, bookmarking, the back
button, and refresh-without-loss for free.

Keep it readable: `?q=harbour&view=sea&from=2026-03-04`. Never put personal data
in a query string.

## Results

- State the count and the scope: "24 of 312 properties".
- Say what is being sorted by, and let the user change it.
- Preserve scroll position when returning from a detail view.
- Keep the query visible in the results header.

## Empty results

The most important state in this pattern, and the most neglected.

```
No properties match "oakwood" with a sea view in March.
[ Clear filters ]  [ Search all dates ]
```

Name the query and the filters. Offer the specific way out, not just a generic
reset. If you can, suggest the nearest match: "3 properties match without the
sea view filter."

## Performance

- Debounce input, and cancel superseded requests.
- Never let an older response overwrite a newer one. Race conditions here
  produce results that do not match the query, which reads as a broken product.
- Paginate or virtualise long result sets.
- Keep the previous results visible while loading the next, dimmed rather than
  cleared.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Hidden active filters | Empty list with no explanation | Visible removable chips |
| No result count | User cannot tell if the filter worked | Always show the count |
| Searching on every keystroke | Floods the server, results flicker | Debounce 200 to 300ms |
| Stale response overwriting fresh | Results do not match the query | Cancel superseded requests |
| Clearing results while loading | Page collapses and jumps | Dim the previous results |
| Filter state not in the URL | Back button and sharing break | Put it in the URL |
| Slider with no numeric input | Cannot be set precisely | Pair with inputs |
| Generic "No results found" | No route forward | Name the query, offer the fix |
| Mixed instant and apply filters | Unpredictable | One behaviour per surface |
| Icon-only search on desktop | Hides the primary way to find things | Show the field |
