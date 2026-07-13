# Post Processing

Aspherix produces three distinct kinds of output during a run, and they serve different post-processing needs — pick the one(s) a case actually needs rather than defaulting to all of them.

- Per-timestep particle/mesh/interaction/Eulerian snapshots — `output_settings`
- Scalar time series — `status` / `status_style`
- Derived/aggregate quantities (residence time, massflow, mixing index, ...) — `calculate`, surfaced through one of the above

Plus two things the CLI invocation itself produces, not an `.asx` command — see `RUNNING.md`: the solver run log (wherever `-log filename` points) and solver warnings (`warnings_aspherix.txt` by default, override with `-warn filename`).

## Per-timestep field/particle output — `output_settings`

**Location:** `post/dump_particle_<step>.vtm` (and matching prefixes for other output kinds), plus an auto-generated ParaView index at `post/aspherix_simulation.pvd` — both under the case's working directory unless `output_settings folder ...`/`file ...` override it.

Writes per-particle, per-mesh, contact/bond-network, and Eulerian-field snapshots at each output interval (VTK/VTM by default).
This is the data source for spatial analysis and visualization — histograms of a per-particle property, contact-network inspection, animating the run, etc.
See `commands/output_settings.md` for the command itself, and `RUNNING.md` for visualizing the result in ParaView.
Because every particle property is written per timestep, arbitrary post-hoc analysis (e.g. building a diameter histogram) can be done afterwards from this data even when there's no dedicated in-run command for it — Aspherix has no native binning/histogram command, so that kind of derived analysis has to be built from the raw per-particle output rather than computed by the script.

## Scalar time series — `status` / `status_style`

**Location:** the `file` destination always writes to a fixed filename, `simulation_data_aspherix.csv`, with no override; the `terminal` destination goes to stdout or wherever `-log` points.

Writes scalar, whole-simulation values (particle count, kinetic energy, a `calculate` result, a custom variable, ...) at each status interval, to the terminal, log, and/or that CSV file.
This is the data source for tracking a single number over time — e.g. a fill fraction, a mesh's center of mass, a custom counter.
See `commands/status.md`.

Because the CSV filename has no override, if a workflow runs multiple variants/cases in the same working directory, later runs will overwrite an earlier run's CSV.
Isolate variants into separate run directories, or copy the CSV out immediately after each run, rather than assuming it's safe to leave in place.

## In-run derived/aggregate quantities — `calculate`

**Location:** nothing on its own — a `calculate` result only lands on disk once referenced by `status_style` or `output_settings` (below).

Computes a derived or spatially/temporally aggregated quantity during the run (residence time, massflow, mixing index, center of mass, min/max/average of a property, etc.) — see `RULES.md` for preferring `calculate` over the legacy `compute` command.
A `calculate` command's result is referenced elsewhere (a `variable` formula, a `status_style` column, `output_settings` particle properties) via its `id_` form — see `commands/variable.md` for that reference syntax.
Look up the specific `calculate` command needed on the public documentation (`DOC_SEARCH.md`) — the family is large and case-specific (residence time vs. massflow vs. mixing index are different commands, not modes of one command).

## Generating plots from the CSV

Once a run produces `simulation_data_aspherix.csv`, generate plots from it by default — the same default-on stance as `REPORTING.md` takes for reporting, and these plots are the kind of result that feeds into that report's "Where results go" section.
This only applies to the CSV time series; the per-timestep VTK/VTM output is visualized in ParaView instead (see `RUNNING.md`), not plotted.

- Defer to whatever data-visualization tooling is available rather than imposing one style — use a `dataviz`-style skill if the environment has one, or match the user's own charting conventions if they've stated any.
If the user gives explicit instructions on what to plot or how, follow those over any default here.
- Produce a standalone Python script that generates the plots, not just an inline/ephemeral analysis, so a human can rerun it later (e.g. after rerunning the simulation with different parameters) without an agent in the loop.
Only do this if Python is available in the environment — check first, same as checking for `aspherix` before running a case — and skip with a note if it isn't.
Follow `PYTHON.md` for how to run/install into whatever environment is already set up, rather than assuming a bare `python`/`pip`.
- The script should run standalone from the command line (e.g. `python plot_results.py`) using commonly available libraries (e.g. pandas/matplotlib), reading the CSV path as an argument or a sensible default next to it — it must not depend on an agent, a skill, or any tool only available inside this assistant.
- If the environment also supports generating a richer HTML artifact (e.g. via a `dataviz` skill), produce that in addition to the standalone script, not instead of it — the script is the reusable, agent-independent artifact; the HTML page is a nicer one-off view of the same data.

## Sequencing

`status_style` and `calculate` outputs are computed as the simulation runs, not derived afterwards — decide what needs to be tracked over time *before* running, since there's no way to reconstruct a missing time series from a completed run's other output.
Per-timestep field output (`output_settings`) is the exception: because it captures full per-particle/per-mesh state at each interval, it supports post-hoc analysis that wasn't explicitly anticipated, at the cost of more data being written (see `RULES.md` on being considerate with output intervals).
