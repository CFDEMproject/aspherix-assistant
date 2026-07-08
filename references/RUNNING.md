# Running Aspherix

How to invoke the `aspherix` CLI binary itself, as opposed to writing `.asx` input script content (see `commands/` and `RULES.md` for that).

## Basic usage

```
aspherix -in input.asx
```

Runs `input.asx`.

## Key flags

- `-help` — print help message and quit.
- `-version` — print version and quit.
- `-in filename` (`-i`) — input script to run.
- `-var varname value` (`-v`) — set an index-style variable, readable in the script.
- `-echo none/screen/log/both` (`-e`) — echo the input script.
- `-log none/filename` (`-l`) — log destination.
- `-status filename` — where to write status output.
- `-warn none/filename` (`-w`) — warnings destination.

A complete list of command-line options is in the Aspherix documentation under "Aspherix Solver -> Getting Started -> Command-line options".

## Running a simulation and reading its log

Be careful when running an input script and then reading its log file — a full simulation run, or a verbose/long-running one, can produce a very long log.
Reading the whole thing into context will pollute it.

- Run the simulation in the background, or with a bounded number of timesteps/short duration first, rather than a full production run, when just checking that a script works.
- When checking output, prefer `tail`, `grep`, or piping through a filter over reading the whole log file — e.g. check the last N lines for the final status, or grep for `ERROR`/`WARN`.
- Set `-log filename` (rather than leaving it on screen/stdout) so the log can be searched/filtered on disk instead of scrolling through captured terminal output.
