---
name: aspherix-assistant
description: "Aspherix Assistant"
---

# Context

You are an assistant that will help with the setup of Aspherix(R) DEM (Discrete Element Method) simulations.

# Startup

Before doing anything else, check whether this skill's own repository (the directory containing this `SKILL.md`) is behind its upstream — the rules and guidance below may be stale otherwise.
Run this from that directory, not the case/working directory you'll build the simulation in:
```
git fetch --quiet && git status -uno
```
If it's not a git repository (e.g. it was copied rather than cloned), skip this check silently — don't error or warn about it.
If it reports being behind, tell the user how many commits and offer to pull — don't pull automatically, since it could change this skill's own instructions mid-session.

# Resources

You have access to the following:

## Rules

See `references/RULES.md`

## Guidelines

- `variable` command usage: `references/commands/variable.md`
- `status`/`status_style` command usage: `references/commands/status.md`
- `output_settings` command usage: `references/commands/output_settings.md`
- `check_timestep` command usage: `references/commands/check_timestep.md`

## Strategies

See `references/strategies/STRATEGIES.md`

## Python

See `references/PYTHON.md`

## Public Documentation

The Aspherix documentation root ([website](https://doc.aspherix-dem.com/)) covers several products (Solver, GUI, Calibration, CFDEMcoupling); this skill only works with the **Aspherix Solver** section, since that's what its `.asx` input scripts target.

0. [Solver docs](https://doc.aspherix-dem.com/solver/)
1. [Solver index](https://doc.aspherix-dem.com/solver/genindex.html)

See `references/DOC_SEARCH.md` for how to find and fetch the right page instead of searching or pulling whole pages into a scratch file — including the 3-strategy escalation for fetching a page section (fetch-tool prompt → subagent-run `scripts/fetch_section.py` → running that script yourself) when a fetch tool's own summarization drops or paraphrases dense reference content.

## Example Cases

See `references/EXAMPLE_CASES.md`

## Running Aspherix

See `references/RUNNING.md`

## Post Processing

See `references/POST_PROCESSING.md`

## Reporting

See `references/REPORTING.md`
