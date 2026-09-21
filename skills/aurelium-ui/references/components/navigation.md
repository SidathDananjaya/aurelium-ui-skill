# Navigation

Navigation answers three questions at all times: where am I, where can I go,
and how do I get back.

## Choosing a pattern

| Pattern | Use when | Avoid when |
|---|---|---|
| Top bar | Under 7 destinations, marketing or simple app | Deep hierarchy |
| Sidebar | Many destinations, app with sections | Content needs full width |
| Tabs | Views of one object, under 7 | Switching context entirely |
| Breadcrumbs | Hierarchy deeper than two levels | Flat structure |
| Command palette | Power users, many actions | The only way to reach something |

A command palette is an accelerator, never the sole path. Every action in it is
reachable another way.

## Current location

The active item is unmistakable and never signalled by colour alone.

```html
<nav aria-label="Main">
  <ul class="nav">
    <li><a href="/overview" aria-current="page">Overview</a></li>
    <li><a href="/bookings">Bookings</a></li>
    <li><a href="/settings">Settings</a></li>
  </ul>
</nav>
```

```css
.nav {
  display: flex;
  gap: var(--space-5);
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav a {
  display: block;
  padding: var(--space-3) 0;
  color: var(--color-text-muted);
  text-decoration: none;
  border-block-end: 2px solid transparent;
}

.nav a:hover { color: var(--color-text); }

/* Weight and a rule, not colour alone */
.nav a[aria-current="page"] {
  color: var(--color-text);
  font-weight: 600;
  border-block-end-color: var(--color-accent);
}

.nav a:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

`aria-current="page"` is what tells assistive technology which item is active.
Styling alone does not.

## Ordering

Serial position effect: the first and last items are remembered best.

- Most important destination first.
- Settings or account last.
- Rarely used or destructive items in the middle, or behind a menu.
- Never put sign out first.

## Sidebar

- Group destinations under short headings when there are more than seven.
- Collapsed state shows icons with accessible names, and a tooltip as a
  supplement rather than a replacement.
- The collapse state persists across sessions.
- Scroll the sidebar independently of the page, and keep the active item
  visible when the page loads.

## Tabs

Tabs switch views of the same object. If the content is unrelated, it is
navigation, not tabs.

Keyboard behaviour is not optional: arrow keys move between tabs, `Home` and
`End` jump to the ends, and `Tab` moves out of the tablist into the panel.

```html
<div role="tablist" aria-label="Booking details">
  <button role="tab" aria-selected="true" aria-controls="p1" id="t1">Guest</button>
  <button role="tab" aria-selected="false" aria-controls="p2" id="t2" tabindex="-1">Payment</button>
</div>
<div role="tabpanel" id="p1" aria-labelledby="t1" tabindex="0">...</div>
```

Never let tabs wrap onto two rows. Scroll them horizontally with visible
affordance, or use a different pattern.

## Breadcrumbs

Show the path, not the history. The last item is the current page and is not a
link.

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/properties">Properties</a></li>
    <li><span aria-current="page">Harbour Suite</span></li>
  </ol>
</nav>
```

## Mobile

- The primary destinations stay reachable with one thumb.
- A hamburger is acceptable for secondary navigation, never for the primary
  action.
- A bottom bar suits three to five destinations.
- The menu button says what it does: `aria-label="Menu"` at minimum, or a
  visible "Menu" label.
- Opening the menu traps focus and closes on `Esc`.

## Skip link

The first focusable element on every page skips to the main content. See
`../doctrine/accessibility.md`.

## Sticky headers

A sticky header must not hide the focused element when tabbing.

```css
:root { scroll-padding-block-start: 5rem; }
```

Keep sticky headers short. A header taking a fifth of a phone viewport is
taking it from the content.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Active state by colour only | Invisible to many users | Weight plus a rule, and `aria-current` |
| Hamburger on desktop | Hides navigation with room to spare | Show the destinations |
| Tabs that wrap to two rows | Order becomes ambiguous | Scroll, or change pattern |
| Breadcrumbs showing history | Confuses path with back button | Show hierarchy |
| More than 7 top-level items | Exceeds comfortable scanning | Group them |
| Command palette as the only path | Undiscoverable | Always provide a visible route |
| Sticky header hiding focus | Keyboard users lose their place | `scroll-padding-block-start` |
| Sign out as the first item | Prime position for a rare action | Put it last, or in a menu |
