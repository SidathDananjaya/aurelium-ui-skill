# HTML and CSS

The default output. Reach for a framework only when the product genuinely needs
one. Most marketing pages, editorial sites, and small applications do not.

## File structure

```
styles/
  tokens.css        generated, never hand-edited
  base.css          reset, document defaults, typography
  layout.css        container, grid, sections
  components.css    buttons, cards, forms, tables
  utilities.css     a small set, not a framework
index.html
```

Import in that order. Later files may override earlier ones, so the cascade
runs from general to specific.

```css
@import url("tokens.css");
@import url("base.css");
@import url("layout.css");
@import url("components.css");
@import url("utilities.css");
```

For production, concatenate rather than chaining `@import` at runtime, which
serialises requests and delays first paint.

## Tokens

Generate, never hand-write:

```
python scripts/tokens.py --direction obsidian --density 6 --theme auto --format css > styles/tokens.css
```

`tokens.css` is a build artefact. Regenerate it when the direction or dials
change. If you find yourself editing it, the dials were wrong.

## Base

```css
*,
*::before,
*::after { box-sizing: border-box; }

html {
  -webkit-text-size-adjust: 100%;
  scroll-padding-block-start: var(--space-9);
}

body {
  margin: 0;
  background: var(--color-page);
  color: var(--color-text);
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: var(--leading-base);
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, h4 {
  margin: 0;
  font-family: var(--font-display);
  text-wrap: balance;
}

p { margin: 0; text-wrap: pretty; }

img, svg, video { display: block; max-inline-size: 100%; }

:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

Zero out heading and paragraph margins, then control spacing with `gap` on
parents. Margins that collapse are the most common source of rhythm bugs.

`scroll-padding-block-start` keeps a focused element clear of a sticky header.

## Component classes

One class per component, with modifiers. No utility soup, no deep nesting.

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

.btn--primary {
  background: var(--color-accent);
  color: var(--color-accent-fg);
}

.btn--secondary {
  background: transparent;
  color: var(--color-text);
  border-color: var(--color-border);
}
```

Name by what the thing is, not what it looks like. `.btn--primary`, never
`.btn--gold`. The colour changes with the direction. The role does not.

Keep specificity flat. One class, one job. If you need `!important`, the
cascade is already wrong.

## Layout

```css
.container {
  inline-size: 100%;
  max-inline-size: var(--container-max, 75rem);
  margin-inline: auto;
  padding-inline: var(--gutter);
}

:root { --gutter: var(--space-5); }

@media (min-width: 64rem) {
  :root { --gutter: var(--space-9); }
}

.stack { display: grid; gap: var(--space-5); }
.stack--tight { gap: var(--space-3); }
.stack--loose { gap: var(--space-9); }

.grid-auto {
  display: grid;
  gap: var(--space-5);
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr));
}
```

Three layout primitives cover most of a site: a container, a vertical stack,
and an auto grid. Reach for a bespoke grid only when the design needs one.

## Utilities

A handful, not a framework. If the list grows past about fifteen, the component
classes are not doing their job.

```css
.visually-hidden {
  position: absolute;
  inline-size: 1px;
  block-size: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}

.text-muted { color: var(--color-text-muted); }
.tabular { font-variant-numeric: tabular-nums lining-nums; }
.measure { max-inline-size: 68ch; }
```

## Theme switching

The generated `auto` theme already handles system preference and an explicit
override. A toggle only needs to set the attribute and remember it.

```html
<button type="button" class="btn btn--secondary" data-theme-toggle aria-pressed="false">
  Dark theme
</button>
```

```js
const KEY = "theme";
const root = document.documentElement;

function apply(theme) {
  root.setAttribute("data-theme", theme);
  try { localStorage.setItem(KEY, theme); } catch (error) { /* private mode */ }
}

let stored = null;
try { stored = localStorage.getItem(KEY); } catch (error) { stored = null; }
if (stored) apply(stored);
```

Wrap every storage access. It throws in some privacy modes, and an unhandled
throw here breaks the whole script.

To avoid a flash of the wrong theme, set the attribute in an inline script in
the `head`, before the stylesheet renders.

## Progressive enhancement

- The page reads and navigates without JavaScript.
- Forms submit without JavaScript where the backend allows.
- Enhancements are additive, guarded by `@supports` where the feature is new.

```css
@supports (view-transition-name: none) {
  /* enhancement only */
}
```

## Pre-flight

```
python scripts/contrast.py --tokens styles/tokens.css
```

Then walk `../quality/preflight.md` in full.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Hand-editing `tokens.css` | Regeneration silently discards the edit | Change the dials and regenerate |
| Naming by appearance | `.btn--gold` breaks when the direction changes | Name by role |
| Deep descendant selectors | Fragile, high specificity, hard to override | One flat class per component |
| `!important` | The cascade is already wrong | Fix the specificity |
| A hundred utility classes | You rebuilt a framework, badly | Component classes, few utilities |
| Chained `@import` in production | Serialised requests, delayed paint | Concatenate at build |
| Margins on children | Collapse and stray trailing space | `gap` on the parent |
| Unguarded `localStorage` | Throws in private mode, breaks the script | try and catch every access |
| Theme applied after first paint | Visible flash of the wrong theme | Inline script in the head |
