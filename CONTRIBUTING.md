# Contributing to Aurelium UI

Thanks for your interest. This guide covers how to propose changes and what the quality bar is.

## Ground rules

1. **Never copy third-party content.** Do not paste code, prose, or images from other skills, design systems, award galleries, or agency sites. Encode principles and patterns in your own words. Credit sources in `CREDITS.md` with a link, not a long quotation.
2. **Every rule must be checkable.** Write "minimum 4.5:1 contrast for body text", not "make it readable". If a reviewer cannot verify a rule mechanically or by direct inspection, rewrite it.
3. **Fonts must be openly licensed.** Only recommend fonts under the SIL Open Font License that are available on Google Fonts. Verify the license before adding one to a list.
4. **Scripts use the Python standard library only.** Python 3.9 or newer. No third-party packages, no network access, no installs.
5. **`SKILL.md` stays under 500 lines.** Detail belongs in `references/`, which load on demand.
6. **Avoid em-dashes in skill instruction text.** Use periods, commas, or colons. Agents copy the style of their instructions into the interfaces they write.

## Development setup

No dependencies to install. You need Git and Python 3.9 or newer.

Run the test suite:

```
python -m unittest discover -s tests
```

Run the skill validator:

```
python tools/validate_skill.py skills/
```

On macOS and Linux, use `python3` instead of `python`.

## Branches and commits

- One branch per unit of work, named `phase/NN-short-name` or `fix/short-name`.
- Commits follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/): `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`, `ci:`. Breaking changes use `feat!:`.
- Scope the type where it helps: `feat(directions):`, `test(scripts):`.
- Stage explicit paths. Do not use `git add .` or `git add -A`.

## Pull requests

- Base every pull request on `main`.
- Fill in the pull request template.
- CI must be green before merge: unit tests and the skill validator both pass.
- Merge with a merge commit rather than a squash, so each Conventional Commit is preserved in history.

## Adding a design direction

A direction is a complete, coherent system, not a color swap. It needs:

- `skills/aurelium-ui/assets/directions/<name>.json` with every required token key.
- `skills/aurelium-ui/references/directions/<name>.md` covering philosophy, tokens, type scale, spacing, radius, elevation, motion, signature details, component notes, a do and don't list, and an example screen.
- Every declared contrast pair passing WCAG AA.
- A row in the decision table in `references/directions/index.md`.

## Adding an archetype

`skills/aurelium-ui/references/archetypes/<name>.md`, under 200 lines, covering user goals, primary tasks, information architecture, key screens, critical states, luxury moments, pitfalls, and recommended directions and dials. Link to the relevant component and pattern files rather than repeating them.

## Reporting issues

Use the issue templates. For a UI quality problem, include the prompt used, the agent and model, the skill version, and a screenshot.

## License

By contributing, you agree that your contributions are licensed under the MIT License.
