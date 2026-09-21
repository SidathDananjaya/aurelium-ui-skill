# Choosing a design direction

A direction is a complete, coherent system: palette, type, rhythm, depth, and
motion character. Pick one and commit to it. Mixing two directions produces the
incoherence that separates amateur work from considered work.

The user may name a direction. If they do, use it. Otherwise infer one from the
brief, state the choice in one sentence with a reason, and proceed.

## The five directions

| Direction | Mood | Accent | Radius | Motion | Best for |
|---|---|---|---|---|---|
| [Quiet Luxury](quiet-luxury.md) | Editorial, calm, warm | Bronze | 2 to 6px | Slow, soft | Hospitality, fashion, real estate, wellness, portfolios |
| [Obsidian](obsidian.md) | Dark, rich, confident | Champagne | 8 to 12px | Precise, damped | Fintech, premium SaaS, automotive, watches, music |
| [Tactile Craft](tactile-craft.md) | Tactile, crafted, human | Terracotta | 12 to 20px | Physical, weighted | Consumer apps, booking, food, lifestyle, e-commerce |
| [Swiss Precision](swiss-precision.md) | Rational, sharp | Signal red | 0 to 2px | Minimal, fast | Dev tools, analytics, agencies, architecture |
| [Functional Futurism](functional-futurism.md) | Precise, technical, cinematic | Live teal | 0 to 4px | Telemetric | AI, aerospace, security, energy, mission control |

## Decision table by archetype

| The user is building | Start with | Because |
|---|---|---|
| Hotel, restaurant, spa, resort | Quiet Luxury | Warmth and editorial calm sell hospitality |
| Fashion, jewellery, beauty | Quiet Luxury | Space and serif display carry the product |
| Real estate, architecture | Quiet Luxury or Swiss Precision | Editorial for lifestyle, Swiss for technical |
| Banking, investing, payments | Obsidian | Dark surfaces and restraint read as trustworthy |
| Premium B2B SaaS | Obsidian | Confident without shouting |
| Watches, automotive, audio | Obsidian | Material richness suits the category |
| E-commerce, marketplace | Tactile Craft | Soft radii and warmth invite browsing |
| Booking, travel, events | Tactile Craft | Human tone reduces transaction anxiety |
| Food, wellness, lifestyle | Tactile Craft | Natural palette, approachable |
| Developer tools, APIs | Swiss Precision | Density and mono type match the audience |
| Analytics, BI, reporting | Swiss Precision | Grid discipline serves dense data |
| Agency, studio, portfolio | Swiss Precision or Quiet Luxury | Swiss for rigour, Quiet for craft |
| AI products, model tooling | Functional Futurism | Technical without the purple gradient cliche |
| Security, observability, infrastructure | Functional Futurism | Live state reads as instrumentation |
| Aerospace, energy, logistics, fleet | Functional Futurism | Mission control is the native idiom |
| Editorial, publishing, docs | Quiet Luxury | Reading typography is the product |

## Decision table by brand mood

| The brief says | Direction |
|---|---|
| Timeless, understated, refined, heritage | Quiet Luxury |
| Premium, exclusive, sophisticated, dark | Obsidian |
| Warm, handmade, approachable, honest | Tactile Craft |
| Clear, rigorous, no nonsense, systematic | Swiss Precision |
| Advanced, precise, powerful, real time | Functional Futurism |

## When two directions both fit

Ask which matters more, then choose:

| Tension | Resolution |
|---|---|
| Warmth versus authority | Warmth to Tactile Craft, authority to Obsidian |
| Density versus calm | Density to Swiss Precision, calm to Quiet Luxury |
| Technical versus human | Technical to Functional Futurism, human to Tactile Craft |
| Editorial versus product | Editorial to Quiet Luxury, product to Obsidian |

## What not to do

- **Do not blend two directions.** Borrowing Obsidian's palette with Tactile
  Craft's radii produces neither.
- **Do not change direction between screens** of one product.
- **Do not pick Functional Futurism by default** because it looks the most
  distinctive. It is wrong for content-heavy reading experiences.
- **Do not pick a direction before reading the brief.** The archetype and the
  audience decide it, not preference.

## Generating the tokens

Once chosen, generate the token set rather than hand-writing values:

```
python scripts/tokens.py --direction obsidian --opulence 4 --density 5 --motion 4 --theme auto --format css
```

Then verify before shipping:

```
python scripts/contrast.py --tokens tokens.css
```

Every direction ships with both themes, and every declared contrast pair passes
WCAG AA in both. That is enforced in CI, not left to inspection.
