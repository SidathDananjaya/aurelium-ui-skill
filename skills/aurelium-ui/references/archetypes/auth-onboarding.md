# Auth and onboarding

Sign-up is the narrowest point in the product. Every field, every step, and
every moment of confusion costs users who would otherwise have stayed.

## User goals

Get in, and get to the thing they came for. Nobody wants to create an account.
They want what is behind it.

## Primary tasks

| Task | Served by |
|---|---|
| Sign up | The shortest honest form |
| Sign in | Fast, with password manager support |
| Recover access | A route that works when they have forgotten everything |
| Verify | Only where genuinely required |
| Reach first value | Onboarding that leads somewhere real |

## Information architecture

1. **Sign in.**
2. **Sign up.**
3. **Verify**, where required.
4. **Recover.**
5. **Onboarding**, as few steps as possible.
6. **First real screen.**

## Key screens

- Sign in.
- Sign up.
- Verification, where required.
- Password reset request and reset form.
- Onboarding steps.

## Sign up

- Ask for the minimum. Email and password, or a single provider button.
- Every additional field costs completions. If you cannot say what a field
  changes about the next screen, remove it.
- State the password requirements **before** the user types, not after failure.
- One password field, with a reveal toggle. Confirmation fields cause more
  errors than they prevent when a reveal exists.
- Never block paste. It breaks every password manager.
- Correct `autocomplete` on every field so managers work: `email`,
  `new-password`, `current-password`.
- Say what happens next: "We will send a code to confirm your email".

```html
<label for="password">Password</label>
<input
  id="password"
  type="password"
  autocomplete="new-password"
  aria-describedby="password-rules"
/>
<p id="password-rules">At least 12 characters. A passphrase works well.</p>
```

The rules are stated up front and linked with `aria-describedby`, so they are
announced with the field rather than discovered on failure.

## Sign in

- Email and password on one screen, or a clearly signposted two-step flow.
- "Forgot password" beside the password field, where the problem occurs.
- Never reveal whether an email exists. "If that address has an account, we
  have sent a link" is the correct response regardless.
- Preserve the email after a failed attempt. Clearing it is gratuitous.
- Remember the method used last time, and lead with it.
- Rate limit, but explain: "Too many attempts. Try again in 5 minutes."

## Verification

- Only verify where it genuinely matters. Many products verify out of habit.
- Six-digit codes with `inputmode="numeric"` and `autocomplete="one-time-code"`.
- Auto-advance between boxes, but allow paste of the whole code.
- Say where the code was sent and offer to resend, with the cooldown visible.
- Never make the user leave and lose their place. Keep the tab usable.
- Offer a route for when the code never arrives.

## Recovery

The flow used by people who are already frustrated. It deserves more care than
it usually gets.

- One obvious route from sign-in.
- Same response whether or not the account exists.
- The reset link states its expiry.
- After reset, sign the user in rather than returning them to the sign-in form.
- Offer a route for someone who has lost access to the email itself.

## Onboarding

Follow `../patterns/onboarding.md`. Specifically here:

- Identify the first moment of value and remove everything between.
- Ask contextual questions later, inside the product, where the answer changes
  something visible.
- Three steps at most before the user sees something real.
- Save progress at every step.
- Make skipping visible for anything not strictly required.

## Critical states

| State | Requirement |
|---|---|
| Email already registered | Offer sign-in, never confirm the address exists publicly |
| Invalid credentials | Generic message, preserve the email |
| Account locked | Explain why and when it unlocks |
| Verification expired | Explain, offer resend, keep them in place |
| Code not received | An alternative route |
| Password too weak | Rules shown before typing, specific feedback after |
| Provider sign-in failed | Fall back to email, preserve what was entered |
| Already signed in | Redirect, do not show the form again |
| Session expired | Explain, return to where they were after signing in |

**Returning the user to where they were after a session expiry** is the detail
that separates a considered product from a careless one.

## Luxury moments

**The first moment after sign-up.** The user has just committed. What they see
next determines whether they stay. It should be the product working, with their
data or with clearly marked sample data, not a checklist of chores.

**Sign-in speed.** For a daily product, sign-in is the most repeated flow. It
should be effortless, with password managers and passkeys fully supported.

**The recovery that works.** Someone who has lost access and gets back in
smoothly remembers it. Someone who does not, leaves.

## Security without hostility

- Support passkeys where you can. They remove the password problem entirely.
- Support password managers fully. Never block paste, never fragment fields in
  ways managers cannot read.
- Long passphrases beat forced complexity rules.
- Do not force rotation without cause.
- Two-factor should be offered clearly and explained in terms of what it
  protects.

Security theatre that makes the product harder to use without making it safer
is a cost with no benefit.

## Pitfalls

| Pitfall | Why it fails | Instead |
|---|---|---|
| Asking for company size at signup | Costs completions, changes nothing yet | Ask later |
| Blocking paste in password fields | Breaks every password manager | Allow paste |
| Password rules revealed on failure | Guaranteed frustration | State up front |
| Confirm password field | Causes more errors than it prevents | One field with reveal |
| "No account with that email" | Leaks who has an account | Same response either way |
| Clearing the form after a failure | Punishes a typo | Preserve everything |
| Verifying email before any value | Users leave to check mail and never return | Verify later where possible |
| Five-step onboarding before value | Most users never finish | Three at most |
| Session expiry losing their place | Work lost, trust lost | Return them after sign-in |
| Forced complexity rules | Produces weaker, written-down passwords | Encourage passphrases |

## Recommended directions and dials

| Product | Direction | Opulence | Density | Motion |
|---|---|---|---|---|
| Consumer app | Tactile Craft | 4 | 3 | 4 |
| B2B SaaS | Obsidian | 3 | 4 | 3 |
| Developer tool | Swiss Precision | 2 | 4 | 2 |
| Hospitality, lifestyle | Quiet Luxury | 5 | 2 | 4 |

Auth screens run low density and low opulence whatever the product. At the
moment of signing in, the user wants a clear path, not personality. Save the
character for the first real screen.

## Related references

`../components/forms.md`, `../patterns/onboarding.md`,
`../patterns/states.md`, `../patterns/feedback.md`,
`../foundations/microcopy.md`, `../doctrine/accessibility.md`.
