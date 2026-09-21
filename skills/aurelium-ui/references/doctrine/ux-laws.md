# UX laws and how Aurelium applies them

Each entry gives the law in one sentence, the rule you follow, a concrete
example, and the anti-example that shows the failure. Apply the rule. Do not
cite the law in the interface copy.

## Visual hierarchy

**Law.** Viewers read a composition in the order its visual weight dictates, not
the order of the markup.

**Rule.** Establish hierarchy with size first, then weight, then color, then
position. Each screen reads in a deliberate order: headline, then key figure or
action, then supporting content.

**Example.** A dashboard card shows the metric at 40px semibold, its label at
13px medium in muted text, and its change indicator at 13px beside the label.

**Anti-example.** A card where the label, value, and change are all 16px
regular, distinguished only by color.

## Gestalt: proximity

**Law.** Elements placed close together are perceived as related.

**Rule.** Inner spacing is always smaller than outer spacing. The gap inside a
group must be less than the gap separating it from the next group. No exceptions.

**Example.** A form field with 8px between label and input, and 24px between one
field and the next.

**Anti-example.** 16px between label and input and 16px between fields, so the
labels appear to belong to the field above.

## Gestalt: similarity and common region

**Law.** Elements that share appearance, or share an enclosing boundary, are
perceived as belonging to the same set.

**Rule.** The same function looks the same everywhere. Group with space first.
If space is not enough, use a subtle surface. Use a border last.

**Example.** Every destructive action in the product uses one identical style.

**Anti-example.** Delete is a red text link in the table, a red filled button in
the drawer, and a grey icon in the header.

## Fitts's law

**Law.** The time to reach a target depends on its distance and its size.

**Rule.** Primary actions are large and near the user's current focus. Every
interactive target is at least 24 by 24 CSS pixels. Primary and touch targets
aim for 44 by 44.

**Example.** A table row's action menu sits at the row's end, with a 44px hit
area extended by padding beyond the 16px icon.

**Anti-example.** A 12px close icon in a dialog corner, 600px from where the
user was reading.

## Hick's law

**Law.** Decision time grows with the number and complexity of choices.

**Rule.** Limit the choices presented at one decision point. Move advanced
options behind progressive disclosure. If a menu exceeds about seven items,
group it.

**Example.** A pricing page shows three plans, with a comparison table below for
those who want detail.

**Anti-example.** A settings page presenting 40 toggles in one flat list.

## Jakob's law

**Law.** People spend most of their time on other products, so they expect yours
to work the same way.

**Rule.** Use familiar conventions for navigation, forms, carts, search, and
settings. Innovate in aesthetics and in detail quality, never in the basic
mechanics of a known interaction.

**Example.** The cart icon sits top right, shows a count badge, and opens a
drawer summarising the order.

**Anti-example.** A horizontal scrolling checkout that replaces the standard
step sequence because it looks distinctive.

## Miller's law and chunking

**Law.** Working memory holds a small number of items at once.

**Rule.** Chunk information into scannable groups. Never require the user to
carry a value from one screen to the next in their head.

**Example.** A 16 digit card number rendered in four groups of four, and the
order total repeated on the confirmation step.

**Anti-example.** A confirmation screen that shows an order ID the user must
remember to use on the support page.

## Doherty threshold

**Law.** Interaction stays engaging when the system responds within about 400ms.

**Rule.** Acknowledge every user action within 400ms, even if the work is not
finished. Use optimistic updates for reversible actions and skeletons for waits
beyond 400ms.

**Example.** A favourite toggle flips instantly and reconciles with the server
afterwards, reverting with a message if the call fails.

**Anti-example.** A save button that appears inert for two seconds, prompting a
second click.

## Aesthetic usability effect

**Law.** People perceive attractive interfaces as easier to use, and forgive
their minor flaws.

**Rule.** Treat this as a reason to invest in craft, never as licence to trade
usability for beauty. If a beautiful treatment reduces clarity, the treatment
changes.

**Example.** A refined, high-contrast focus ring that suits the brand.

**Anti-example.** Body text at 40 percent opacity because it looks more elegant.

## Peak end rule

**Law.** People judge an experience by its most intense moment and by its
ending, not by the average.

**Rule.** Identify the peak and the ending of each flow, then invest
disproportionately there. Every archetype file names its luxury moments.

**Example.** A booking confirmation that states what happens next, when, and how
to change it, with the detail well set rather than dumped in a list.

**Anti-example.** A checkout with a polished payment form that ends on an
unstyled "Thank you for your order" page.

## Tesler's law, or conservation of complexity

**Law.** Every process has irreducible complexity. The only question is who
absorbs it.

**Rule.** The system absorbs it. Smart defaults, autofill, inferred formatting,
and forgiving input parsing are the product's job, not the user's.

**Example.** A phone field that accepts spaces, dashes, and brackets, then
normalises on submit.

**Anti-example.** A field that rejects input and tells the user to remove spaces.

## Von Restorff effect, or isolation effect

**Law.** The item that differs from its neighbours is the one remembered.

**Rule.** Exactly one element per screen is visually distinct: the primary
action, or the key insight. Distinctiveness spent on two things is spent on
neither.

**Example.** One accent-filled button in a view of neutral surfaces.

**Anti-example.** Accent color on the button, the active nav item, three badges,
and a promotional banner.

## Serial position effect

**Law.** Items at the start and end of a sequence are recalled best.

**Rule.** Place the most important navigation items first and last. Put
destructive or rarely used items in the middle, or behind a menu.

**Example.** A sidebar that opens with Overview and closes with Settings.

**Anti-example.** Sign out placed first, above the primary destinations.

## Postel's law, applied to input

**Law.** Be liberal in what you accept and conservative in what you produce.

**Rule.** Accept any reasonable spelling of a value. Display it in one canonical
format. Never make the user match an undisclosed pattern.

**Example.** A date field accepting `2026-03-04`, `4 Mar 2026`, and `04/03/2026`,
then displaying the canonical form and stating the interpretation.

**Anti-example.** A field that silently fails unless the input is `DD/MM/YYYY`.

## Resolving conflicts

Jakob's law and originality collide often. Convention wins on mechanics.
Originality belongs in typography, color, spacing, motion quality, and detail.

Hick's law and discoverability collide often. Reduce the visible choices, but
never hide the primary path. Progressive disclosure applies to advanced options,
not to the main task.
