# React

Tokens live in CSS. Components consume them. Moving the palette into
JavaScript objects forks the system and breaks the contrast check, which reads
CSS custom properties.

## Structure

```
src/
  styles/
    tokens.css      generated, never hand-edited
    base.css
  components/
    Button/
      Button.tsx
      Button.module.css
  App.tsx
```

Colocate the component with its styles. A component and its CSS that live apart
drift apart.

## Tokens

Generate them, then import once at the application root:

```
python scripts/tokens.py --direction obsidian --density 6 --theme auto --format css > src/styles/tokens.css
```

```tsx
// src/main.tsx
import "./styles/tokens.css";
import "./styles/base.css";
```

`tokens.css` is a build artefact. When the direction or the dials change,
regenerate it. Editing it by hand means the next regeneration silently discards
the change.

Do not import the palette into JavaScript. `contrast.py` reads CSS custom
properties, so a palette that lives in a TypeScript object cannot be checked,
and the AA guarantee lapses without anyone noticing.

## A component

```tsx
import styles from "./Button.module.css";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "tertiary";
  loading?: boolean;
};

export function Button({
  variant = "secondary",
  loading = false,
  children,
  ...rest
}: ButtonProps) {
  return (
    <button
      className={`${styles.btn} ${styles[variant]}`}
      data-loading={loading}
      aria-busy={loading}
      {...rest}
    >
      <span className={styles.label}>{children}</span>
    </button>
  );
}
```

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  min-block-size: 44px;
  padding: var(--space-3) var(--space-5);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  font: inherit;
  font-weight: 600;
  cursor: pointer;
  transition: background var(--duration-fast) var(--ease-standard);
}

.primary { background: var(--color-accent); color: var(--color-accent-fg); }

.secondary {
  background: transparent;
  color: var(--color-text);
  border-color: var(--color-border);
}

.btn:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Keeps the width while the spinner replaces the label */
.btn[data-loading="true"] .label { visibility: hidden; }
```

Spreading `...rest` means the component accepts `type`, `disabled`,
`aria-label` and every handler without re-declaring them. A component that
blocks standard attributes will be worked around within a week.

`aria-busy` communicates the loading state. `data-loading` drives the styling.
Both are needed: one for assistive technology, one for CSS.

## Variants

Prefer data attributes over class concatenation for state, because they are
visible in devtools and queryable in tests.

```tsx
<div data-state={open ? "open" : "closed"} className={styles.drawer} />
```

```css
.drawer { transform: translateX(100%); }
.drawer[data-state="open"] { transform: translateX(0); }
```

## Theme

One provider, one attribute, storage guarded.

```tsx
const KEY = "theme";

function readStored(): string | null {
  try { return localStorage.getItem(KEY); } catch { return null; }
}

export function useTheme() {
  const [theme, setTheme] = React.useState<string | null>(null);

  React.useEffect(() => {
    const initial = readStored();
    if (initial) document.documentElement.setAttribute("data-theme", initial);
    setTheme(initial);
  }, []);

  const change = React.useCallback((next: string) => {
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem(KEY, next); } catch { /* private mode */ }
    setTheme(next);
  }, []);

  return { theme, setTheme: change };
}
```

Read storage inside an effect, not during render. Reading it during render
breaks server rendering and causes a hydration mismatch.

To prevent a flash of the wrong theme, set the attribute in a small inline
script before React mounts.

## Motion

CSS first. Reach for a motion library only for gestures, shared element
transitions, or physics. A library imported to fade a modal is a dependency
that did not earn its place.

```css
.modal {
  opacity: 0;
  transform: scale(0.97);
  transition:
    opacity var(--duration-fast) var(--ease-exit),
    transform var(--duration-fast) var(--ease-exit);
}

.modal[data-state="open"] {
  opacity: 1;
  transform: scale(1);
  transition:
    opacity var(--duration-base) var(--ease-entrance),
    transform var(--duration-base) var(--ease-entrance);
}

@media (prefers-reduced-motion: reduce) {
  .modal, .modal[data-state="open"] {
    transform: none;
    transition: opacity var(--duration-fast) var(--ease-standard);
  }
}
```

If you do use a motion library, respect reduced motion through its own API
rather than assuming the CSS media query covers it. A JavaScript-driven
animation ignores the CSS override entirely.

See `../motion/recipes.md`.

## Accessibility in components

React makes it easy to build inaccessible components quickly. The usual
failures:

- A `div` with `onClick` instead of a `button`. Not focusable, no Enter or
  Space, invisible to assistive technology.
- Focus not managed when a modal opens or closes.
- `key` set to the array index, so React reuses DOM nodes and focus lands on
  the wrong row after a reorder.
- Conditional rendering that removes the focused element without moving focus,
  dropping it to the body.
- Icon-only buttons with no accessible name.

```tsx
// Focus returns to the trigger when the dialog closes
const triggerRef = React.useRef<HTMLButtonElement>(null);

React.useEffect(() => {
  if (!open) triggerRef.current?.focus();
}, [open]);
```

Prefer the native `dialog` element, or a headless library that handles focus
management, over hand-rolling it.

## Lists and state

```tsx
{items.map((item) => (
  <Row key={item.id} item={item} />
))}
```

`key` is the item's stable identity, never the index. With an index key, React
reuses the wrong nodes on reorder and the user's focus, selection, and input
follow the wrong row.

Render every state from `../patterns/states.md`, not just the loaded one:

```tsx
if (error) return <ErrorState onRetry={retry} error={error} />;
if (loading) return <Skeleton rows={5} />;
if (!items.length && query) return <NoResults query={query} onClear={clear} />;
if (!items.length) return <FirstUse onCreate={create} />;
return <List items={items} />;
```

Ordering matters: error before loading, and the two empty states distinguished
by whether a query is active.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Palette in a JavaScript object | Forks the system, breaks the contrast check | CSS custom properties |
| Inline styles for design values | Bypasses tokens, no theme switching | Classes referencing tokens |
| `div` with `onClick` | Not focusable, not announced | `button` |
| Array index as `key` | Wrong nodes reused, focus lands wrong | Stable identity |
| Reading storage during render | Hydration mismatch | Read in an effect |
| A motion library to fade a modal | Dependency that did not earn its place | CSS transitions |
| Only the loaded state rendered | The product fails on first contact with reality | Every state |
| Hand-rolled modal focus | Almost always incomplete | Native `dialog`, or a headless library |
| Props that block standard attributes | Worked around within a week | Spread the rest |
| Styling state with class concatenation | Invisible in devtools, awkward in tests | Data attributes |
