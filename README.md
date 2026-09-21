# Aurelium UI

> Helping AI coding agents build polished, accessible, production-ready interfaces.

**Status: work in progress.** This repository is being built phase by phase and is not yet ready to install.

## What it is

Aurelium UI is an open-source [Agent Skill](https://code.claude.com/docs/en/skills) that turns a coding agent into a senior product designer and design engineer with a luxury sensibility. It works in two modes:

- **Create**: design and implement a new web app UI with a coherent, premium design system.
- **Audit and Elevate**: review an existing UI against a scored rubric, then upgrade it.

Luxury in software is the absence of friction and the presence of care. Aurelium encodes that as five qualities, in priority order: clarity, restraint, precision, material quality, and effortlessness.

## What it is not

- Not a component library or npm UI kit.
- Not tied to one framework. Default output is HTML and CSS, with recipes for Tailwind, React, and Next.js.
- No image generation, no paid tier.

## Installation

Not yet available. Install instructions land with the v0.1.0 release.

## Repository layout

| Path | Contents |
|---|---|
| `skills/aurelium-ui/` | The skill itself: `SKILL.md`, workflows, references, assets, scripts |
| `tools/` | Repository tooling, including the skill validator used in CI |
| `tests/` | Python `unittest` suites for scripts and tools |
| `evals/` | Evaluation protocol, prompts, and before/after results |
| `gallery/` | Static showcase site built with the skill |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributors and agents working on this repository should read [CLAUDE.md](CLAUDE.md) first.

## License

MIT. See [LICENSE](LICENSE). Sources and influences are credited in [CREDITS.md](CREDITS.md).
