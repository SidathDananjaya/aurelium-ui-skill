# Onboarding

Onboarding is not a tour. It is the shortest path to the moment the product
first proves useful.

## The principle

Identify the single moment where the user first gets value, then remove
everything between them and it.

| Product | First value |
|---|---|
| Booking | Seeing real availability for their dates |
| Analytics | Seeing their own data in a chart |
| Note taking | Having written something and it saved |
| Fintech | Seeing a real balance |
| Team tool | Having a colleague in the workspace |

Every step that does not serve that moment is a candidate for deletion, or for
moving to after it.

## Ask later

Most products ask for too much too early.

| Ask at signup | Ask later |
|---|---|
| What is needed to create the account | Company size, role, team name |
| What is needed for the first task | Billing, before the trial ends |
| Nothing else | Avatar, preferences, integrations |

Every field at signup costs completions. If you cannot say what a field
changes about the next screen, it does not belong there.

Prefer inferring over asking. Timezone, locale, and currency are usually
detectable, offered as a correctable default rather than a question.

## Progressive disclosure

Teach at the moment of use, not in advance. A feature explained three screens
before it is needed has been forgotten by the time it matters.

| Instead of | Do |
|---|---|
| A five-slide tour at first launch | Explain each feature when first reached |
| A modal listing everything | An empty state that explains one thing |
| A checklist of twenty tasks | Three tasks that lead to first value |

A tour is a sign that the interface needs the explanation. Where you can, fix
the interface instead.

## Empty states are onboarding

The best onboarding is often no onboarding: an empty state that explains the
feature and offers the action. It appears exactly when relevant, costs nothing
to dismiss, and does not block.

See `states.md` for the first-use empty state structure.

## Multi-step flows

When steps are genuinely needed:

- Show position and total: "Step 2 of 4", with steps named rather than
  numbered where possible.
- Every step is reversible, and going back preserves everything entered.
- Validate per step, not all at the end.
- Allow skipping anything not strictly required, and make skipping visible
  rather than hidden.
- Save progress. A user who closes the tab returns where they left off.

```html
<nav aria-label="Progress">
  <ol class="steps">
    <li class="step" data-state="done"><span class="visually-hidden">Completed: </span>Account</li>
    <li class="step" data-state="current" aria-current="step">Property</li>
    <li class="step" data-state="todo">Availability</li>
  </ol>
</nav>
```

```css
.steps {
  display: flex;
  gap: var(--space-5);
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: var(--text-xs);
}

.step {
  color: var(--color-text-muted);
  padding-block-end: var(--space-2);
  border-block-end: 2px solid var(--color-border);
}

/* Weight and rule carry the state, not colour alone */
.step[data-state="current"] {
  color: var(--color-text);
  font-weight: 600;
  border-block-end-color: var(--color-accent);
}

.step[data-state="done"] { color: var(--color-text); }
```

The hidden "Completed:" text means a screen reader conveys the same state the
border conveys visually.

## Checklists

A setup checklist works when it is short and each item leads somewhere useful.

- Three to five items, never twenty.
- Each item states the benefit, not the task: "Add your first property so
  guests can book" rather than "Create property".
- Show progress honestly.
- Allow dismissal, permanently, and do not bring it back.
- Never block the product behind completing it.

## Sample data

For a product that is useless while empty, offer sample data, clearly marked
and trivially removable.

Mark it unmistakably. A user who mistakes sample data for real data and acts on
it has been actively harmed by the onboarding.

## Permissions and personal data

Ask at the moment the permission is needed, with the reason attached.

| Bad | Good |
|---|---|
| Requesting notifications on first launch | Requesting when the user enables an alert, explaining what it sends |
| Requesting location at signup | Requesting when they tap "Near me" |

A permission prompt with no context gets denied, and the denial is usually
permanent.

## Returning users

Onboarding is not only for the first session.

- A user returning after a long absence may need a short re-orientation, not
  the full flow again.
- A new feature announces itself once, in context, and never again after
  dismissal.
- Never show the first-run experience twice. It reads as the product having
  forgotten them.

## Measuring

The metric is time to first value, not tour completion. A tour with 90 percent
completion and a product with 20 percent activation is a tour that is working
and an onboarding that is not.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Five-slide tour at first launch | Forgotten before it is needed | Teach at point of use |
| Asking everything at signup | Every field costs completions | Ask later |
| Blocking the product behind setup | User never reaches the value | Let them in, guide inside |
| Twenty-item checklist | Reads as work, not welcome | Three to five |
| Permission prompt with no reason | Denied, usually permanently | Ask in context |
| Unmarked sample data | User acts on fiction | Mark and make removable |
| Non-dismissible onboarding | Feels like a trap | Always dismissible |
| Losing progress on refresh | Restarting is where users quit | Save each step |
| Re-showing first-run to returning users | The product forgot them | Track completion |
| Measuring tour completion | Optimises the wrong thing | Measure time to first value |
