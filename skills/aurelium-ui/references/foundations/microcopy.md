# Microcopy

Copy is interface. The words a user reads while deciding what to do are part of
the design, not content poured in afterwards.

## Voice

Calm, confident, specific. The tone of someone who knows the answer and does not
need to perform.

| Quality | Means | Not |
|---|---|---|
| Calm | States facts without urgency theatre | "Hurry, only 2 left!" |
| Confident | No hedging, no apologising for the product | "We're sorry, but you may need to possibly try again" |
| Specific | Names the actual thing and the actual number | "Some items could not be saved" |
| Plain | The user's words, not the system's | "Your payload failed validation" |
| Brief | Every word earns its place | "In order to be able to proceed, please..." |

**Never use exclamation marks** in product copy. They read as nervous. A single
one is permitted at a genuine peak moment, such as a completed booking, and even
then a period usually reads more expensive.

**Never use em-dashes** in generated interface copy. Use periods, commas, or
colons.

Write in sentence case for every heading, label, and button. Title Case In
Product UI reads dated, and All Caps removes word shape.

## Buttons are verbs

A button label says what will happen when it is pressed, from the user's point
of view.

| Instead of | Write |
|---|---|
| Submit | Create account, Send message, Place order |
| OK | Save changes, Delete draft, Got it |
| Yes / No | Delete file / Keep file |
| Click here | The actual action |
| Continue, on a final step | Confirm and pay |

**Check.** Read each button label out of context. If you cannot tell what it
does, rewrite it.

In a confirmation dialog, both buttons name their outcome. "Are you sure?" with
"Yes" and "No" forces the user to re-read the question. "Delete 12 files" and
"Cancel" does not.

Match the label to the heading. A dialog titled "Delete project" has a button
reading "Delete project", not "Confirm".

## Errors: what happened, why, what next

Every error message has three parts. Two of them are usually missing.

```
[What happened]  We could not process your card.
[Why]            Your bank declined the payment.
[What next]      Try a different card, or contact your bank.
```

| Bad | Good |
|---|---|
| Error 500 | We could not load your bookings. Retry, or refresh the page. |
| Invalid input | Enter a date in the future. |
| Something went wrong | We could not save your changes. Your work is still here. Retry. |
| Password invalid | Use at least 12 characters, including a number. |
| Network error | You appear to be offline. We will retry when the connection returns. |

Rules:

- Never blame the user. "The email address was not recognised" beats "You
  entered an invalid email."
- Never expose a status code, stack trace, or internal identifier as the whole
  message. A reference code may follow the plain explanation.
- Say what was preserved. "Your draft is saved" removes most of the panic.
- Put the message beside the field that caused it, not only in a summary.
- Never say "please" to soften a failure the product caused.

## Empty states guide, they do not apologise

An empty state is the user's first view of a feature. It is an onboarding
opportunity, not a gap.

Four parts: what this is, why it is empty, what to do, and the action itself.

```
No invoices yet
Invoices appear here once you send your first one.
[ Create invoice ]
```

Distinguish the two empty states, because they need different copy:

| State | Copy |
|---|---|
| Empty on first use | Explain the feature and give the primary action |
| Empty after filtering | Say what was searched, and offer to clear the filter |

**Do.** "No results for 'oakwood'. Clear filters, or search all properties."
**Don't.** "No data."

Never use an illustration of an empty box with "Nothing here!" as the whole
message. It occupies space without doing work.

## Labels and help text

- Labels are nouns, short, and always visible. A placeholder is not a label.
- Help text sits below the field, before the user types, not after they fail.
- Show the requirement up front. "At least 12 characters" belongs under the
  password field from the start.
- Mark optional fields rather than required ones when most are required.
- Never put an example in a placeholder that could be mistaken for a value.

```html
<label for="vat">VAT number</label>
<input id="vat" aria-describedby="vat-hint" />
<p id="vat-hint">Optional. We add this to your invoices.</p>
```

## Numbers, dates, and units

- Format numbers for the locale, with thousands separators.
- Use tabular figures wherever numbers align. See `typography.md`.
- Give dates in an unambiguous form. "4 Mar 2026" never confuses, "04/03/2026"
  often does.
- Relative time for recency, absolute on hover or beside it: "2 hours ago" with
  the exact timestamp available.
- Always state the currency and the unit. "1,240" is not a price.
- Round to a sensible precision. "99.99998% uptime" should read "99.99%".

## Confirmation and destructive actions

Prefer undo over confirmation. A confirmation dialog interrupts everyone to
protect against a rare mistake, and users learn to dismiss it without reading.

Confirm only when the action is genuinely irreversible or expensive.

When you do confirm:

- Name the object and the count. "Delete 12 files" not "Delete items".
- Say what is lost and whether it can be recovered.
- Make the destructive button the one that describes the destruction.
- Never make the destructive action the default focus.

## Success and confirmation

The end of a flow is half of what the user remembers. Say what happened, what
happens next, and how to change it.

**Do.** "Table booked for 4 on Friday 6 March at 7:30pm. A confirmation is on
its way to name@example.com. You can change this booking until 24 hours before."
**Don't.** "Success!"

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Lorem ipsum in a deliverable | Hides real length and rhythm problems | Write plausible real copy |
| Exclamation marks | Reads nervous, undercuts confidence | A period |
| "Oops!" or "Uh oh!" | Trivialises a failure the user cares about | State what happened |
| "Something went wrong" alone | Gives the user nothing to act on | What happened, why, what next |
| Title Case Everywhere | Dated, harder to scan | Sentence case |
| "Click here" | Meaningless out of context, poor for screen readers | Name the destination or action |
| Placeholder used as the label | Disappears on focus, fails accessibility | Visible label |
| "Submit" | Names the mechanism, not the outcome | Name the outcome |
| Emoji in product copy | Wrong register, inconsistent rendering | Words |
| Fake data that looks fake | Undermines the whole design review | Realistic names, amounts, and dates |
