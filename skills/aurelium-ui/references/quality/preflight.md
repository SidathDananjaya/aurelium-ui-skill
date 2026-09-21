# Pre-flight

The authoritative gate. Nothing is done until every item here passes.

This is the single source for the pass or fail checks. The create workflow
points here rather than restating them, so there is one list to keep correct.

**Run each check. Never claim a check passed unless you ran it.** An unverified
claim is worse than an admitted gap, because it removes the user's chance to
catch it.

## How to use this

Work down the list. For each item, record `pass`, `fail`, or `n/a` with a
reason. Fix every failure before reporting. Anything that cannot be fixed is
reported as a known gap, named plainly.

## 1. Tokens

| # | Check | How |
|---|---|---|
| 1.1 | No hard-coded colour | Grep the output for hex, `rgb(`, and `hsl(` outside token definitions. Zero hits |
| 1.2 | No off-scale spacing | Grep padding, margin, and gap for pixel values. Every one resolves to a token |
| 1.3 | No raw durations | Grep for `ms` and `s` in transitions. Every one is a motion token |
| 1.4 | Radius from the scale | Every `border-radius` is a token, `0`, or a pill |
| 1.5 | At most three elevation levels | Count distinct shadow tokens in use |
| 1.6 | Two font families, plus mono | Count `font-family` declarations |

## 2. Contrast and colour

| # | Check | How |
|---|---|---|
| 2.1 | Every declared pair passes AA | Run `../../scripts/contrast.py --tokens tokens.css`. Exit code 0 |
| 2.2 | Body text at least 4.5:1 | Included in 2.1, and check any colour set outside tokens |
| 2.3 | Large text at least 3:1 | 24px regular or 18.66px bold and above |
| 2.4 | UI boundaries at least 3:1 | Borders that carry meaning, focus rings, chart series |
| 2.5 | No meaning by colour alone | Every semantic colour is paired with an icon, a word, or a pattern |
| 2.6 | Text over imagery verified | Sample the lightest pixel under the text. Still passes |

## 3. Hierarchy and layout

| # | Check | How |
|---|---|---|
| 3.1 | One primary action per view | Count elements using the primary button style. Exactly 1 |
| 3.2 | One focal point per view | Cover the fold. A stranger can name the most important thing |
| 3.3 | Inner spacing smaller than outer | For every group, largest inner gap is below smallest outer gap |
| 3.4 | Alignment holds | Edges line up across sections on one grid |
| 3.5 | Reading order is deliberate | Headline, then key figure or action, then supporting content |

## 4. States

| # | Check | How |
|---|---|---|
| 4.1 | Every data view ships every state | Render each one. See `../patterns/states.md` |
| 4.2 | Loading matches final dimensions | Skeleton height equals real content height. No shift |
| 4.3 | Two distinct empty states | First use and no results say different things |
| 4.4 | Errors name a fix | No message reads only "Something went wrong" |
| 4.5 | Input preserved on error | Submit a failing form. Nothing is cleared |
| 4.6 | Long content survives | Test a 120 character name, a 7 figure number, 40 items |

## 5. Keyboard and focus

| # | Check | How |
|---|---|---|
| 5.1 | Full keyboard operation | Unplug the mouse. Complete the primary task |
| 5.2 | Focus always visible | Tab every screen. Never invisible, never hidden by a sticky header |
| 5.3 | Tab order matches visual order | No positive `tabindex` |
| 5.4 | `Esc` closes every overlay | Open each one and press it |
| 5.5 | Focus trapped and returned | Modal traps while open, returns to its trigger on close |
| 5.6 | Skip link first | The first focusable element skips to main content |

## 6. Semantics

| # | Check | How |
|---|---|---|
| 6.1 | Correct elements | Actions are `button`, navigation is `a`. No `div` with a click handler |
| 6.2 | Heading order | One `h1`, no skipped levels. Disable CSS and read it |
| 6.3 | Every field has a visible label | A placeholder is not a label |
| 6.4 | Errors linked to fields | `aria-describedby`, and `aria-invalid` on the field |
| 6.5 | Icon-only buttons named | Every one has an accessible name |
| 6.6 | Images have correct alt | Meaningful described, decorative `alt=""`, none missing |
| 6.7 | `lang` set on `html` | Present and correct |

## 7. Targets

| # | Check | How |
|---|---|---|
| 7.1 | Minimum 24 by 24 | Measure the smallest interactive element. Inline text links exempt |
| 7.2 | Primary and touch 44 by 44 | Padding counts toward the target |
| 7.3 | Adjacent targets separated | At least 8px between hit areas |

## 8. Motion

| # | Check | How |
|---|---|---|
| 8.1 | Every animation has a purpose | State it in one sentence. No sentence means delete it |
| 8.2 | Only `transform` and `opacity` | Profile a frame. No layout or paint during animation |
| 8.3 | Reduced motion keeps meaning | Enable the setting. Every state change still reads |
| 8.4 | No infinite animation | Except a genuine spinner or a live status indicator |
| 8.5 | Interruptible | A second click reverses from the current position |

## 9. Responsive

| # | Check | How |
|---|---|---|
| 9.1 | Renders at 375, 768, 1024, 1440 | No horizontal scroll, no clipping, no overlap |
| 9.2 | Reflows at 320px | No loss of content or function |
| 9.3 | 200 percent zoom | At 1280px wide. Still usable |
| 9.4 | Touch targets on mobile | Primary actions reachable with one thumb |

## 10. Performance

| # | Check | How |
|---|---|---|
| 10.1 | LCP under 2.5s | Throttled mobile profile, not a fast desktop |
| 10.2 | INP under 200ms | Interact repeatedly while measuring |
| 10.3 | CLS under 0.1 | Watch for late banners, fonts, and images |
| 10.4 | Images have reserved dimensions | `width` and `height`, or `aspect-ratio` |
| 10.5 | Fonts do not shift on swap | Fallback metrics tuned |
| 10.6 | No console errors or warnings | Open the console. It is clean |

## 11. Content

| # | Check | How |
|---|---|---|
| 11.1 | No lorem ipsum | Every string is plausible real copy |
| 11.2 | Data is realistic | Real-looking names, amounts, dates. Not "Test User 1" |
| 11.3 | Buttons are verbs | Read each label out of context. The outcome is clear |
| 11.4 | No exclamation marks | Except at a genuine peak moment |
| 11.5 | Numbers formatted | Tabular figures, locale separators, currency stated |

## Reporting

Close with the output contract:

```
Direction   Obsidian, opulence 4, density 6, motion 3, theme auto
Files       tokens.css, index.html, dashboard.html, DESIGN.md
Pre-flight  Contrast 22/22 pass. One primary action per view. All states
            implemented. Keyboard and focus verified at 375 to 1440.
Gaps        10.1 to 10.3 not measured: no running build to profile.
            Offline state not implemented, the product has no offline mode.
```

A gap named is a professional handoff. A gap hidden is a defect you shipped.
A check claimed but not run is worse than either.
