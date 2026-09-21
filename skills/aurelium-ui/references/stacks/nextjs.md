# Next.js

Everything in `react.md` applies. This covers what Next.js does differently:
font loading, metadata, and images.

## Fonts

`next/font` self-hosts the font at build time, so there is no request to a
third-party host, no privacy concern, and no render-blocking stylesheet. It
also generates a fallback with matched metrics, which is what removes the
layout shift on swap.

Use the `variable` option so the font becomes a custom property that the token
system can consume.

```tsx
// app/layout.tsx
import { Fraunces, Manrope, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const display = Fraunces({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-display-face",
});

const body = Manrope({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-body-face",
});

const mono = JetBrains_Mono({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-mono-face",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${display.variable} ${body.variable} ${mono.variable}`}
    >
      <body>{children}</body>
    </html>
  );
}
```

Then point the generated tokens at those faces, in a file imported after
`tokens.css`:

```css
:root {
  --font-display: var(--font-display-face), Georgia, serif;
  --font-body: var(--font-body-face), ui-sans-serif, system-ui, sans-serif;
  --font-mono: var(--font-mono-face), ui-monospace, monospace;
}
```

The `-face` suffix keeps the two layers distinct: Next.js owns the face, the
token owns the stack. Overwriting `--font-body` directly from `next/font`
would drop the fallback stack.

Rules:

- Subset to the scripts you need. Loading the full range for `latin` only is
  waste.
- `display: "swap"` on every face.
- Declare fonts at module scope, never inside a component. Calling the loader
  in a render creates a new font on every render.
- Two families plus mono, matching the performance budget.

## Metadata

```tsx
// app/layout.tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  metadataBase: new URL("https://example.com"),
  title: {
    default: "Harbour House",
    template: "%s | Harbour House",
  },
  description: "A seventeen room hotel on the Galle waterfront.",
  openGraph: {
    type: "website",
    siteName: "Harbour House",
    images: [{ url: "/og.png", width: 1200, height: 630 }],
  },
};
```

Per route:

```tsx
export const metadata: Metadata = {
  title: "Harbour Suite",
  description: "Corner suite with a view over the harbour.",
};
```

`metadataBase` is required for relative Open Graph URLs to resolve. Without it
they silently stay relative and every social preview breaks.

The `template` gives per-page titles the suffix without repeating it.

## Theme without a flash

Server rendering makes the flash worse: the server has no access to
`localStorage`, so it always renders the default. Set the attribute before
first paint.

```tsx
// app/layout.tsx, inside <head>
<script
  dangerouslySetInnerHTML={{
    __html: `(function(){try{var t=localStorage.getItem("theme");
      if(t)document.documentElement.setAttribute("data-theme",t);}catch(e){}})();`,
  }}
/>
```

This is one of the few legitimate uses of `dangerouslySetInnerHTML`: the
content is a fixed literal with no interpolated input.

Never read `localStorage` during render. It does not exist on the server, and
the resulting hydration mismatch is reported as a warning rather than an error,
so it is easy to miss.

## Images

```tsx
import Image from "next/image";

<Image
  src="/media/suite.jpg"
  alt="Corner suite with a view over the harbour at dusk"
  width={1600}
  height={1067}
  priority
  sizes="(min-width: 64rem) 50vw, 100vw"
/>;
```

- `width` and `height` are required for local images and reserve the space.
- `priority` on the LCP image only. It preloads, and marking several defeats
  the purpose.
- Never `priority` and `loading="lazy"` together.
- `sizes` matters whenever the image is not full width. Without it the browser
  assumes 100vw and downloads a file far larger than the slot.
- `fill` needs a positioned parent with a known aspect ratio.

For a remote image, configure the host. An unconfigured host throws at runtime
rather than degrading.

## Server and client components

Design work mostly lives in server components, which ship no JavaScript.

Add `"use client"` only where interactivity requires it: a theme toggle, a
drawer, a form with live validation. Push the boundary as far down the tree as
possible.

```tsx
// A server component rendering a small client island
import { ThemeToggle } from "./ThemeToggle"; // "use client"

export default function Header() {
  return (
    <header>
      <nav>{/* static, no JavaScript shipped */}</nav>
      <ThemeToggle />
    </header>
  );
}
```

Marking the root layout `"use client"` sends the whole tree to the browser and
discards most of the framework's benefit.

## CSS

- One `globals.css` imported in the root layout, containing `tokens.css` and
  the base layer.
- CSS Modules for components.
- Import order in the root layout determines the cascade.

```tsx
import "./globals.css"; // tokens first, then base
```

## Pre-flight

The generated tokens are plain CSS, so the check is unchanged:

```
python scripts/contrast.py --tokens app/tokens.css
```

Then walk `../quality/preflight.md`.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Google Fonts via a stylesheet link | Render-blocking, third-party request, layout shift | `next/font` |
| Font loader called inside a component | A new font object on every render | Module scope |
| Overwriting `--font-body` from `next/font` | Drops the fallback stack | A `-face` variable the token references |
| Missing `metadataBase` | Relative Open Graph URLs never resolve | Set it once in the root layout |
| Reading `localStorage` during render | Hydration mismatch, only a warning | Inline script before paint |
| `priority` on several images | Preloading everything preloads nothing | The LCP image only |
| Omitting `sizes` on a partial-width image | Downloads a file far larger than the slot | Always set `sizes` |
| `"use client"` on the root layout | Ships the whole tree, discards the framework | Push the boundary down |
| Plain `img` for local images | No optimisation, no reserved space | `next/image` |
| Unconfigured remote image host | Throws at runtime | Configure the host |
