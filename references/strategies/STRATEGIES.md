# Strategies

Short, self-contained problem-solving strategies for building and debugging Aspherix cases.

Each entry here should be a few sentences — just enough to state the strategy and when to reach for it.
If a strategy needs its own examples, multi-step walkthrough, or supporting files, give it its own file in `references/strategies/<name>.md` and link it from here instead of growing this file.

## Verify a per-particle-state command actually worked

`mark_particles`/`define_group`/`enable_heat_transfer`/... can run with no error while doing nothing — verify the actual value.
Use `define_group id check region <same-region>` for a live count, or the restart file for a property meant to persist through one.

## Mesh element size vs. particle size

When generating or importing a wall mesh (STL/VTK/OBJ, see `mesh.html`), keep triangle edge lengths on the same order as the particle diameters that will contact it, rather than triangulating for visual smoothness alone.
Aspherix's neighbor-list binning sizes its bins off the particle contact cutoff, so a mesh triangulated much finer than the particles multiplies the number of wall-neighbor entries each particle has to check, degrading performance and memory use for no physical benefit.
Triangles much larger than the particles are also a problem on curved geometry: a coarse triangulation flattens the curve into visible facets, and particles can catch on the resulting edges as if the surface had artificial steps.
If a case needs a smooth curved surface without shrinking every triangle to particle scale, use `mesh.html`'s `curvature`/`curvature_tolerant` keywords to control faceting on curved regions specifically, rather than uniformly refining the whole mesh.

## Mesh preprocessing

A mesh (walls, moving geometry) imported into a case may need preprocessing before Aspherix will accept it or before it'll behave correctly — unit mismatches, topological defects caught at import, mesh-quality hard limits that only trigger on first real use, distinguishing intentional geometry from defects, and deriving/verifying regions from a mesh's actual enclosed interior.
See `strategies/MESH_PREPROCESSING.md` for the full walkthrough.

## What a reduced-scale ("smoke") run establishes

Running a script at a much lower particle count validates plumbing — it parses, meshes import, motion and measurement commands bind, output appears — but not physics or termination.
Packing geometry changes with count, so anything driven by bed depth (conveying, shearing, burden weight) becomes a different problem rather than a smaller one; check where the particles actually settle before treating a reduced run as representative.
Cost does not scale with count either, since wall meshes are re-binned every timestep however few particles there are — compare wall-triangle count against particle count first, and note that moving meshes cost substantially more per step than static ones (measured ~4x).
A smoke run's physics can genuinely never reach its own stop condition at reduced scale (e.g. a bed-depth-dependent process that needs a real bed to engage) — and since `until_condition_reached`/`until_settled`/`until_filled` have no timeout argument, that burns wall-clock time indefinitely with no signal anything is wrong.
Cap a smoke-scale run's own wall-clock time (a practical default: 10 minutes) independent of its own stop condition — if it hasn't finished by then, stop it and ask the user whether the behavior genuinely needs full scale to reproduce, rather than assuming reduced scale must eventually converge.

## `check_timestep` is silent unless a fraction is actually exceeded - surface it explicitly, don't rely on the absence of a warning

