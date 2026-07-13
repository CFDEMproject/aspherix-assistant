# Post Processing

Aspherix produces three distinct kinds of output during a run, and they serve different post-processing needs — pick the one(s) a case actually needs rather than defaulting to all of them.

## Per-timestep field/particle output — `output_settings`

Writes per-particle, per-mesh, contact/bond-network, and Eulerian-field snapshots at each output interval (VTK/VTM by default).
This is the data source for spatial analysis and visualization — histograms of a per-particle property, contact-network inspection, animating the run, etc.
See `commands/output_settings.md` for the command itself, and `RUNNING.md` for visualizing the result in ParaView.
Because every particle property is written per timestep, arbitrary post-hoc analysis (e.g. building a diameter histogram) can be done afterwards from this data even when there's no dedicated in-run command for it — Aspherix has no native binning/histogram command, so that kind of derived analysis has to be built from the raw per-particle output rather than computed by the script.

## Scalar time series — `status` / `status_style`

Writes scalar, whole-simulation values (particle count, kinetic energy, a `calculate` result, a custom variable, ...) at each status interval, to the terminal, log, and/or a CSV file.
This is the data source for tracking a single number over time — e.g. a fill fraction, a mesh's center of mass, a custom counter.
See `commands/status.md`.

The CSV destination (`file`) always writes to a fixed filename (`simulation_data_aspherix.csv`) with no override — if a workflow runs multiple variants/cases in the same working directory, later runs will overwrite an earlier run's CSV.
Isolate variants into separate run directories, or copy the CSV out immediately after each run, rather than assuming it's safe to leave in place.

## In-run derived/aggregate quantities — `calculate`

Computes a derived or spatially/temporally aggregated quantity during the run (residence time, massflow, mixing index, center of mass, min/max/average of a property, etc.) — see `RULES.md` for preferring `calculate` over the legacy `compute` command.
A `calculate` command's result is referenced elsewhere (a `variable` formula, a `status_style` column, `output_settings` particle properties) via its `id_` form — see `commands/variable.md` for that reference syntax.
Look up the specific `calculate` command needed on the public documentation (`DOC_SEARCH.md`) — the family is large and case-specific (residence time vs. massflow vs. mixing index are different commands, not modes of one command).

## Sequencing

`status_style` and `calculate` outputs are computed as the simulation runs, not derived afterwards — decide what needs to be tracked over time *before* running, since there's no way to reconstruct a missing time series from a completed run's other output.
Per-timestep field output (`output_settings`) is the exception: because it captures full per-particle/per-mesh state at each interval, it supports post-hoc analysis that wasn't explicitly anticipated, at the cost of more data being written (see `RULES.md` on being considerate with output intervals).
