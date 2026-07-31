# Running Aspherix

How to invoke the `aspherix` CLI binary itself, as opposed to writing `.asx` input script content (see `commands/` and `RULES.md` for that).

## Environment

Running the executable depends on having the Aspherix environment correctly set up.
The `aspherix` executable MUST be available in your PATH.

You can check if it is available with the following shell command:
```
which aspherix
```

> NOTE: It is recommended that the Aspherix environment already be preloaded — and NOT (re-)loaded each time a simulation is run.

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

A complete list of command-line options is at `https://doc.aspherix-dem.com/solver/Section_commandline.html` in the Aspherix Solver documentation (see `DOC_SEARCH.md`).

## Running a simulation and reading its log

Be careful when running an input script and then reading its log file — a full simulation run, or a verbose/long-running one, can produce a very long log.
Reading the whole thing into context will pollute it.

- Run the simulation in the background, or with a bounded number of timesteps/short duration first, rather than a full production run, when just checking that a script works.
- When checking output, prefer `tail`, `grep`, or piping through a filter over reading the whole log file — e.g. check the last N lines for the final status, or grep for `ERROR`/`WARN`.
- Set `-log filename` (rather than leaving it on screen/stdout) so the log can be searched/filtered on disk instead of scrolling through captured terminal output.

## Concurrent runs

Never start a second `aspherix` process against a case directory that already has a run in progress.
Aspherix's own output files — notably `simulation_data_aspherix.csv` (see `POST_PROCESSING.md`) — are not safe for concurrent writers and can be corrupted, forcing a full re-run to recover.
If you need to test or iterate on something small while a longer run is still going, do it in a separate scratch/case-copy directory rather than the one the active run is using.

## GPU execution

Aspherix can run on GPU via a command-line flag (see the CLI's own `-help` / documented command-line options for the exact current flag name and any architecture-selection options).

## Visualizing results

Aspherix results are written to ParaView `.pvd` files.
To visualize the results a working version of ParaView is required, and the Aspherix macros must be installed (bundled with the Aspherix installer).

```
paraview --data=path/to/results.pvd
```

Launching the macro automatically via a `--script` flag is currently unreliable — don't pass `--script`.
Instead, launch ParaView with `--data` as above, then tell the user to run the Aspherix macro themselves from the Macros menu once ParaView is open.

ParaView macros are commonly installed in `~/.config/ParaView/Macros/`.
