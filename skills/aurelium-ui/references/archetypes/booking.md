# Booking and reservation

Booking is committing to a time. The anxiety is about availability and about
whether the commitment can be changed.

## User goals

Find a slot that works, believe it is really available, book it, and know how
to change it.

## Primary tasks

| Task | Served by |
|---|---|
| See what is available | A calendar or slot view, honestly rendered |
| Narrow to what suits | Date, party size, duration, type |
| Commit | Details and payment |
| Be certain | Confirmation with everything restated |
| Change or cancel | A visible, easy route |

## Information architecture

1. **Search.** Dates, party size, location.
2. **Availability.** What is free, with price where it varies.
3. **Selection.** The specific slot or room.
4. **Details.** Who, and any requirements.
5. **Payment.** Where taken.
6. **Confirmation.** Everything restated.
7. **Manage.** View, change, cancel.

## Key screens

- Availability.
- Selection detail.
- Details and payment.
- Confirmation.
- Manage booking.

## Availability

The screen the whole product turns on. It must be honest and legible.

- Show what is available **and** what is not. An empty calendar with no
  explanation reads as broken.
- Unavailable slots are visible but clearly marked, never silently omitted.
- Say why where you can: "Fully booked", "Closed Mondays", "Minimum 2 nights".
- Show price on the slot where price varies by date.
- Default to the nearest sensible date, never to today if today is impossible.
- Timezone stated wherever the booking is remote.

```
Mon 2   Tue 3   Wed 4   Thu 5   Fri 6
 --     18:00   18:00   18:00   19:30
        20:15   20:15    --     21:00
```

A dash with a legend beats a missing cell. The customer needs to know the day
exists and is full.

## Selecting a date range

- Two taps or clicks: start then end. Never two separate pickers to coordinate.
- Show the nights or days count as it is selected.
- Minimum and maximum stay stated before the user hits them, not after.
- Blocked dates within a range are visible before selection.
- Changing the start does not silently discard the end.

## Critical states

| State | Requirement |
|---|---|
| No availability for the query | Say so, offer nearest alternatives |
| Partially available | Show what is possible, name the constraint |
| Slot taken during checkout | Explain immediately, offer alternatives, preserve details |
| Held, expiring | Show the remaining time, warn before expiry |
| Payment failed | Preserve the hold if possible, preserve all details |
| Confirmed | Everything restated |
| Cancelled | Confirm, state any refund and its timing |
| Waitlist | If offered, state the position or likelihood honestly |

**The slot taken during checkout is the defining state of this archetype.** It
will happen. Handle it explicitly: explain, offer the nearest alternatives, and
never lose what the user typed.

## Holds

If a slot is held while the user completes details:

- Say it is held and for how long.
- Show the countdown, without inducing panic.
- Warn before expiry, with a way to extend.
- On expiry, explain and offer to re-check rather than silently failing.

## Confirmation

The peak-end moment. The user has committed money and time and wants certainty.

```
Table for 4, Friday 6 March, 7:30pm
The Harbour Room, 12 Marine Parade

A confirmation is on its way to name@example.com
You can change or cancel this booking until 7:30pm on Thursday 5 March.

[ Add to calendar ]  [ Change booking ]
```

- Restate everything: what, when, where, how many, how much.
- State the change and cancellation deadline as a date and time, never as
  "24 hours before".
- Offer add-to-calendar. It is trivial and removes a real task.
- Give the reference in a copyable form.
- Say what to do on arrival if there is anything to know.

## Change and cancel

Hiding cancellation does not reduce cancellations. It produces support tickets
and distrust.

- One clear route from the confirmation and from the account.
- State the policy before the user commits, not only after.
- Confirm cancellation with what will be refunded and when.

## Luxury moments

**Slot selection.** The moment of choosing. Generous targets, clear pricing,
honest availability. This is where a booking product feels considered or cheap.

**The confirmation.** Complete, calm, and specific. A confirmation that answers
every question the guest was about to ask is the cheapest luxury in the product.

**The reminder.** A well-timed, useful reminder that includes directions and
the change link, rather than a bare "See you tomorrow".

## Pitfalls

| Pitfall | Why it fails | Instead |
|---|---|---|
| Hiding unavailable slots | Reads as broken or empty | Show, marked, with a reason |
| No explanation for unavailability | User cannot adjust their query | Say why |
| Losing details when a slot is taken | Punishes the user for a race | Preserve everything |
| "Cancel up to 24 hours before" | Requires mental arithmetic | Give the date and time |
| Hidden cancellation policy | Distrust, then support tickets | State before commitment |
| Two separate date pickers | Coordinating them is fiddly | One range picker |
| No timezone on remote bookings | Wrong bookings, guaranteed | State it |
| Countdown with no warning | Session expires mid-typing | Warn and offer to extend |
| Confirmation without a deadline | The first thing they will ask | State it |
| Defaulting to an impossible date | Immediate dead end | Default to the nearest possible |

## Recommended directions and dials

| Sector | Direction | Opulence | Density | Motion |
|---|---|---|---|---|
| Hotels, spas, fine dining | Quiet Luxury | 6 | 3 | 4 |
| Restaurants, activities, casual | Tactile Craft | 5 | 4 | 5 |
| Clinics, professional services | Swiss Precision | 3 | 5 | 3 |
| Premium travel, private hire | Obsidian | 5 | 4 | 3 |

Availability screens run denser than the rest of the flow, because the user is
comparing. The confirmation runs the lowest density in the product.

## Related references

`../components/forms.md`, `../components/overlays.md`,
`../patterns/states.md`, `../patterns/feedback.md`,
`../foundations/microcopy.md`.
