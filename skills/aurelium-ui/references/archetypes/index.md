# Choosing an archetype

Identify the archetype from the primary task, not from the industry. A hotel
site that takes reservations is a booking product. A hotel site that only
describes the property is a landing page.

Most real products combine two or three. Build the primary one properly and
borrow from the others.

## From what the user asked for

| The request mentions | Archetype |
|---|---|
| landing page, homepage, marketing site, product page, pricing page, waitlist, coming soon | [Marketing and landing](landing.md) |
| dashboard, overview, home screen, control panel, metrics, KPIs, team workspace | [SaaS dashboard](dashboard.md) |
| analytics, reporting, charts, insights, BI, data explorer, funnel, cohort, observability | [Analytics and data](analytics.md) |
| shop, store, product detail, cart, checkout, catalogue, marketplace, listing | [E-commerce](ecommerce.md) |
| booking, reservation, appointment, availability, calendar, scheduling, table, room, slot | [Booking and reservation](booking.md) |
| banking, wallet, payments, transfer, balance, transactions, cards, invoicing, trading | [Fintech and banking](fintech.md) |
| admin, back office, internal tool, CRUD, records, user management, moderation, bulk edit | [Admin and data tables](admin.md) |
| sign up, sign in, login, register, onboarding, verification, password reset, first run | [Auth and onboarding](auth-onboarding.md) |

## From the primary task

| The user's main job | Archetype |
|---|---|
| Be persuaded | Marketing and landing |
| Check whether things are fine | SaaS dashboard |
| Investigate why something happened | Analytics and data |
| Choose and buy an object | E-commerce |
| Commit to a time | Booking and reservation |
| Move or understand money | Fintech and banking |
| Process many records quickly | Admin and data tables |
| Get into the product | Auth and onboarding |

The distinction between dashboard and analytics is the one most often missed. A
dashboard reports status and is scanned. Analytics supports investigation and is
interrogated. Building one as the other produces something that does neither.

## Combinations

Real products are rarely one archetype.

| Product | Primary | Also borrows from |
|---|---|---|
| Hotel website with booking | Booking | Landing, for the property pages |
| SaaS with usage reporting | Dashboard | Analytics, for the explore view |
| Marketplace | E-commerce | Admin, for the seller back office |
| Banking app | Fintech | Dashboard, for the overview screen |
| Any product at all | Its own | Auth and onboarding, always |

**Every product includes auth and onboarding.** It is the one archetype nobody
requests and everybody needs.

Build the primary archetype fully. Borrow specific screens from the others
rather than blending their conventions.

## Common phrasings and where they land

| Phrase | Archetype | Note |
|---|---|---|
| "a site for my restaurant" | Landing, unless it takes bookings | Ask if reservations matter |
| "a portal for our customers" | Dashboard | Usually status plus a few actions |
| "a page to sell my course" | Landing | The purchase is a single action |
| "a tool for my team to manage orders" | Admin | Internal, so density is high |
| "an app to track my spending" | Fintech | Even without a bank behind it |
| "a page showing our availability" | Booking | Availability implies commitment |
| "a homepage with our latest numbers" | Dashboard | Not analytics unless they filter |

When the request is ambiguous between two archetypes and the choice changes the
structure, that is worth one question. Otherwise pick the more likely one, state
the assumption, and proceed.

## What every archetype shares

Whatever you are building:

- Every data view ships the complete state set in `../patterns/states.md`.
- One primary action per screen.
- Tokens only, from the chosen direction.
- WCAG 2.2 AA as the floor.
- The pre-flight in the create workflow before you call it done.

## Coverage

Eight archetypes ship today. Settings, editorial, portfolio, AI chat, messaging,
and documentation are planned. If a request does not fit one of the eight, pick
the nearest, say which one you chose and why, and apply the doctrine and
foundations directly.

## Related references

`../directions/index.md` for choosing the visual system,
`../patterns/states.md` for the states every archetype needs,
`../../workflows/create.md` for the build order.
