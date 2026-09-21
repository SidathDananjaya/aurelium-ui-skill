# CLAUDE.md

Instructions for AI coding agents working on **this repository**. This is not the skill itself. The skill lives in `skills/aurelium-ui/`.

Read this file completely before making any change.

## Project identity (confirmed, do not change)

| Item | Value |
|---|---|
| Product name | Aurelium UI |
| Tagline | Helping AI coding agents build polished, accessible, production-ready interfaces. |
| GitHub repository | `aurelium-ui-skill` |
| GitHub owner | `SidathDananjaya` |
| Skill folder and `name` field | `aurelium-ui` (folder `skills/aurelium-ui/`, must match frontmatter `name`) |
| Default branch | `main` |
| License | MIT |
| Author (LICENSE) | Sidath Mendis |
| Author (`metadata.author`) | SidathDananjaya |

The repository name ends in `-skill` so people recognize what it is on GitHub. The skill name inside stays short because agents display it and users type it.

## Environment (confirmed in Phase 0)

| Item | Value |
|---|---|
| Operating system | Windows 11 Pro |
| Shells | PowerShell and Git Bash |
| **Python command** | **`python`** (3.13.5). `py` also works. `python3` is **not** available on this machine. |
| Git | 2.52.0 |
| GitHub CLI | `gh`, installed at `C:\Program Files\GitHub CLI\gh.exe`, authenticated as `SidathDananjaya` |

Run the tests with:

```
python -m unittest discover -s tests
```

Run the validator with:

```
python tools/validate_skill.py skills/
```

On macOS and Linux these become `python3`. Any documentation written for a general audience should say `python3` and note the Windows equivalent.

## Planning document

The implementation plan for this project is kept **locally only, at `IMPLEMENTATION_PLAN.md` in the repository root**. It is listed in `.gitignore` and is deliberately never committed or pushed. Do not add it, reference it from any committed file, or copy its contents into the repository.

Because contributors cloning this repository will not have it, every committed file must stand on its own. This file is the durable record of the rules that matter.

## Git ownership rule (important)

**The human runs every Git and GitHub command. The agent never runs them.**

- The agent **must not** run `git add`, `git commit`, `git push`, `git checkout`, `git merge`, `git tag`, `git reset`, `git rebase`, `git stash`, or any `gh` command that changes state.
- The agent **may** run read-only commands to verify state: `git status`, `git diff`, `git log --oneline`, `git branch`.
- At every commit point the agent stops editing, prints the exact commands in one code block, and waits for the human to reply `done` or paste errors.
- If the human pastes an error, the agent explains it in plain language and gives the exact fix commands.

## Command format the agent must use

Commands must work in Windows Command Prompt, PowerShell, and macOS or Linux terminals:

- One command per line. No `&&` chains, no backslash line continuations, no heredocs.
- Use **double quotes** for commit messages and titles. Never single quotes, because Command Prompt does not treat them as quotes.
- Always `git add` **explicit file or folder paths**. Never `git add .` or `git add -A`.

**Phase start**, printed before changing any file in a new phase:

```
git checkout main
git pull origin main
git checkout -b phase/NN-short-name
```

**Commit point**, one block per commit. The agent runs `git status` itself first, read-only, so the paths it lists are correct and complete:

```
git status
git add path/to/file-or-folder path/to/other-file
git commit -m "type(scope): short description"
```

**Phase close-out**, printed after the final commit of a phase and after acceptance checks pass:

```
git push -u origin phase/NN-short-name
gh pr create --base main --head phase/NN-short-name --title "Phase NN: Phase name" --body "Implements Phase NN. See the changelog for notes."
gh pr checks --watch
gh pr merge --merge --delete-branch
git checkout main
git pull origin main
```

Use `--merge` rather than `--squash` so each Conventional Commit is preserved in history. If checks fail, do not merge. Diagnose, fix, and print a new commit block plus `git push`.

## Working rules

1. Work on **one phase at a time**, in order.
2. At the start of a phase, restate the goal and list the files to be created or changed.
3. At the end of a phase, run every acceptance check. If one fails, fix it before moving on.
4. Update `CHANGELOG.md` under `## [Unreleased]` before the close-out commit.
5. At every checkpoint, stop and summarize what was done, what was decided, and what is open. Wait for human approval before continuing.
6. **Never copy code, text, or images from third-party websites, award galleries, design systems, or other skills.** Encode principles and patterns in your own words. Credit sources in `CREDITS.md` with a link, not a long quotation.
7. If something is ambiguous, state the assumption in the phase summary rather than silently choosing.
8. **Keep `SKILL.md` under 500 lines.** Target under 250. Detail belongs in `references/`, which load on demand.

## Content standards

- **Every rule must be checkable.** Write "minimum 4.5:1 contrast for body text", not "make it readable".
- **Scripts use the Python standard library only.** Python 3.9 or newer, no third-party packages, no network access. Use `pathlib` and open files with `encoding="utf-8"`. Every script supports `--help`, offers `--json` output, and exits non-zero on check failure.
- **Fonts must be under the SIL Open Font License** and available on Google Fonts. Verify each license before listing it.
- **Avoid em-dashes in skill instruction text.** Use periods, commas, or colons. Agents copy the style of their instructions into the copy they write.
- **Tone of skill files** is imperative, specific, and testable.

## Agent Skills spec constraints

- A skill is a folder containing `SKILL.md`, plus optional `scripts/`, `references/`, `assets/`.
- `SKILL.md` starts with YAML frontmatter, then Markdown instructions. The file must be named exactly `SKILL.md`.
- `name`: required, 1 to 64 characters, lowercase letters, digits, and hyphens only, no leading or trailing hyphen, no consecutive hyphens, and it **must match the folder name**.
- `description`: required, 1 to 1024 characters, must state what the skill does **and when to use it**. This field controls triggering, so include concrete trigger words.
- Optional fields: `license`, `compatibility` (max 500 characters), `metadata` (key and value pairs).
- **No angle brackets** (`<` or `>`) anywhere in frontmatter.
- The full `SKILL.md` loads when the skill activates. Reference files load on demand, so keep each one focused.
