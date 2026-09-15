# Strategies

Short, self-contained problem-solving strategies for building and debugging Aspherix cases.

Each entry here should be a few sentences — just enough to state the strategy and when to reach for it.
If a strategy needs its own examples, multi-step walkthrough, or supporting files, give it its own file in `references/strategies/<name>.md` and link it from here instead of growing this file.

## Mesh element size vs. particle size

When generating or importing a wall mesh (STL/VTK/OBJ, see `mesh.html`), keep triangle edge lengths on the same order as the particle diameters that will contact it, rather than triangulating for visual smoothness alone.
Aspherix's neighbor-list binning sizes its bins off the particle contact cutoff, so a mesh triangulated much finer than the particles multiplies the number of wall-neighbor entries each particle has to check, degrading performance and memory use for no physical benefit.
Triangles much larger than the particles are also a problem on curved geometry: a coarse triangulation flattens the curve into visible facets, and particles can catch on the resulting edges as if the surface had artificial steps.
If a case needs a smooth curved surface without shrinking every triangle to particle scale, use `mesh.html`'s `curvature`/`curvature_tolerant` keywords to control faceting on curved regions specifically, rather than uniformly refining the whole mesh.

## Mesh preprocessing

A mesh (walls, moving geometry) imported into a case may need preprocessing before Aspherix will accept it or before it'll behave correctly — unit mismatches, topological defects caught at import, mesh-quality hard limits that only trigger on first real use, distinguishing intentional geometry from defects, and deriving/verifying regions from a mesh's actual enclosed interior.
See `strategies/MESH_PREPROCESSING.md` for the full walkthrough.

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

## `simulate mode until_filled` is for continuous insertion, not one-shot `pack`

`insertion mode pack` inserts its full target in one shot at the next `simulate` call, not as an ongoing stream.
Pairing it with `simulate mode until_filled` is still a mistake, but for a more specific reason than "the two don't compose well": confirmed directly, in isolation, with nothing after `until_filled` in the script - once its own convergence criterion is met, `until_filled` itself issues a literal internal `delete_atoms region deletion_region_ remove_multispheres_completely yes`, wiping every particle in the case, no error or warning.
For a one-shot `pack` insertion, use `simulate mode until_settled` (optionally with its own `velocity_threshold`) instead - it settles the already-inserted bed without this cleanup step.
Reserve `until_filled` for `stream`/`rate_in_region`-style continuous insertion, where deleting a trial fill before the real one starts is presumably the intended behavior.

## Verify a `pack` insertion actually reached its target

See `insertion.html` for the `packing_generator` styles (`simple`/`dense`/`batch`) and the `dense`/`dense_experimental` volume-fraction ceiling. `dense`'s undershoot tracks the resulting **volume fraction** (particle volume / region volume), not the raw target count - a higher target that also raises the volume fraction can converge *closer* to target, not further from it, so don't assume a bigger ask must undershoot proportionally worse. Whichever style is used, check the actual inserted count against the target afterward rather than assuming it was met (see `RULES.md`'s "Cross-script Parameter Consistency" for why that matters downstream).

## Reaching a high cumulative insertion target - don't retry `pack`

A single one-shot `pack` insertion can't reach a high enough target on its own (see above), and retrying `pack` itself toward a region-occupancy target is a trap once particles are meant to leave the region after settling - see `insertion_pack.html`/`insertion_rate_in_region.html` for why. Use `mode rate_in_region` with `insert_every_time` instead (self-limits correctly via a genuine cumulative `target_particle_count`/`target_mass`), sized as a recipe rather than guessed:

1. Pulse interval = region depth (fall direction) / insertion velocity, so each pulse clears the region before the next fires.
2. Max feasible volume fraction per pulse ~20-30% (`rate_in_region` has no `packing_generator`, so it saturates via plain random sequential placement well below a packed bed) - verify against a real run rather than trusting the estimate.
3. Pulse rate sized to request the full remaining target each pulse.
4. Number of pulses = target volume fraction / that per-pulse ceiling, with a safety margin, rounded up.
5. Bound the insertion with a fixed-time window sized from that pulse count, `disable_command` it, and only then call `simulate mode until_settled` - see `simulate.html` for why a still-active insertion isn't safe to leave running into it.

## Writing a periodic restart checkpoint, not just one at the end

`RULES.md`'s "Cross-script Parameter Consistency" section says to write intermediate restarts during long runs; this is the concrete mechanism. Use the `restart` command (`restart.html`), not another `write_restart` call: `restart N file1 file2` writes a checkpoint every N *timesteps* (compute N from the phase's own `write_output_timestep`/`simulation_timestep`) and alternates between the two filenames, so a crash mid-write can't corrupt both at once. Keep this separate from a final one-shot `write_restart` at a `simulate` block's natural end (e.g. `until_settled` converging) - that stays the real, fully-settled handoff; the periodic ones exist so a long run can be stopped early without losing everything, at the cost of a not-yet-converged handoff if used that way. If a later phase's `read_restart` path should be swappable between the two, make it an `index`-style variable overridable via `-var` rather than a literal filename.

## Cohesion

Cohesion (inter-particle/particle-wall stickiness) is a separate property from friction, defaults off, and should stay off unless the material is actually known or expected to be cohesive (fine powders, moisture, etc.).
Enabling it adds its own coefficients — flag them for sign-off like any other material property (see `REPORTING.md`).
