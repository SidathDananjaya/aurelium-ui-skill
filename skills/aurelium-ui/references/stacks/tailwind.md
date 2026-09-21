# Tailwind

Tailwind is a delivery mechanism for the design system, not a replacement for
it. The tokens stay the source of truth.

## Generate the theme

```
python scripts/tokens.py --direction obsidian --density 6 --theme auto --format tailwind > src/styles/theme.css
```

Then import it after Tailwind:

```css
@import "tailwindcss";
@import "./theme.css";
```

The generated file contains two layers:

1. **Raw tokens** under an `au-` namespace, in `:root` and the dark theme
   blocks. These carry the actual values and switch with the theme.
2. **A `@theme inline` layer** mapping Tailwind's namespaces to those tokens.

## Why `inline` is not optional

Tailwind v4 is CSS first: the theme is declared with `@theme`, not a JavaScript
config.

```css
@theme inline {
  --color-page: var(--au-color-page);
}
```

Without `inline`, Tailwind resolves the variable **at build time** and bakes in
whatever the light palette held. The utilities then keep light colours forever
and theme switching silently stops working, while every class name still looks
correct. It is a failure that survives review.

`inline` keeps the `var()` reference in the output, so `bg-page` follows
`--au-color-page` and switches with the theme.

## Why the `au-` prefix

Tailwind owns the `--color-*`, `--text-*`, `--spacing-*`, `--radius-*`,
`--shadow-*`, `--font-*` and `--ease-*` namespaces. Declaring raw values there
would collide, and `--color-page: var(--color-page)` is circular.

The raw tokens therefore live under `au-`, and the theme layer maps across.

It also keeps `contrast.py` working, because the generated `contrast-pairs`
comment names the prefixed properties:

```
python scripts/contrast.py --tokens src/styles/theme.css
```

## Using it

```html
<button class="inline-flex items-center gap-2 min-h-11 px-5 py-3
               rounded-md bg-accent text-accent-fg font-semibold
               transition-colors duration-fast ease-standard
               hover:bg-accent-hover
               focus-visible:outline-2 focus-visible:outline-focus
               focus-visible:outline-offset-2">
  Confirm booking
</button>
```

Every class resolves to a token. Nothing is arbitrary.

## No arbitrary values

An arbitrary value is a token that escaped the system.

| Instead of | Write |
|---|---|
| `bg-[#6b5423]` | `bg-accent` |
| `p-[13px]` | `p-3` |
| `rounded-[10px]` | `rounded-md` |
| `text-[17px]` | `text-lg` |
| `duration-[220ms]` | `duration-base` |
| `shadow-[0_2px_6px_rgba(0,0,0,.22)]` | `shadow-e2` |

**Check.** Grep the markup for `-[`. Every hit is either a genuine one-off with
a comment explaining it, or a bug.

If you need a value the scale does not have, the question is whether the scale
is wrong, not whether to escape it. Change the dials and regenerate.

## Extracting components

Utility classes on repeated elements become unreadable and drift apart. Extract
once a pattern appears three times.

In a component framework, extract to a component. In plain HTML, use
`@apply` sparingly:

```css
@layer components {
  .btn {
    @apply inline-flex items-center justify-center gap-2 min-h-11 px-5 py-3
           rounded-md font-semibold transition-colors duration-fast ease-standard;
  }

  .btn-primary { @apply bg-accent text-accent-fg hover:bg-accent-hover; }
}
```

`@apply` is a last resort. It reintroduces the indirection Tailwind exists to
remove, and it does not work in `@theme`. Prefer a real component.

## Theme switching

The generated file already handles `prefers-color-scheme` and the
`[data-theme]` override. Tell Tailwind about the attribute so `dark:` variants
follow the same switch:

```css
@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));
```

Most components should not need `dark:` at all. If the colour comes from a
semantic token, it already switched.

Reaching for `dark:` often means a hard-coded colour is hiding underneath.

## Reduced motion

The generated tokens collapse durations under `prefers-reduced-motion`, so
`duration-base` shortens automatically. Movement still needs handling per
component:

```html
<div class="translate-y-2 motion-reduce:translate-y-0
            transition-transform duration-base ease-standard">
```

## Content scanning

Tailwind only generates classes it can see. A class assembled at runtime does
not exist in the output.

```jsx
// Broken: the class is never seen by the scanner
<div className={`bg-${color}`} />

// Correct: full class names, statically visible
const TONE = { danger: "bg-danger", success: "bg-success" };
<div className={TONE[tone]} />
```

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| `@theme` without `inline` for referenced vars | Values bake in, theme switching dies silently | `@theme inline` |
| Redefining the scale in the config | Forks the system, breaks the contrast check | Map to the generated tokens |
| Arbitrary values | Tokens that escaped the system | Use the scale, or change the dials |
| A JavaScript config in v4 | The v3 shape. Ignored or deprecated | CSS first with `@theme` |
| `dark:` on every element | A hard-coded colour is hiding underneath | Semantic tokens that switch |
| `@apply` everywhere | Reintroduces the indirection Tailwind removes | Extract a component |
| Interpolated class names | The scanner never sees them | Full class names in a map |
| Long class strings never extracted | Unreadable, and they drift apart | Extract at the third repetition |
| Hand-editing the generated theme | Regeneration discards it | Change the dials and regenerate |
