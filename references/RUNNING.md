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
