# The ten usability heuristics, made checkable

Jakob Nielsen's ten heuristics, each reduced to one rule you implement and one
check you can run. The check is binary. If you cannot answer yes, the interface
is not finished.

See `CREDITS.md` for attribution.

## 1. Visibility of system status

**Rule.** Every asynchronous action shows a pending state, then either a success
or an error state. The user never wonders whether something is happening.

**Check.** Trigger every async action with the network throttled. Each one
acknowledges within 400ms and resolves visibly. No action resolves silently.

## 2. Match between the system and the real world

**Rule.** Use the words your users use. No internal jargon, no database field
names, no HTTP status codes in user-facing copy.

**Check.** Read every string aloud. Flag any term that exists only because of
the implementation, such as "entity", "payload", "null", "400", or "sync job".

## 3. User control and freedom

**Rule.** Every destructive or significant action is reversible. Prefer undo
over a confirmation dialog. `Esc` closes any overlay. Every multi-step flow has
a visible way back that preserves entered data.

**Check.** Perform each destructive action, then attempt to reverse it. Open
each overlay and press `Esc`. Move back a step in each flow and confirm the
previously entered values are still there.

## 4. Consistency and standards

**Rule.** The same concept uses the same word, the same icon, and the same
component everywhere. Platform conventions win over internal invention.

**Check.** List every button label in the product. Any two labels meaning the
same thing must be identical. "Delete" and "Remove" do not coexist for one
action.

## 5. Error prevention

**Rule.** Make invalid states unreachable before validating them. Disable what
cannot apply, constrain formats at the input, and confirm only genuinely
irreversible actions.

**Check.** Attempt to submit each form with plausible bad input. Count the
errors that could have been prevented by a better control, such as a date picker
instead of free text. The count is zero.

## 6. Recognition rather than recall

**Rule.** Keep the information needed for the current decision visible. Never
require the user to remember a value from a previous screen.

**Check.** For each step of each flow, cover the previous screen. Every value
needed to proceed is still on screen.

## 7. Flexibility and efficiency of use

**Rule.** Serve the first-time user by default and the repeat user with
accelerators: keyboard shortcuts, bulk actions, saved views, sensible defaults
that remember the last choice.

**Check.** Complete the primary task using only the keyboard. Confirm at least
one accelerator exists for the most repeated task in the product.

## 8. Aesthetic and minimalist design

**Rule.** Every element on a screen competes with every other element for
attention. Remove anything that does not serve the current task.

**Check.** For each element, state what task it serves. Anything without an
answer is removed, not shrunk or faded.

## 9. Help users recognise, diagnose, and recover from errors

**Rule.** Every error message states what happened, why, and what to do next, in
plain language. Errors are linked to the field that caused them.

**Check.** Read every error string. Each contains a cause and an action. No
string reads only "Something went wrong" or shows a raw error code without
explanation. Form errors move focus to the offending field.

## 10. Help and documentation

**Rule.** Put guidance where the difficulty is, not in a separate manual.
Inline hints, examples in placeholders, and contextual explanations beat a help
centre link.

**Check.** For each field or control a new user could misread, confirm the
explanation is adjacent to it, not one click away.

## Using these in an audit

Score each heuristic pass or fail, then record the failures as findings under
these severity levels:

- A failure that blocks the task or excludes a user is **Critical**.
- A failure that measurably slows or confuses is **Important**.
- A failure that only costs refinement is **Polish**.

Report the check you ran, not just the verdict. "Pressed Esc in the filter
drawer, nothing happened" is actionable. "Poor user control" is not.