`check_timestep` (and Aspherix's own implicit 20% check) only prints when a fraction is exceeded - an unbroken log of no warnings means margin was never tested, not that it's safe.
Surface it proactively instead: add its `.rayleigh_fraction`/`.hertz_fraction` (see `commands/check_timestep.md`'s reference syntax) to `status_style` in every phase of a case, not just where a problem is already suspected - each phase can have a different effective timestep, so margin in one says nothing about another.

## Artificially soft Young's modulus for numerical stability

Real material Young's moduli (e.g. ~200 GPa for steel, ~70 GPa for glass) push Hertzian contact stiffness high enough that the resulting Rayleigh/Hertz timestep (see `commands/check_timestep.md`) becomes impractically small — a case built with a literal, "realistic" Young's modulus is one of the most common sources of instability or outright errors on first run, not a solver bug.
Standard DEM practice for rigid-ish materials (metals, minerals, most bulk solids) is to soften Young's modulus by several orders of magnitude (e.g. down to the 1e6-1e8 Pa range) rather than use the literal material value: contact overlap and force response barely change at DEM timescales for a genuinely rigid material, so the modulus only needs to be high enough that particles don't visibly interpenetrate, not physically exact.
Always pair a chosen Young's modulus with `check_timestep` (see `commands/check_timestep.md` and `RULES.md`'s Timestep Criteria) rather than picking a modulus and `simulation_timestep` independently — if a case uses a high Young's modulus (order 1e9 Pa or above) and also reports timestep/stability errors, softening the modulus is usually the right fix, not shrinking the timestep further to compensate.
This softening isn't appropriate for every case: skip it when contact stiffness itself is the quantity of interest (e.g. calibrating against a real material's elastic response, or a packing/consolidation study sensitive to stiffness) — flag that tradeoff to the user rather than silently softening the modulus.

## GPU/CPU command and model parity isn't guaranteed or fully documented

A command, insertion style, or contact-model sub-style that works on CPU may be rejected or behave differently on GPU.
If the preferred choice turns out to be GPU-unsupported, look for a GPU-supported alternative that approximates the same physical intent rather than dropping the requirement silently.

## Non-sphericity

A sphere is the default shape for a reason (cheapest to simulate) — but for markedly non-spherical particles (elongated, angular, flat), represent that with either a genuinely non-spherical shape (multi-sphere, convex/concave, superquadric) or a rolling-friction contact model on ordinary spheres.
Prefer rolling friction by default: it approximates bulk flow behavior (angle of repose, mixing) well at much lower cost, and is sufficient unless the particle geometry itself is what the case needs to get right.

## Insertion

Picking the right `simulate` mode for how particles were inserted, verifying a `pack` insertion actually hit its target, reaching a high cumulative target without retrying `pack`, packing particles into position by tilting gravity instead, and compacting a bed with `mesh_module servo`.
See `strategies/INSERTION.md` for the full set of strategies.

## Writing a periodic restart checkpoint, not just one at the end

`RULES.md`'s "Simulation Output" section says to write intermediate restarts during long runs; this is the concrete mechanism.
Use the `restart` command (`restart.html`), not another `write_restart` call: `restart N file1 file2` writes a checkpoint every N *timesteps* (compute N from the phase's own `write_output_timestep`/`simulation_timestep`) and alternates between the two filenames, so a crash mid-write can't corrupt both at once.
Keep this separate from a final one-shot `write_restart` at a `simulate` block's natural end (e.g. `until_settled` converging) - that stays the real, fully-settled handoff; the periodic ones exist so a long run can be stopped early without losing everything, at the cost of a not-yet-converged handoff if used that way.
If a later phase's `read_restart` path should be swappable between the two, make it an `index`-style variable overridable via `-var` rather than a literal filename.
This mechanism is for a standalone Aspherix run only - a CFD-coupled case (`enable_cfd_coupling`) syncs restarts from the CFD side, not through this `restart` mechanism, so don't assume it applies there too (see `commands/enable_cfd_coupling.md`).

## Only regenerate a restart when the phase that produced it actually needs to change

Before re-running an earlier phase's script over a later phase's parameter change, check whether the earlier phase's own physics actually depends on it.
E.g. packing is independent of particle heat capacity, so `read_restart` can just pick up the new value instead of re-running the packing phase.

## Ramp prescribed mesh motion from rest, don't start it at full speed

See `mesh_module_motion.html`'s note on starting at full speed, and `variable.html`'s note on building a temporal ramp for a `simulate`-based script (not the `ramp(x,y)` math function, which isn't a fit there) - apply that general pattern to the motion command's velocity/period/omega argument.

## Cohesion

Cohesion (inter-particle/particle-wall stickiness) is a separate property from friction, defaults off, and should stay off unless the material is actually known or expected to be cohesive (fine powders, moisture, etc.).
Enabling it adds its own coefficients — flag them for sign-off like any other material property (see `REPORTING.md`).

