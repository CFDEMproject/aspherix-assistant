# Strategies

Short, self-contained problem-solving strategies for building and debugging Aspherix cases.

Each entry here should be a few sentences — just enough to state the strategy and when to reach for it.
If a strategy needs its own examples, multi-step walkthrough, or supporting files, give it its own file in `references/strategies/<name>.md` and link it from here instead of growing this file.

## Mesh element size vs. particle size

When generating or importing a wall mesh (STL/VTK/OBJ, see `mesh.html`), keep triangle edge lengths on the same order as the particle diameters that will contact it, rather than triangulating for visual smoothness alone.
Aspherix's neighbor-list binning sizes its bins off the particle contact cutoff, so a mesh triangulated much finer than the particles multiplies the number of wall-neighbor entries each particle has to check, degrading performance and memory use for no physical benefit.
Triangles much larger than the particles are also a problem on curved geometry: a coarse triangulation flattens the curve into visible facets, and particles can catch on the resulting edges as if the surface had artificial steps.
If a case needs a smooth curved surface without shrinking every triangle to particle scale, use `mesh.html`'s `curvature`/`curvature_tolerant` keywords to control faceting on curved regions specifically, rather than uniformly refining the whole mesh.
