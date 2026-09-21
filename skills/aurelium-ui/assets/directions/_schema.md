# Direction token schema

Every file in this folder except those starting with an underscore is a design
direction, consumed by `../../scripts/tokens.py` and validated in CI.

Colors are stored as **sRGB hex**. WCAG contrast is defined on sRGB relative
luminance, so hex is what can be checked exactly. Author the ramp perceptually
in `oklch()` if you prefer, then record the resulting hex here. `tokens.py` can
emit an `oklch()` layer behind `@supports` for engines that support it.

## Required keys

| Key | Type | Contents |
|---|---|---|
| `name` | string | The direction slug. Must match the filename |
| `label` | string | Human readable name |
| `colors` | object | Must contain `light` and `dark` |
| `fonts` | object | `display`, `body`, and optionally `mono` |
| `type` | object | Must contain `base` and `ratio` |
| `spacing` | object | Must contain `base` |
| `radii` | object | Named radius values |
| `shadows` | object | Elevation tokens, three levels at most |
| `borders` | object | Hairline width and per-theme colors |
| `motion` | object | Must contain `durations` and `easings` |
| `contrast_pairs` | array | Pairs to verify, see below |

## colors

`light` and `dark` each carry the same key set, so a theme switch never leaves a
token undefined.

| Token | Purpose |
|---|---|
| `page` | The page background |
| `surface` | A raised surface sitting on the page |
| `surface-raised` | The next level up, for overlays |
| `text` | Body text |
| `text-muted` | Secondary text. The pair that most often fails AA |
| `border` | Hairline color |
| `accent` | The single accent |
| `accent-hover` | Accent under pointer |
| `accent-fg` | Text or icon placed on the accent fill |
| `focus` | Focus indicator |
| `success`, `warning`, `danger`, `info` | Semantic colors, text safe |

Every value is a 6 digit hex string including the leading `#`.

## type

| Key | Type | Notes |
|---|---|---|
| `base` | number | Base size in px. Never below 16 for body |
| `ratio` | number | Modular scale ratio, above 1.0 |
| `steps` | string | Optional, default `-2..6` |

## spacing

| Key | Type | Notes |
|---|---|---|
| `base` | number | The grid unit in px. Always 4 |
| `multiplier` | number | Optional density multiplier, default 1.0 |

## motion

`durations` and `easings` are objects of named values.

```json
"motion": {
  "durations": { "fast": "120ms", "base": "200ms", "slow": "320ms" },
  "easings": {
    "standard": "cubic-bezier(0.2, 0, 0, 1)",
    "exit": "cubic-bezier(0.4, 0, 1, 1)"
  }
}
```

## contrast_pairs

Each entry names two color tokens and the theme to check them in. The validator
fails the build if any pair falls below its threshold.

```json
"contrast_pairs": [
  { "fg": "text", "bg": "page", "theme": "light", "min": 4.5 },
  { "fg": "accent-fg", "bg": "accent", "theme": "dark", "min": 4.5 }
]
```

| Field | Required | Notes |
|---|---|---|
| `fg` | yes | A token name from `colors.<theme>` |
| `bg` | yes | A token name from `colors.<theme>` |
| `theme` | yes | `light` or `dark` |
| `min` | no | Threshold, default 4.5. Use 3.0 for non text |

Every direction declares at minimum, in both themes:

- `text` on `page`
- `text` on `surface`
- `text-muted` on `page`
- `accent-fg` on `accent`
- `focus` on `page`, at 3.0

## Adding a direction

1. Copy an existing file and change the values.
2. Run `python ../../scripts/contrast.py --pair "#fg" "#bg"` while choosing
   colors, or check the whole file with the validator.
3. Run `python ../../../../tools/validate_skill.py ../../../` from this folder,
   or the repository form `python tools/validate_skill.py skills/`.
4. Write the matching Markdown file in `../../references/directions/`.
5. Add a row to the decision table in that folder's `index.md`.

A direction is a complete, coherent system, not a color swap. See
`../../../../CONTRIBUTING.md` for what a new direction must include.
