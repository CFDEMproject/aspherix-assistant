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
- `enable_cfd_coupling` command usage: `references/commands/enable_cfd_coupling.md`
- `primitive_wall` command usage: `references/commands/primitive_wall.md`

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

## Calibration

Aspherix Calibration (`aspherix-calibration`, licensed separately) finds DEM material parameters that reproduce lab tests of a bulk material; for calibration work, use the sibling skill [Aspherix Calibration Assistant](https://github.com/CFDEMproject/aspherix-calibration-assistant).
That skill may not be installed or accessible for every user; if it isn't available, say so, and help with what this skill covers — e.g. a manual parameter study with plain `.asx` cases compared against the user's measurements, which is not a calibration.
Example material models for several material classes, usable as starting points before a calibration, are collected in the DCS knowledge base (`https://support.aspherix.org/support/solutions/articles/201000124214`); they are example values, not tailored to a specific real material.

## Post Processing

See `references/POST_PROCESSING.md`

## Reporting

See `references/REPORTING.md`
