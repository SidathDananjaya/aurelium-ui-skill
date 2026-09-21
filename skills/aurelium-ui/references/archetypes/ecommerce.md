# E-commerce

The product is the content. Everything the interface does should get out of its
way or help the customer judge it.

## User goals

Find something suitable, believe it is right, and buy it without anxiety. Most
abandonment is not about price. It is about doubt.

## Primary tasks

| Task | Served by |
|---|---|
| Find | Search, category navigation, filters |
| Judge | Imagery, specification, reviews, returns policy |
| Decide | Price, availability, delivery date |
| Buy | Cart and checkout |
| Feel safe | Confirmation, tracking, a visible way to reverse |

## Information architecture

1. **Listing.** Category or search results with filters.
2. **Product detail.** The decision screen.
3. **Cart.** Review and adjust.
4. **Checkout.** Details, delivery, payment.
5. **Confirmation.** What was bought and what happens next.
6. **Account.** Orders, returns, addresses.

## Key screens

- Listing.
- Product detail.
- Cart.
- Checkout.
- Confirmation.

## Product detail

The screen where the sale is made or lost.

- **Imagery first.** Multiple angles, consistent crop and background, zoom,
  and scale where size is ambiguous. See `../components/media.md`.
- Price visible without scrolling, with tax status stated.
- Availability stated plainly, with the delivery date rather than a lead time.
  "Arrives Thursday 12 March" beats "Ships in 2 to 3 days".
- Variants change the image and the price, and update the URL.
- Out-of-stock variants are visible but marked, not hidden, so the customer
  knows the option exists.
- Specification as a table, not prose.
- Returns policy near the buy action, not only in the footer.

**Check.** Cover everything but the first viewport. Can the customer tell what
it is, what it costs, and when it arrives?

## Listing

- One aspect ratio across every card. Mixed ratios break the grid.
- Show price, and the price after discount with the original struck through.
- Filters are visible and removable. See `../patterns/search-filter.md`.
- Result count always stated.
- Sort options named plainly, with the default stated.
- Never lazy-load so aggressively that the customer cannot reach the footer.

## Cart

- Always reachable, with a count.
- Editable in place: quantity, variant, remove.
- Removing offers undo rather than confirmation.
- Show the subtotal, and be explicit about what is not yet included.
- Never surprise at checkout. Estimate delivery and tax in the cart.

## Checkout

Unexpected cost at the final step is the single largest cause of abandonment.
Everything here is about removing doubt.

- Guest checkout, always. Never force account creation before purchase.
- One column, clear steps, progress visible.
- Show the order summary throughout.
- Every cost itemised before the payment step: item, delivery, tax, discount.
- Address autocomplete, with manual entry always available.
- Payment fields follow `../components/forms.md`: correct `inputmode`,
  correct `autocomplete`, accept spaces in card numbers.
- Never block paste.
- Errors preserve every entered value.
- The final button states the amount: "Pay 84.00".

## Critical states

| State | Requirement |
|---|---|
| Out of stock | Stated on listing and detail, with a notify option |
| Low stock | Only when true. Never manufactured |
| Price changed in cart | Say so before payment, never silently |
| Item removed while in cart | Explain, offer an alternative |
| Payment declined | Explain, preserve the cart, offer another method |
| Delivery unavailable to address | Say so before the payment step |
| Empty cart | Route back to something useful |
| Order confirmed | Full detail, what happens next |

## Luxury moments

**Product detail imagery.** The closest thing to handling the object. Consistent,
generous, zoomable photography does more for perceived quality than any other
single element.

**The order confirmation.** The peak-end rule in its clearest form. The customer
has just parted with money and is at their most anxious. Confirm exactly what
they bought, what it cost, when it arrives, where it is going, and how to change
or return it. This page is cheap to build well and almost always neglected.

**The unboxing of information.** Order tracking that proactively tells the
customer where their parcel is, rather than making them ask.

## Pitfalls

| Pitfall | Why it fails | Instead |
|---|---|---|
| Costs revealed at the final step | The largest cause of abandonment | Itemise in the cart |
| Forced account creation | Loses the sale outright | Guest checkout |
| Inconsistent product photography | Undermines perceived quality | One convention |
| "Ships in 2 to 3 days" | Customer wants a date | Give the date |
| Hidden out-of-stock variants | Customer cannot tell the option exists | Show, marked |
| Fake urgency and fake scarcity | Cheapens the brand, erodes trust | Only true information |
| Blocking paste in card fields | Breaks password managers | Allow paste |
| Clearing the form on a declined card | Punishes the customer for the bank | Preserve everything |
| Confirmation reading "Thank you" | Wastes the peak moment | Full detail and next steps |
| Returns policy only in the footer | Doubt at the decision point | Near the buy action |

## Recommended directions and dials

| Sector | Direction | Opulence | Density | Motion |
|---|---|---|---|---|
| Fashion, jewellery, beauty | Quiet Luxury | 6 | 3 | 4 |
| Homeware, food, craft | Tactile Craft | 5 | 4 | 5 |
| Electronics, tools | Swiss Precision | 3 | 6 | 3 |
| Watches, automotive, audio | Obsidian | 6 | 4 | 4 |

Checkout always runs lower opulence and lower motion than the rest of the store.
At the moment of payment, the customer wants clarity, not personality.

## Related references

`../components/media.md`, `../components/cards-lists.md`,
`../components/forms.md`, `../patterns/search-filter.md`,
`../patterns/states.md`, `../foundations/imagery.md`.
