# Data display

Figures, KPIs, and charts. The job is comprehension, not decoration. A chart
that looks impressive and answers nothing has failed.

## KPI tiles

A KPI answers one question. Three to five per view, never a wall of twelve.

| Part | Rule |
|---|---|
| Label | What this measures, plain words, muted |
| Value | The figure, largest element, tabular figures |
| Unit | Attached to the value, never assumed |
| Change | Direction plus magnitude, with a glyph and a word |
| Context | Against what, over what period |

A number with no comparison is trivia. "1,240" means nothing. "1,240 bookings,
up 8 percent on last month" means something.

```html
<article class="kpi">
  <h3 class="kpi-label">Bookings this month</h3>
  <p class="kpi-value">1,240</p>
  <p class="kpi-change" data-direction="up">
    <span aria-hidden="true">&#9650;</span>
    Up 8% on last month
  </p>
</article>
```

```css
.kpi {
  display: grid;
  gap: var(--space-2);
  padding: var(--space-5);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
}

.kpi-label {
  margin: 0;
  font-size: var(--text-xs);
  font-weight: 500;
  color: var(--color-text-muted);
}

.kpi-value {
  margin: 0;
  font-size: var(--text-3xl);
  line-height: var(--leading-3xl);
  letter-spacing: var(--tracking-3xl);
  font-variant-numeric: tabular-nums lining-nums;
}

.kpi-change {
  margin: 0;
  font-size: var(--text-xs);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.kpi-change[data-direction="up"] { color: var(--color-success); }
.kpi-change[data-direction="down"] { color: var(--color-danger); }
```

The glyph plus the word "Up" carries the meaning. The colour is reinforcement,
never the signal itself.

**Up is not always good.** Rising churn, latency, or error rate is bad. Colour
by whether the change is good, not by its direction, and be consistent about it.

## Choosing a chart

| Question | Chart |
|---|---|
| How has this changed over time? | Line |
| How do a few categories compare? | Horizontal bar |
| How does a total break down over time? | Stacked area or stacked bar |
| How do two variables relate? | Scatter |
| What is the distribution? | Histogram or box plot |
| What proportion of a whole? | Bar, almost always |

Pie and donut charts are readable for two or three segments at most. Beyond
that a bar chart is better at the only task a pie has. A donut with eight
slices and a legend is a table that lost its labels.

Never use a 3D chart. The perspective distorts the values, which is the one
thing a chart must not do.

## Chart rules

- **Bar charts start at zero.** Truncating the axis exaggerates differences and
  is misleading rather than clever.
- Line charts may use a non-zero baseline, but say so on the axis.
- Label the series directly at the line end rather than using a legend. A
  legend makes the eye travel back and forth.
- Annotate what matters: the peak, the anomaly, the target line. An annotation
  is worth more than a colour scheme.
- Sort bars by value unless the category has a natural order such as time.
- Show the data density you have. Do not smooth a line until it implies
  measurements you never took.

## Colour in charts

- Use one accent for a single series. Do not rainbow a single-series chart.
- For multiple series, vary lightness within a hue before adding hues.
- Never encode meaning in colour alone. Add a direct label, a pattern, or a
  shape.
- Check every series colour against the background and against its neighbours.
- Semantic colours keep their semantic meaning inside charts. Red is a problem,
  not just the third series.

## Accessibility

A chart is an image of data. The data must also exist as text.

```html
<figure>
  <div class="chart" role="img" aria-labelledby="chart-title chart-desc"></div>
  <figcaption id="chart-title">Bookings by month, 2026</figcaption>
  <p id="chart-desc" class="visually-hidden">
    Bookings rose from 840 in January to 1,240 in March, with a dip to 790 in
    February.
  </p>
  <details>
    <summary>View as table</summary>
    <table><!-- the same figures --></table>
  </details>
</figure>
```

The `details` table is the most reliable accommodation, and it helps sighted
users who want exact values too.

## Figures everywhere

Every figure that changes in place, aligns in a column, or sits beside another
figure uses tabular lining numerals. Without it, a live-updating value visibly
wobbles.

Format for the locale, state the currency and unit, and round to a sensible
precision. "99.99998% uptime" should read "99.99%".

## Sparklines

A sparkline shows shape, not value. Give it a current value beside it in text,
and no axes. If the user needs to read a value off it, it should be a chart.

## Empty and loading

- **Loading**: a skeleton with the chart's real dimensions. A collapsing chart
  area causes layout shift.
- **Empty**: explain why there is no data and what would produce some. Never
  render empty axes with no explanation.
- **Partial**: render what you have and mark the gap. Never interpolate across
  missing data silently, which invents readings.

## Anti-patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Truncated bar chart axis | Exaggerates differences, misleads | Start at zero |
| 3D charts | Perspective distorts values | Flat |
| Pie chart with many slices | Unreadable, needs a legend | Horizontal bar |
| Rainbow palette on one series | Colour implies difference that is not there | One accent |
| Legend instead of direct labels | Eye travels back and forth | Label at the line end |
| Colour as the only encoding | Excludes many users | Add labels or patterns |
| A figure with no comparison | Trivia, not insight | Give it context |
| Proportional figures in a KPI | Value wobbles as it updates | `tabular-nums` |
| Green for every increase | Rising churn is not good news | Colour by good or bad |
| Smoothing over missing data | Invents measurements | Show the gap |
