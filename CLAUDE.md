# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This repo defines a Claude Code **skill** named "Aspherix Assistant" — it is not an application with source code, build steps, or tests. It helps with the setup of Aspherix(R) DEM (Discrete Element Method) simulations.

- `SKILL.md` — the skill definition (frontmatter + instructions loaded when the skill is invoked). Points to the public Aspherix documentation at https://doc.aspherix-dem.com/ (see also the genindex at `/genindex.html`).
- `references/RULES.md` — the single source of truth for rule *content* that applies to every simulation case under `workspaces/cases/`. Other files (e.g. an `INSTRUCTIONS.md` used while building a case, and an `AUDIT.md` used to check a completed build) describe *when*/*how* each rule is applied, but the rule text itself must live only in `references/RULES.md` — don't fork rule content into multiple places.

## Working in this repo

- When adding or changing a rule that Aspherix cases must follow, edit `references/RULES.md` directly rather than duplicating rule text elsewhere.
- Current rules (see `references/RULES.md` for the authoritative list):
  - No legacy LIGGGHTS-style `fix <id> <group-id> <style> ...` commands anywhere. Use Aspherix's native declarative commands instead (e.g. mesh motion must use `mesh_module motion` with styles like `linear`, `rotate`, `wiggle`, not `fix <id> <group> move/mesh ...`).
