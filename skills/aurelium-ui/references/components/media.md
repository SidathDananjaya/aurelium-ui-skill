# Media

Galleries, product imagery, and video. One considered image beats six
decorative ones. See `../foundations/imagery.md` for art direction and alt text.

## Galleries

A gallery has a lead image and thumbnails. The lead never changes size when the
selection changes, which means the container is sized by aspect ratio rather
than by the current image.

```html
<div class="gallery">
  <div class="gallery-main">
    <img
      src="/media/suite-01.jpg"
      alt="Harbour Suite seen from the doorway, bed facing the window"
      width="1200"
      height="800"
      fetchpriority="high"
    />
  </div>
  <ul class="gallery-thumbs" role="tablist" aria-label="Suite photographs">
    <li>
      <button role="tab" aria-selected="true" type="button">
        <img src="/media/suite-01-thumb.jpg" alt="" width="120" height="80" />
        <span class="visually-hidden">Photo 1 of 6</span>
      </button>
    </li>
  </ul>
</div>
```

```css
.gallery-main {
  aspect-ratio: 3 / 2;
  overflow: hidden;
  border-radius: var(--radius-lg);
  background: var(--color-border);
}

.gallery-main img {
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
}

.gallery-thumbs {
  display: flex;
  gap: var(--space-3);
  margin-block-start: var(--space-3);
  padding: 0;
  list-style: none;
  overflow-x: auto;
  scrollbar-gutter: stable;
}

.gallery-thumbs button {
  padding: 0;
  border: 2px solid transparent;
  border-radius: var(--radius-sm);
  background: none;
  cursor: pointer;
  line-height: 0;
}

.gallery-thumbs [aria-selected="true"] {
  border-color: var(--color-accent);
}

.gallery-thumbs button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

Thumbnail `alt` is empty because the button's hidden text already names it.
Duplicating the description makes a screen reader read everything twice.

Rules that always apply:

- Arrow keys move between thumbnails.
- The count is stated: "Photo 1 of 6".
- The selected thumbnail is marked by a border, not by opacity alone.
- Preload the lead image, lazy-load the rest.

## Carousels

Most carousels are a way to hide content the team could not prioritise. Before
building one, ask whether a grid would serve better. Users rarely reach slide
three.

If a carousel is genuinely right:

- Never auto-advance. If you must, pause on hover, on focus, and under
  `prefers-reduced-motion`.
- Always provide visible previous and next controls, at full target size.
- Indicate position and total.
- Make it keyboard operable and swipeable.
- Never put the primary call to action on a slide that scrolls away.

## Product imagery

- One angle convention across the catalogue, one background, one crop.
- Consistent aspect ratio across every listing.
- Zoom on the detail page, either on hover for pointer or tap to open for touch.
- Show scale where size is ambiguous, with a known object or a stated dimension.
- Colour variants swap the image, and the alt text updates with them.

Inconsistent product photography undoes an otherwise excellent interface faster
than almost any other single factor.

## Video

- Never autoplay with sound.
- Autoplay only when muted, short, looping, and decorative.
- Always provide a poster at the same aspect ratio so nothing shifts.
- Captions for any video carrying speech. Captions are not optional.
- Provide a transcript for anything instructional.
- Controls are visible, keyboard operable, and at full target size.

```html
<video
  poster="/media/tour-poster.jpg"
  width="1600"
  height="900"
  muted
  loop
  playsinline
  controls
>
  <source src="/media/tour.webm" type="video/webm" />
  <track kind="captions" src="/media/tour.vtt" srclang="en" label="English" default />
</video>
```

```css
@media (prefers-reduced-motion: reduce) {
  video[autoplay] { display: none; }
  .video-poster-fallback { display: block; }
}
```

Under reduced motion, an autoplaying background video is replaced by its
poster, not merely paused.

## Lightbox

- Opens with focus moved into it, traps focus, closes on `Esc`.
- Returns focus to the thumbnail that opened it.
- Arrow keys move between images.
- Shows position: "3 of 12".
- The close control is at full target size, not a 12px glyph in the corner.

See `overlays.md` for the focus rules, which apply in full.

## Aspect ratio and layout stability

Every image and video declares dimensions or an `aspect-ratio`. This is the
single most common cause of layout shift, and it is entirely preventable.

The placeholder occupies the exact final dimensions. A skeleton of a different
height causes the shift it was meant to prevent.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Gallery resizing per image | Page jumps on every selection | Fixed aspect ratio container |
| Auto-advancing carousel | Steals control, unreadable | Manual, or a grid |
| Primary action on a carousel slide | Scrolls out of reach | Keep it fixed |
| Duplicated alt on thumbnails | Screen reader reads everything twice | Empty alt plus hidden label |
| Autoplay with sound | Hostile, often blocked | Muted, or no autoplay |
| Video with no captions | Excludes many users outright | Always caption speech |
| Missing width and height | Layout shift on load | Always declare them |
| Lazy loading the hero image | Delays LCP, the opposite of intent | `fetchpriority="high"` |
| Selected thumbnail by opacity only | Ambiguous, fails contrast | Visible border |
| 12px close button on a lightbox | Nearly unhittable | Full 44px target |
