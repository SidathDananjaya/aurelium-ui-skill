# Imagery

Imagery is the most expensive surface in an interface to get right and the
easiest to get wrong. One considered image beats six decorative ones.

## Art direction

Every image answers a question: what does this tell the user that text cannot?
An image that answers nothing is removed, not shrunk.

| Archetype | Image role | Treatment |
|---|---|---|
| Hospitality, fashion, editorial | Carries the mood, often the hero | Large, few, high quality, minimal overlay |
| E-commerce | The product is the content | Consistent angle, consistent background, generous crop |
| SaaS, dashboards, dev tools | Usually none. Real UI beats stock | Product screenshots, framed honestly |
| Fintech | Trust signals, not lifestyle photos | Restrained, often illustration or none |

**Don't.** Use a stock photograph of people smiling at a laptop. It reads as
filler on sight and tells the user nothing.
**Do.** Show the actual product, the actual room, the actual object.

## Aspect ratios

Pick a small set and hold it across the product. Mixed ratios in one grid break
the rhythm more than mixed subjects do.

| Ratio | Use |
|---|---|
| 1:1 | Product thumbnails, avatars, grids |
| 4:3 | Editorial cards, interiors |
| 3:2 | Photography, the standard camera ratio |
| 16:9 | Video, wide hero |
| 2:3 or 3:4 | Portrait, fashion, architecture |

Always reserve the space before the image arrives.

```css
.media {
  aspect-ratio: 3 / 2;
  inline-size: 100%;
  overflow: hidden;
  border-radius: var(--radius-md);
}

.media img {
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
  object-position: center;
}
```

`object-fit: cover` crops. When the subject is not centred, set
`object-position` per image rather than accepting a bad crop. For images where
nothing may be cropped, such as a logo or a diagram, use `contain`.

## Responsive sources

Serve an image sized for the slot, not the largest one available.

```html
<img
  src="/media/suite-800.jpg"
  srcset="/media/suite-400.jpg 400w,
          /media/suite-800.jpg 800w,
          /media/suite-1600.jpg 1600w"
  sizes="(min-width: 64rem) 50vw, 100vw"
  alt="Corner suite with a view over the harbour at dusk"
  width="1600"
  height="1067"
  loading="lazy"
  decoding="async"
/>
```

Rules that always apply:

- `width` and `height` are always present, even when CSS overrides them. They
  give the browser the ratio and prevent layout shift.
- `loading="lazy"` below the fold, never on the largest above-the-fold image.
- `fetchpriority="high"` on the hero image.
- Modern formats with a fallback via `picture` when the toolchain allows.

See `../doctrine/performance.md` for the budget these rules serve.

## Overlays and legibility

Text over an image needs a guaranteed contrast floor. A photograph's brightness
varies, so the overlay is what makes the text safe, not the photograph.

```css
.hero {
  position: relative;
  isolation: isolate;
}

.hero::after {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  /* Gradient scrim: strongest where the text sits */
  background: linear-gradient(
    to top,
    oklch(0% 0 0 / 0.72) 0%,
    oklch(0% 0 0 / 0.40) 45%,
    oklch(0% 0 0 / 0.05) 100%
  );
}
```

**Check.** Sample the lightest pixel under the text. Contrast still meets 4.5:1
there. A flat 20 percent scrim almost never survives this test.

Prefer a gradient scrim over a flat one. It protects the text without flattening
the whole image.

Never place body copy over a busy area. Move the text to a solid panel instead.

## Placeholder strategy

While an image loads, and when it is missing, the slot still holds its shape.

| Situation | Treatment |
|---|---|
| Loading | Neutral surface at the exact aspect ratio, optionally a blurred tiny preview |
| Missing or failed | Neutral surface with a small muted icon, never a broken image glyph |
| Not yet uploaded | Surface with a clear action, such as "Add a photo" |
| Avatar with no image | Initials on a neutral surface, never a random color per user |

```css
.media {
  background: var(--neutral-100);
}

[data-theme="dark"] .media {
  background: var(--neutral-800);
}
```

Do not animate a shimmer on an image placeholder unless the wait exceeds 400ms.
A shimmer that appears and vanishes instantly reads as a flicker.

For demonstration and eval work, use plainly neutral placeholder blocks rather
than watermarked stock. A grey rectangle is honest. A watermarked photo is not.

## Alt text

Alt text describes the image's purpose in this context, not its contents in
full.

| Image role | Alt text |
|---|---|
| Decorative, meaning already in the text | `alt=""`, always present, never omitted |
| Informative | Describe what matters here, in one sentence |
| Functional, such as a logo that links home | Describe the destination, not the picture |
| Complex, such as a chart | Short alt, plus the data in text or a table nearby |

**Do.** `alt="Corner suite with a view over the harbour at dusk"`
**Don't.** `alt="image"`, `alt="suite-final-v2.jpg"`, or
`alt="Photo of a hotel room showing a bed, two lamps, a window, curtains..."`

Never start alt text with "Image of" or "Photo of". The screen reader already
announced that it is an image.

An empty `alt` attribute is a decision. A missing one is a bug, because the
screen reader then reads the filename.

## Video

- Never autoplay with sound.
- Autoplay only when muted, short, looping, and decorative, and respect
  `prefers-reduced-motion` by showing a still instead.
- Always provide a poster image at the same aspect ratio.
- Captions for any video carrying speech.

```html
<video poster="/media/loop-poster.jpg" muted loop playsinline
       width="1600" height="900">
  <source src="/media/loop.webm" type="video/webm" />
</video>
```

```css
@media (prefers-reduced-motion: reduce) {
  video[autoplay] { display: none; }
  .video-fallback { display: block; }
}
```

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Generic stock photography | Reads as filler instantly | Real product, real place, or nothing |
| Mixed aspect ratios in one grid | Breaks the rhythm | One ratio per grid |
| Missing `width` and `height` | Layout shift when it loads | Always declare them |
| Flat 20 percent scrim under text | Fails contrast over bright areas | Gradient scrim, verified by sampling |
| `alt="image"` or a filename | Useless to a screen reader | Purposeful description, or `alt=""` |
| Autoplaying video with sound | Hostile, and often blocked anyway | Muted, short, with a reduced-motion fallback |
| Lazy loading the hero image | Delays LCP, the opposite of the intent | `fetchpriority="high"` on the hero |
| A broken image icon on failure | Looks unfinished | Neutral placeholder at the right ratio |
