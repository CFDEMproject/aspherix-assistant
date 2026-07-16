# Aspherix Assistant

A [Claude Code](https://claude.com/claude-code) skill that helps with the setup of [Aspherix®](https://www.aspherix-dem.com/) DEM (Discrete Element Method) simulations.

It steers Claude toward Aspherix's native declarative command syntax, points it at the public Aspherix documentation, and packages command- and strategy-specific guidance that's tedious to look up by hand.

## Install

This skill follows the [Agent Skills](https://agentskills.io) open standard, so the same `SKILL.md` works across Claude Code, Cursor, Gemini CLI, and Google Antigravity — only the install directory differs per tool.
See [`INSTALLATION.md`](INSTALLATION.md) for exact per-tool install paths and methods.

## What's in here

- `SKILL.md` — the skill definition: context, links to the public Aspherix [docs](https://doc.aspherix-dem.com/), and pointers into `references/`.
- `references/RULES.md` — the single source of truth for rules every Aspherix case must follow.
- `references/RUNNING.md` — how to invoke the `aspherix` CLI binary itself.
- `references/commands/<name>.md` — per-command guidance (styles, syntax, examples, preferred usage) for commands worth documenting beyond the public docs, one file per command.
- `references/strategies/STRATEGIES.md` — short problem-solving strategies for building and debugging cases; larger ones get their own `references/strategies/<name>.md` file.

See `CLAUDE.md` for the conventions used when extending this repo.

## Trademarks

"Aspherix" and "Aspherix®" are trademarks of DCS Computing GmbH, Linz.
This is documentation/tooling that references the public Aspherix documentation; it is not the Aspherix software itself. See `LICENSE` for details.

## License

MIT — see `LICENSE`.
