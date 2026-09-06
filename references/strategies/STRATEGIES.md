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
=======
## What a reduced-scale ("smoke") run establishes

Running a script at a much lower particle count validates plumbing — it parses, meshes import, motion and measurement commands bind, output appears — but not physics or termination.
Packing geometry changes with count, so anything driven by bed depth (conveying, shearing, burden weight) becomes a different problem rather than a smaller one; check where the particles actually settle before treating a reduced run as representative.
Cost does not scale with count either, since wall meshes are re-binned every timestep however few particles there are — compare wall-triangle count against particle count first, and note that moving meshes cost substantially more per step than static ones (measured ~4x).

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

## `simulate mode until_filled`/`until_settled` - pick the mode that matches the insertion style

See `simulate.html` for what each mode actually checks - don't guess from the name. In short: `until_filled` assumes a `pack`-then-`stream` pattern and is not a fit for a one-shot `pack` (use `until_settled` instead) or for a `rate_in_region` insertion with its own `target_particle_count`/`target_mass` (use a separate `until_condition_reached` on that target, then `until_settled` - `until_settled`'s own convergence check is not reliable while insertion is still running, per its documented note).

## Verify a `pack` insertion actually reached its target

See `insertion.html` for `packing_generator` styles, the `dense_experimental` ceiling, and when to prefer `rate_in_region` over any one-shot packing style. Whichever style is used, check the actual inserted count against the target afterward rather than assuming it was met - a silent shortfall can also make a downstream stop condition sized for the *intended* count wrong (see `RULES.md`'s "Cross-script Parameter Consistency").

## Ramp prescribed mesh motion from rest, don't start it at full speed

See `mesh_module_motion.html`'s note on starting at full speed, and `variable.html`'s note on building a temporal ramp for a `simulate`-based script (not the `ramp(x,y)` math function, which isn't a fit there) - apply that general pattern to the motion command's velocity/period/omega argument.

## Cohesion

Cohesion (inter-particle/particle-wall stickiness) is a separate property from friction, defaults off, and should stay off unless the material is actually known or expected to be cohesive (fine powders, moisture, etc.).
Enabling it adds its own coefficients — flag them for sign-off like any other material property (see `REPORTING.md`).
