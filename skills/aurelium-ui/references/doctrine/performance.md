# Performance budget

Speed is part of the product. A slow luxury interface is not a luxury
interface. Every number here is a pass or fail threshold, not an aspiration.

## Core Web Vitals

| Metric | Budget | What it measures |
|---|---|---|
| Largest Contentful Paint | under 2.5s | When the main content becomes visible |
| Interaction to Next Paint | under 200ms | Responsiveness to input across the visit |
| Cumulative Layout Shift | under 0.1 | Unexpected movement of visible content |

Measure at the 75th percentile, on a mid-tier mobile device profile and a
throttled connection. A result that only passes on a fast desktop has not
passed.

## Animation

Animate `transform` and `opacity`. These are the only properties the browser can
composite without layout or paint work.

| Instead of | Animate |
|---|---|
| `width`, `height` | `transform: scale()`, or animate a wrapper's clip |
| `top`, `left`, `margin` | `transform: translate()` |
| `box-shadow` | `opacity` on a pseudo-element holding the shadow |
| `background-color` on a large surface | `opacity` on an overlay layer |

`filter` is permitted sparingly, on small elements only. It forces a new
compositing layer and gets expensive at full-viewport size.

**Check.** Record a performance profile while each animation runs. No layout or
paint entries appear during the animation, only compositing.

Never animate anything that is not visible, and never leave an infinite
animation running off screen.

```css
/* Promote deliberately, and only while it animates */
.drawer { transition: transform var(--duration-base) var(--ease-standard); }
.drawer.is-animating { will-change: transform; }
```

Do not leave `will-change` applied permanently. It reserves memory for an
element that is not moving.

## Fonts

- Maximum two families, plus one monospace face for data.
- Maximum four total weights and styles across the whole product.
- `font-display: swap` on every face.
- Preload only the single face used by the largest above-the-fold text.
- Subset to the character ranges you actually need.
- Always declare a fallback stack with similar metrics.

```html
<link
  rel="preload"
  href="/fonts/body-400.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

```css
@font-face {
  font-family: "Body";
  src: url("/fonts/body-400.woff2") format("woff2");
  font-weight: 400;
  font-display: swap;
  size-adjust: 100%;
}
```

**Check.** Count the font files requested on first load. The count matches the
declared face count. No layout shift occurs when the webfont replaces the
fallback. Tune with `size-adjust`, `ascent-override`, and
`descent-override` if it does.

## Images

- Every image declares `width` and `height`, or an `aspect-ratio`, so space is
  reserved before it loads.
- Modern formats, with a fallback.
- `loading="lazy"` below the fold. Never on the LCP image.
- `fetchpriority="high"` on the LCP image.
- Serve responsive sources rather than one oversized file.

```html
<img
  src="/media/suite.avif"
  alt="Corner suite with sea view"
  width="1440"
  height="960"
  fetchpriority="high"
  decoding="async"
/>
```

**Check.** Load each page with images disabled. The layout holds its shape. No
content jumps when they arrive.

## Layout stability

Reserve space for anything that arrives late:

- Banners, cookie notices, and announcement bars. Render them in the initial
  layout or overlay them, never insert them above existing content.
- Embeds and iframes get a sized container.
- Skeletons match the dimensions of the content that replaces them. A skeleton
  that is a different height than the real content causes the shift it was
  meant to prevent.

## JavaScript

- Ship no framework for a page that does not need one. The default output of
  this skill is HTML and CSS.
- Defer anything not needed for first render.
- Prefer CSS for motion. Reach for a motion library only for gestures, shared
  element transitions, or physics.
- Break long tasks. A single task over 50ms blocks input and damages INP.

**Check.** Disable JavaScript. Content is still readable and navigation still
works, unless the product is genuinely an application rather than a document.

## The pre-flight numbers

Before saying a build is done:

1. LCP under 2.5s, INP under 200ms, CLS under 0.1 on a throttled mobile profile.
2. Only `transform` and `opacity` animate.
3. Font file count matches declared faces, no shift on swap.
4. Every image has reserved dimensions.
5. No console errors or warnings.
6. No infinite animation outside a live status indicator.
