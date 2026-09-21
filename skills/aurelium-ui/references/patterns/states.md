# States

Every data-driven view ships every state below. This is the rule most often
skipped, and skipping it is what separates a demo from a product.

A view is not finished when the happy path renders.

## The complete set

| State | When | Must contain |
|---|---|---|
| Default | Data loaded, normal case | The content |
| Loading | Request in flight | Skeleton matching real dimensions |
| Empty, first use | Nothing exists yet | What this is, why it is empty, the action |
| Empty, no results | Filter or search matched nothing | What was searched, how to clear it |
| Error, recoverable | Request failed, retry may work | What happened, why, retry |
| Error, fatal | Cannot proceed | Plain explanation, a way out, what was preserved |
| Partial data | Some sources failed | What loaded, what did not, retry for the rest |
| Offline | Connection lost, where applicable | Status, what still works, recovery |
| Success | Action completed | What happened, what is next |
| Long content | Very long values, many items | No overflow, no clipping, no broken layout |
| Permission denied | User lacks access | Who can grant it, how to ask |

Not every view needs offline or permission denied. Every view needs the rest.

## Loading

A skeleton matches the dimensions of the content that replaces it. A skeleton
of a different height causes the layout shift it was meant to prevent.

```html
<div class="skeleton-row" aria-hidden="true"></div>
<p class="visually-hidden" role="status">Loading bookings</p>
```

```css
.skeleton-row {
  block-size: 44px;
  border-radius: var(--radius-sm);
  background: var(--color-border);
}

@media (prefers-reduced-motion: no-preference) {
  .skeleton-row {
    animation: skeleton-pulse var(--duration-slow) ease-in-out infinite alternate;
  }
}

@keyframes skeleton-pulse {
  to { opacity: 0.55; }
}
```

Rules:

- Under 400ms, show nothing. A flash of skeleton is worse than a brief wait.
- Over 400ms, skeleton. Never a bare centred spinner for a whole page.
- The shimmer is decorative, so it is hidden from assistive technology and a
  `role="status"` element announces the load instead.
- Do not animate under reduced motion.

## Empty, first use

This is the user's first sight of a feature. It is an onboarding moment, not a
gap.

```
No bookings yet
Bookings appear here once a guest reserves a room.
[ Create a booking ]
```

Four parts: what this is, why it is empty, what to do, and the action itself.

Never ship a bare "No data" or an illustration with "Nothing here!" as the
whole message.

## Empty, no results

Different state, different copy. The feature works. The filter is too narrow.

```
No results for "oakwood"
No properties match this search in March.
[ Clear filters ]  [ Search all dates ]
```

Name what was searched. Offer the way out. Never make the user guess which
filter caused it.

## Errors

Three parts, always: what happened, why, what to do next.

| Type | Behaviour |
|---|---|
| Recoverable | Keep the surrounding UI, offer retry, preserve input |
| Fatal | Explain plainly, offer a route out, state what was saved |
| Field level | Beside the field, linked with `aria-describedby` |
| Page level | `role="alert"`, focus moved to it |

Never show a raw status code as the whole message. A reference code may follow
a plain explanation.

Always say what was preserved. "Your draft is saved" removes most of the panic.

## Partial data

When one source of several fails, render what you have and mark the gap
honestly.

```
Revenue and bookings loaded. Occupancy is unavailable.
[ Retry occupancy ]
```

Never silently render a chart with a missing series as though it were complete.
Never interpolate across missing data, which invents readings that were never
taken.

## Offline

- State the status plainly.
- Say what still works.
- Queue actions where you can, and say they are queued.
- Recover automatically and confirm when back.

Do not block the whole interface because one request failed.

## Success

The end of a flow is half of what the user remembers.

```
Table booked for 4 on Friday 6 March at 7:30pm.
A confirmation is on its way to name@example.com.
You can change this booking until 24 hours before.
```

Say what happened, what happens next, and how to change it. Never just
"Success".

For small actions, a toast is enough. For a flow's ending, the confirmation
deserves the screen.

## Long content

Test with the worst realistic content, not the tidiest:

- A 120 character name.
- A number in the millions with a currency symbol.
- An email address with no break opportunity.
- Forty items where you designed for five.
- A single item where you designed for a grid.

```css
.title {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.identifier {
  overflow-wrap: anywhere;
}
```

Never truncate a price, a date, or anything the user needs in full.

## Permission denied

Say who can grant access and how to ask. "Access denied" with no route forward
is a dead end.

```
You do not have access to billing.
An account owner can grant it in Settings, People.
[ Request access ]
```

## Implementation checklist

For each data view, confirm by actually rendering each one:

1. Default renders.
2. Loading skeleton matches final dimensions.
3. Empty first use explains and offers the action.
4. Empty filtered names the query and clears.
5. Recoverable error retries and preserves input.
6. Fatal error explains and offers an exit.
7. Partial data marks the gap.
8. Offline handled, if applicable.
9. Success states what is next.
10. Long content does not break the layout.
11. Permission denied names a route, if applicable.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Only the happy path built | The product fails on first contact with reality | Build every state |
| Full page spinner | No sense of what is coming | Skeleton at real dimensions |
| Skeleton at the wrong height | Causes the shift it prevents | Match dimensions |
| One empty state for both cases | First use and no results need different copy | Two states |
| "Something went wrong" alone | Nothing to act on | What, why, what next |
| Raw status code to the user | Meaningless and alarming | Plain language, code after |
| Losing input on error | Punishes the user for a server fault | Preserve everything |
| Silent partial data | User trusts an incomplete chart | Mark the gap |
| "Access denied" with no route | Dead end | Name who can grant it |
| Testing only with tidy data | Real content breaks it | Test the worst case |
