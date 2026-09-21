# Spacing and layout

Space is the material. It is the primary tool for grouping, hierarchy, and
calm. Every spacing value in the product comes from one scale.

## The 4px base grid

Every margin, padding, gap, and size is a multiple of 4px. The only exceptions
are hairline borders and deliberate optical corrections, each of which carries a
comment explaining itself.

```css
:root {
  --space-0:  0;
  --space-1:  0.25rem; /*  4px */
  --space-2:  0.5rem;  /*  8px */
  --space-3:  0.75rem; /* 12px */
  --space-4:  1rem;    /* 16px */
  --space-5:  1.5rem;  /* 24px */
  --space-6:  2rem;    /* 32px */
  --space-7:  2.5rem;  /* 40px */
  --space-8:  3rem;    /* 48px */
  --space-9:  4rem;    /* 64px */
  --space-10: 5rem;    /* 80px */
  --space-11: 6rem;    /* 96px */
  --space-12: 8rem;    /* 128px */
  --space-13: 10rem;   /* 160px */
}
```

The scale is not linear. Steps are close together at small sizes, where
precision matters, and spread apart at large sizes, where the difference between
96px and 100px is invisible.

**Check.** Grep the stylesheet for `px` and `rem` values in spacing properties.
Every one resolves to a token.

## The density dial changes the scale, not the grid

Density multiplies the scale. It never abandons the 4px base.

| Density | Multiplier | Card padding | Section padding at desktop |
|---|---|---|---|
| 1 to 3, spacious | 1.25 | 32 to 40px | 128 to 160px |
| 4 to 6, balanced | 1.0 | 24px | 80 to 96px |
| 7 to 10, dense | 0.75 | 12 to 16px | 40 to 48px |

## Inner spacing is always less than outer

This is the single most reliable rule in layout. Items in a group sit closer to
each other than the group sits to its neighbours. Break it and the eye groups
the wrong things.

```css
.field {
  display: grid;
  gap: var(--space-2); /* 8px between label and input */
}

.field-set {
  display: grid;
  gap: var(--space-5); /* 24px between one field and the next */
}
```

**Check.** For every group on the screen, measure the largest internal gap and
the smallest external gap. Internal must be smaller. Always.

**Do.** A card with 24px padding, 12px between its rows, and 32px between cards.
**Don't.** A card with 16px padding sitting 16px from the next card, so the
boundary disappears.

## Vertical rhythm

Space between blocks expresses their relationship, not a fixed cadence.

| Relationship | Gap |
|---|---|
| Label to its control | `--space-2` |
| Rows within a card | `--space-3` to `--space-4` |
| Sibling components | `--space-5` to `--space-6` |
| Subsection to subsection | `--space-7` to `--space-8` |
| Major section to major section | `--space-9` to `--space-13` |

Space above a heading is always larger than the space below it. The heading
belongs to what follows, not to what precedes it.

```css
.section-heading {
  margin-block-start: var(--space-9);
  margin-block-end: var(--space-4);
}
```

Prefer `gap` on a flex or grid parent over margins on children. Gap cannot
collapse, cannot double up, and cannot leave a stray margin at the end of a list.

## Breakpoints

Design at four widths. These are the four to screenshot and the four to test.

| Width | Target | Columns | Gutter | Margin |
|---|---|---|---|---|
| 375px | Phone | 4 | 16px | 20px |
| 768px | Tablet | 8 | 24px | 32px |
| 1024px | Small laptop | 12 | 24px | 40px |
| 1440px | Desktop | 12 | 32px | 64px |

Write breakpoints mobile first, with `min-width` queries. Add a breakpoint when
the content breaks, not because a device exists.

## Containers

Content has a maximum width even when the viewport does not.

| Content | Maximum |
|---|---|
| Long-form reading | 68ch, roughly 680px |
| Standard app content | 1200px |
| Wide dashboard | 1440px |
| Full bleed media | none |

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
```

Never let a container run edge to edge on a large screen. Text that starts at
the left bezel and ends at the right has no frame and reads as unfinished.

## Grids

Use CSS Grid for two-dimensional layout and Flexbox for one direction.

Prefer intrinsic layouts that need no breakpoint at all:

```css
.card-grid {
  display: grid;
  gap: var(--space-5);
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr));
}
```

`min(100%, 18rem)` prevents overflow when the container is narrower than the
track minimum, which is the usual bug with `auto-fit`.

**Do.** Align items to a shared grid so edges line up across sections.
**Don't.** Centre everything by default. Centred layouts have no structural
spine, and every element ends up equally weighted.

## Optical corrections

Mathematical alignment and visual alignment differ. The eye wins.

- A triangle in a circular play button sits 1 to 2px right of centre.
- Round shapes overshoot a flat baseline slightly, by roughly 1 to 2 percent of
  their size.
- Text inside a pill needs more horizontal padding than the maths suggests,
  because the round ends eat space.
- A capital letter beside an icon aligns on the cap height, not the box.

Each correction gets a comment, so a later reader does not "fix" it.

```css
.play-icon {
  /* Optical centring: the triangle's mass sits left of its bounding box */
  transform: translateX(1px);
}
```

## Touch and pointer spacing

Interactive targets are at least 24 by 24 CSS pixels, and at least 44 by 44 for
primary and touch. Adjacent targets need at least 8px between their hit areas so
a near miss does not trigger the wrong one.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Off-scale values such as 13px or 37px | Rhythm breaks, nothing aligns | Use the scale |
| Equal inner and outer spacing | Groups dissolve | Inner always smaller |
| Margins on children instead of gap | Collapsing and stray trailing space | `gap` on the parent |
| Centred everything | No spine, no hierarchy | Left aligned structure, centre for emphasis only |
| Fixed pixel heights on content containers | Text overflows at other sizes | `min-block-size` and let content grow |
| Filling empty space with decoration | Space was the point | Leave it |
| One breakpoint set copied between projects | Ignores this content's break points | Add breakpoints where the layout breaks |
