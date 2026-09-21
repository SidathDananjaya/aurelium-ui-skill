# Fintech and banking

Money makes people careful. Every design decision here is judged against one
question: does this make the user more or less certain?

## User goals

Know the balance, understand where money went, move money safely, and be
confident nothing is wrong.

## Primary tasks

| Task | Served by |
|---|---|
| Check the balance | Above the fold, unambiguous |
| Understand recent activity | Transaction list with real merchant names |
| Move money | Transfer, with a review step |
| Find a specific transaction | Search and filter |
| Resolve a problem | A visible route to dispute or support |

## Information architecture

1. **Overview.** Balances and recent activity.
2. **Account detail.** Full transaction history.
3. **Transfer.** Send, with review and confirmation.
4. **Cards.** Manage, freeze, limits.
5. **Settings.** Security, notifications, statements.

## Key screens

- Overview with balances and recent activity.
- Account detail and full transaction history.
- Transfer: enter, review, confirm.
- Card management.
- Transaction detail, with a route to dispute.

## The balance

- Unambiguous and above the fold.
- Say which balance it is. Available and current differ, and conflating them
  causes overdrafts.
- Currency always stated, never assumed.
- Tabular lining figures, always.
- If it is masked by default for privacy, reveal on an explicit action and say
  the masking is deliberate.

```html
<p class="balance">
  <span class="balance-label">Available balance</span>
  <span class="balance-value">12,480.00</span>
  <span class="balance-currency">GBP</span>
</p>
```

A number without a label and a currency is not a balance. It is a number.

## Transactions

- Merchant name as the customer recognises it, not the acquirer string.
- Date, amount, and running balance where useful.
- Pending clearly distinguished from settled.
- Amounts right-aligned with tabular figures, negative values unmistakable by
  more than colour.
- Category and search that work on the names people remember.
- Never collapse several real transactions into one summary row without saying
  so.

Pending versus settled is the distinction users most often misread. Mark it in
text, not by opacity.

## Transfers

The highest-stakes flow in the product.

1. **Enter.** Recipient, amount, reference.
2. **Review.** Everything restated, with the fee and the arrival time.
3. **Authenticate.** Where required.
4. **Confirm.** What happened and what comes next.

Rules:

- The review step is never skipped, even for repeat recipients.
- Show the fee and the exchange rate before commitment, never after.
- State when the money will arrive, as a date and time where possible.
- Name the recipient in the confirmation, not just the account number.
- For a first-time recipient, say so and slow the flow down deliberately.
- Never pre-fill an amount.

## Critical states

| State | Requirement |
|---|---|
| Insufficient funds | Say the shortfall, before submission where possible |
| Payment pending | Say what pending means here and when it clears |
| Payment failed | Explain plainly, confirm no money moved, preserve details |
| Payment delayed | Proactive, with a revised expectation |
| Account frozen or restricted | Explain what the user can still do and who to contact |
| Data unavailable | Never show a stale balance as current. Say it is unavailable |
| Session expiring | Warn before, never mid-transfer |
| Card frozen | State clearly what still works, such as direct debits |

**Never show a stale balance without a timestamp.** A wrong balance is worse
than no balance, because the user will act on it.

## Trust and security

Trust here is built by clarity, not by security iconography.

- Say when data was last updated.
- Explain what an action does before it is taken, especially freezing a card.
- Make the reversible things obviously reversible, and the irreversible things
  obviously irreversible.
- Never use a padlock icon as a substitute for actually explaining security.
- Never ask for credentials in an unexpected context. It trains users to be
  phishable.
- Log out on inactivity, but warn first and never mid-flow.

## Luxury moments

**The transfer confirmation.** The user has just moved money and wants
certainty. Name the recipient, the amount, the fee, the arrival time, and the
reference. Give a route to cancel if cancellation is possible.

**The balance on first load.** Fast, accurate, and unambiguous. This is the
screen opened most often in the product's life.

**The resolved problem.** A dispute flow that keeps the user informed without
being asked does more for loyalty than any visual treatment.

## Accessibility and precision

- Tabular figures on every monetary value, without exception.
- Never rely on red and green alone for credit and debit. Use a sign, a word,
  or a glyph.
- Currency codes rather than ambiguous symbols in multi-currency contexts.
- Round consistently, and never round in a way that changes a total.
- Screen reader output for an amount must be unambiguous: "minus 42 pounds 50",
  not "dash 42.50".

## Pitfalls

| Pitfall | Why it fails | Instead |
|---|---|---|
| Unlabelled balance | Available and current are different | Label it |
| Currency assumed | Ambiguous, and wrong for travellers | Always state it |
| Acquirer strings as merchant names | Unrecognisable, generates disputes | Clean names |
| Pending shown like settled | Users spend money they do not have | Mark in text |
| Skipping the review step | One typo sends money to a stranger | Never skip |
| Fees revealed after commitment | Destroys trust immediately | Show before |
| Stale balance with no timestamp | The user acts on a wrong figure | Timestamp or withhold |
| Colour alone for debit and credit | Excludes many users | Sign and word |
| Session expiring mid-transfer | Terrifying and infuriating | Warn beforehand |
| Padlock icons as trust theatre | Signals nothing, protects nothing | Explain plainly |

## Recommended directions and dials

| Product | Direction | Opulence | Density | Motion |
|---|---|---|---|---|
| Private banking, wealth | Obsidian | 5 | 4 | 2 |
| Consumer banking | Tactile Craft | 4 | 5 | 3 |
| Business banking, treasury | Swiss Precision | 2 | 7 | 2 |
| Crypto, trading infrastructure | Functional Futurism | 4 | 7 | 3 |

Motion stays low everywhere in fintech. Animation during a money movement reads
as instability. The transfer flow should feel deliberate, not fluid.

## Related references

`../components/data-display.md`, `../components/tables.md`,
`../components/forms.md`, `../patterns/states.md`,
`../patterns/feedback.md`, `../foundations/typography.md`.
