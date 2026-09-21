# Forms

A form is a conversation. Ask only what you need, ask it clearly, and never
punish the user for formatting.

## Anatomy

| Part | Rule |
|---|---|
| Label | Always visible, above the input, a noun |
| Input | At least 44px tall, 16px text minimum on mobile |
| Help text | Below the label, before the user types |
| Error | Below the input, linked with `aria-describedby` |
| Required marker | In text, not colour or an asterisk alone |

Label to input gap is `--space-2`. Field to field is `--space-5`. Inner spacing
smaller than outer, always.

## Labels

A placeholder is not a label. It disappears the moment typing starts, fails
contrast in most implementations, and leaves the user unable to check what they
were asked.

```html
<div class="field">
  <label for="email">Email address</label>
  <input
    id="email"
    name="email"
    type="email"
    autocomplete="email"
    aria-describedby="email-hint"
  />
  <p class="hint" id="email-hint">We send your booking confirmation here.</p>
</div>
```

```css
.field {
  display: grid;
  gap: var(--space-2);
}

.field + .field { margin-block-start: var(--space-5); }

.field label {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--color-text);
}

.field input,
.field select,
.field textarea {
  min-block-size: 44px;
  padding: var(--space-3) var(--space-4);
  font: inherit;
  color: var(--color-text);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.field input:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

.hint {
  margin: 0;
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.error {
  margin: 0;
  font-size: var(--text-xs);
  color: var(--color-danger);
  display: flex;
  gap: var(--space-2);
}

.field[data-invalid="true"] input { border-color: var(--color-danger); }
```

The error uses colour **and** an icon or the word, never colour alone.

## Validation timing

| Moment | Behaviour |
|---|---|
| While typing, first attempt | Say nothing. Interrupting mid-entry is hostile |
| On blur, if touched and invalid | Show the error |
| While typing, after an error is shown | Revalidate live, so the user sees it clear |
| On submit | Validate everything, focus the first invalid field |

Never validate an empty field the user has not reached yet.

## Errors

Every message states what is wrong and how to fix it.

| Bad | Good |
|---|---|
| Invalid input | Enter a date in the future |
| Error | Use at least 12 characters, including a number |
| Field required | Enter your full name as it appears on your card |

On submit, move focus to the first invalid field and announce a summary:

```html
<div role="alert" class="error-summary">
  <h2>2 fields need attention</h2>
  <ul>
    <li><a href="#email">Email address: add the part after the @</a></li>
    <li><a href="#card">Card number: check the last 4 digits</a></li>
  </ul>
</div>
```

The summary links to the fields. A list of problems the user cannot jump to is
a worse experience than no summary.

## Input types and autocomplete

Use the right type so mobile keyboards and password managers behave.

| Data | Type | Autocomplete |
|---|---|---|
| Email | `email` | `email` |
| Phone | `tel` | `tel` |
| Name | `text` | `name`, `given-name`, `family-name` |
| Street | `text` | `street-address` |
| Postcode | `text` | `postal-code` |
| Card number | `text`, `inputmode="numeric"` | `cc-number` |
| One-time code | `text`, `inputmode="numeric"` | `one-time-code` |

Never use `type="number"` for a card, postcode, or phone. It permits scientific
notation, strips leading zeros, and adds spinners nobody wants.

## Be liberal in what you accept

The system absorbs complexity, not the user.

- Accept spaces, dashes, and brackets in phone and card numbers, then normalise.
- Accept several date spellings, display the canonical one, and state the
  interpretation.
- Trim whitespace silently.
- Accept a pasted value that includes a label, such as "Card: 4242...".

A field that rejects input and tells the user to remove spaces is a bug.

## Masks and formatting

Format as the user types only when the format aids comprehension, such as card
numbers in groups of four. Never move the caret unpredictably, and never block
paste.

## Multi-step forms

- Show progress: step 2 of 4, with the steps named.
- Every step is reversible, and going back preserves what was entered.
- Validate per step, not only at the end.
- Never lose data on navigation, refresh, or a failed submit.
- The final step summarises everything before the irreversible action.

## Groups

Related inputs use `fieldset` and `legend`. This is how a screen reader knows
that three radio buttons answer one question.

```html
<fieldset>
  <legend>Room preference</legend>
  <label><input type="radio" name="room" value="garden" /> Garden view</label>
  <label><input type="radio" name="room" value="sea" /> Sea view</label>
</fieldset>
```

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Placeholder as the label | Vanishes on focus, fails contrast | Visible label above |
| Validating while first typing | Shows errors for input not finished | Validate on blur |
| Colour-only error state | Invisible to many users | Colour plus icon and text |
| `type="number"` for card or phone | Strips zeros, adds spinners | `inputmode="numeric"` |
| Blocking paste on password or code | Breaks password managers | Allow paste |
| Rejecting spaces in a card number | The user copied it correctly | Normalise on submit |
| Asterisk alone for required | Meaning assumed, not stated | Say "Required" or mark optional |
| Losing data on back navigation | Destroys trust immediately | Preserve state |
| Clearing the whole form on one error | Punishes a small mistake | Keep every valid value |
