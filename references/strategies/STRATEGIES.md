# Strategies

Short, self-contained problem-solving strategies for building and debugging Aspherix cases.

Each entry here should be a few sentences — just enough to state the strategy and when to reach for it.
If a strategy needs its own examples, multi-step walkthrough, or supporting files, give it its own file in `references/strategies/<name>.md` and link it from here instead of growing this file.

## Mesh element size vs. particle size

When generating or importing a wall mesh (STL/VTK/OBJ, see `mesh.html`), keep triangle edge lengths on the same order as the particle diameters that will contact it, rather than triangulating for visual smoothness alone.
Aspherix's neighbor-list binning sizes its bins off the particle contact cutoff, so a mesh triangulated much finer than the particles multiplies the number of wall-neighbor entries each particle has to check, degrading performance and memory use for no physical benefit.
Triangles much larger than the particles are also a problem on curved geometry: a coarse triangulation flattens the curve into visible facets, and particles can catch on the resulting edges as if the surface had artificial steps.
If a case needs a smooth curved surface without shrinking every triangle to particle scale, use `mesh.html`'s `curvature`/`curvature_tolerant` keywords to control faceting on curved regions specifically, rather than uniformly refining the whole mesh.

## Artificially soft Young's modulus for numerical stability

Real material Young's moduli (e.g. ~200 GPa for steel, ~70 GPa for glass) push Hertzian contact stiffness high enough that the resulting Rayleigh/Hertz timestep (see `commands/check_timestep.md`) becomes impractically small — a case built with a literal, "realistic" Young's modulus is one of the most common sources of instability or outright errors on first run, not a solver bug.
Standard DEM practice for rigid-ish materials (metals, minerals, most bulk solids) is to soften Young's modulus by several orders of magnitude (e.g. down to the 1e6-1e8 Pa range) rather than use the literal material value: contact overlap and force response barely change at DEM timescales for a genuinely rigid material, so the modulus only needs to be high enough that particles don't visibly interpenetrate, not physically exact.
Always pair a chosen Young's modulus with `check_timestep` (see `commands/check_timestep.md` and `RULES.md`'s Timestep Criteria) rather than picking a modulus and `simulation_timestep` independently — if a case uses a high Young's modulus (order 1e9 Pa or above) and also reports timestep/stability errors, softening the modulus is usually the right fix, not shrinking the timestep further to compensate.
This softening isn't appropriate for every case: skip it when contact stiffness itself is the quantity of interest (e.g. calibrating against a real material's elastic response, or a packing/consolidation study sensitive to stiffness) — flag that tradeoff to the user rather than silently softening the modulus.
