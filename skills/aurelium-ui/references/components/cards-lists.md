# Cards and lists

A card is a container for one object. A list is a sequence of them. Most
interfaces use cards where a list would read better.

## When a card earns its place

Use a card when the object has an image, several attributes, and its own
actions. Otherwise use a list row, which is denser and easier to scan.

| Content | Use |
|---|---|
| Image plus title plus metadata plus action | Card |
| Title plus one or two values | List row |
| Mostly figures, compared across items | Table |
| One attribute per item | Plain list |

A grid of cards each holding a title and one line of text should have been a
list. The card added a boundary and took away density.

## Anatomy

| Part | Rule |
|---|---|
| Media | One aspect ratio across the grid |
| Title | One line preferred, two maximum, then truncate |
| Metadata | Muted, smaller step, never more than three items |
| Body | Optional, two to three lines, then truncate |
| Actions | One primary at most, aligned to the end |

Padding is uniform on all sides, from the spacing scale. Inner gaps are smaller
than the gap between cards.

## Separation, in order of preference

1. **Space.** Distance alone, no boundary.
2. **Surface.** A different background lightness.
3. **Hairline.** A one pixel border.
4. **Shadow.** Only when the card genuinely floats, such as a dragged item.

Most card grids need step one or two. A shadow on every card makes elevation
meaningless. See `../foundations/surfaces-depth.md`.

```html
<article class="card">
  <div class="card-media">
    <img src="/media/suite.jpg" alt="Harbour suite at dusk" width="800" height="533" />
  </div>
  <div class="card-body">
    <h3 class="card-title">Harbour Suite</h3>
    <p class="card-meta">Sleeps 2 . Sea view . 42 sq m</p>
    <p class="card-price"><b>240</b> per night</p>
  </div>
</article>
```

```css
.card-grid {
  display: grid;
  gap: var(--space-5);
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr));
}

.card {
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.card-media {
  aspect-ratio: 3 / 2;
  background: var(--color-border);
}

.card-media img {
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
}

.card-body {
  display: grid;
  gap: var(--space-2);
  padding: var(--space-5);
}

.card-title {
  margin: 0;
  font-size: var(--text-lg);
  line-height: var(--leading-lg);
  text-wrap: balance;
}

.card-meta {
  margin: 0;
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.card-price {
  margin: 0;
  font-variant-numeric: tabular-nums;
}
```

`min(100%, 18rem)` prevents overflow when the container is narrower than the
track minimum, which is the usual `auto-fit` bug.

## Concentric radii

Media inside a card uses the outer radius minus the padding between them. An
inner radius larger than its outer radius always looks broken.

## The whole card as a target

If the whole card navigates, the title carries the link and the card stretches
its hit area. This keeps one link per card in the accessibility tree instead of
three competing ones.

```css
.card { position: relative; }

.card-title a::after {
  content: "";
  position: absolute;
  inset: 0;
}

/* Anything that must stay clickable sits above the stretched link */
.card-actions { position: relative; z-index: 1; }
```

Never wrap the entire card in an `a` containing a button. Interactive elements
cannot nest.

## Long content

Every card must survive a very long title, a missing image, and a missing
price. Test with the worst realistic content, not the tidiest.

```css
.card-title {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

Truncate with a clamp rather than a fixed height, and never truncate a price,
a date, or anything the user needs in full.

## Lists

- Separate rows with a hairline, not a gap, so the list reads as one object.
- Row height is consistent. A row that grows with content breaks the rhythm.
- Put the identifying value first and the changing value last.
- A row that is clickable shows it on hover and focus.

## Selection

Selected state uses a background change plus a visible marker, never colour
alone. Bulk selection needs a select-all that states what it selected: "All 24
on this page" is not the same as "All 312".

## States

Every card grid and list ships the full state set from `../patterns/states.md`.
The two most often missed: empty after filtering, and a single very long item.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Shadow on every card | Elevation stops meaning anything | Hairline or surface |
| Mixed aspect ratios in one grid | Breaks the rhythm | One ratio |
| Card for a title and one line | Adds boundary, removes density | List row |
| Nested interactive elements | Invalid, breaks keyboard | Stretched link on the title |
| Fixed card height | Overflows with real content | Let content grow, clamp text |
| Inner radius larger than outer | Looks broken | Concentric radii |
| Truncating a price or date | Removes the information they needed | Truncate prose only |
| Three competing links per card | Tab order becomes noise | One stretched link |
