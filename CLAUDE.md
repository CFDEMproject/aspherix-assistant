# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This repo defines a Claude Code **skill** named "Aspherix Assistant" — it is not an application with source code, build steps, or tests. It helps with the setup of Aspherix(R) DEM (Discrete Element Method) simulations.

- `SKILL.md` — the skill definition (frontmatter + instructions loaded when the skill is invoked). Points to the public Aspherix documentation at https://doc.aspherix-dem.com/ (see also the genindex at `/genindex.html`).
- `references/RULES.md` — the single source of truth for rule *content* that applies to every simulation case under `workspaces/cases/`. Other files (e.g. an `INSTRUCTIONS.md` used while building a case, and an `AUDIT.md` used to check a completed build) describe *when*/*how* each rule is applied, but the rule text itself must live only in `references/RULES.md` — don't fork rule content into multiple places.
- `references/commands/<name>.md` — per-command guidance (e.g. `references/commands/variable.md`), one file per Aspherix command, named after the command itself. Use for *how*/*when* to use a specific command (styles, syntax, examples); general cross-command rules still belong only in `references/RULES.md`.
- `references/strategies/STRATEGIES.md` — short, self-contained problem-solving strategies (a few sentences each). A strategy that needs its own examples or multi-step walkthrough gets its own `references/strategies/<name>.md` file, linked from `STRATEGIES.md`.

## Commit messages

Every commit made by an AI agent must end with a `Co-Authored-By:` trailer naming the specific model that wrote it (e.g. `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`), not a generic tool name.
This repo relies on that trailer to audit which model authored which change, so use the exact model name/version, and never omit or genericize it.

## Working in this repo

- When adding or changing a rule that Aspherix cases must follow, edit `references/RULES.md` directly rather than duplicating rule text elsewhere.
- When adding guidance specific to one Aspherix command, put it in its own `references/commands/<name>.md` file and link it from `SKILL.md`'s Guidelines section, rather than growing `references/RULES.md` or `SKILL.md` itself.
- When adding a problem-solving strategy: a short one goes directly in `references/strategies/STRATEGIES.md`; a strategy that needs its own examples or walkthrough gets its own `references/strategies/<name>.md` file, linked from `STRATEGIES.md`.
- Current rules (see `references/RULES.md` for the authoritative list):
  - No legacy LIGGGHTS-style `fix <id> <group-id> <style> ...` commands anywhere. Use Aspherix's native declarative commands instead (e.g. mesh motion must use `mesh_module motion` with styles like `linear`, `rotate`, `wiggle`, not `fix <id> <group> move/mesh ...`).
