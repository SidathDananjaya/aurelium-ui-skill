# Credits

Aurelium UI encodes widely published principles from user experience research, accessibility standards, and typographic practice. Everything in this repository is written in our own words. Nothing is copied from the sources below.

Listing a source here is attribution, not a claim of endorsement, affiliation, or partnership.

## Standards

| Source | Used for |
|---|---|
| [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/), W3C | Contrast ratios, target sizes, focus visibility, keyboard operation, reflow |
| [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/), W3C | Component roles, keyboard interaction patterns, focus management |
| [Core Web Vitals](https://web.dev/articles/vitals), Google | Performance budget thresholds for LCP, INP, and CLS |

## User experience literature

| Source | Used for |
|---|---|
| Jakob Nielsen, "10 Usability Heuristics for User Interface Design", Nielsen Norman Group | The heuristics encoded in `references/doctrine/heuristics.md`. Each is restated as one implementable rule and one binary check |
| Fitts's law, Hick's law, Jakob's law, Miller's law, Tesler's law, Doherty threshold, Von Restorff effect, serial position effect, peak-end rule, aesthetic-usability effect | The application rules in `references/doctrine/ux-laws.md` |
| Jon Postel, the robustness principle, from RFC 761 and RFC 1122 | Applied to form input handling in `references/doctrine/ux-laws.md`. The original concerns network protocol implementations, not user interfaces. The application to input parsing is ours |
| Gestalt principles of grouping (proximity, similarity, common region) | Grouping and spacing rules in `references/doctrine/ux-laws.md` and the foundations |
| Daniel Kahneman and Barbara Fredrickson, research on the peak-end rule | The rule that flows invest at their peak and their ending |

## Typography and color

| Source | Used for |
|---|---|
| Established typographic practice on measure, line height, and tracking | `references/foundations/typography.md` |
| [Google Fonts](https://fonts.google.com/) | Font availability. Only SIL Open Font License faces are recommended, and each license is verified before listing |

## Scoring rubric

The weighting in `references/quality/rubric.md` is informed by publicly described judging criteria for web design awards, which commonly weigh design, usability, creativity, and content. Aurelium UI is independent and is not affiliated with, endorsed by, or connected to any awards organization.

## Fonts

All fonts recommended by this skill are distributed under the SIL Open Font License, Version 1.1. Their copyright and license terms belong to their respective authors and foundries. Aurelium UI does not bundle or redistribute font files. It only names fonts and points to where they are published.

### Verification method

The list in `references/foundations/typography.md` was verified on 21 September 2026 against the [google/fonts](https://github.com/google/fonts) repository, which classifies families by directory: `ofl/` for the SIL Open Font License, `apache/` for Apache 2.0, and `ufl/` for the Ubuntu Font License. Each family was confirmed present under `ofl/` with its own `OFL.txt`, and a sample of those files was read to confirm the text is the SIL Open Font License Version 1.1 rather than a directory convention alone.

Twelve families were verified: Cormorant Garamond, Instrument Serif, Newsreader, Fraunces, Hanken Grotesk, Manrope, Figtree, Schibsted Grotesk, Geist, Space Grotesk, IBM Plex Mono, and JetBrains Mono.

Re-verify before adding any family to that list. A font being free to use on a webfont host does not make it OFL.

## Corrections

If you believe something here is miscredited or a source is missing, please open an issue.
