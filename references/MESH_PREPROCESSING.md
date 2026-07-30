# Mesh Preprocessing

Meshes (walls, moving geometry) imported into a case may need preprocessing before Aspherix will accept them or before they'll behave correctly.

## Units

Meshes are frequently authored/exported in a different unit system (e.g. millimeters) than the simulation's own unit system (typically SI/meters).
Aspherix does not convert mesh units on import — check the mesh's actual scale (bounding box) against the case's `simulation_domain` before assuming they already match.

## Healing / topological repair

An imported mesh can fail Aspherix's own import checks (non-manifold edges, degenerate/duplicate facets, slivers) independent of any unit issue.
If a dedicated mesh-healing/preprocessing tool exists in the Aspherix ecosystem for this, prefer it over an in-solver workaround (e.g. an element-exclusion mechanism).

## A passing import check is not the same as a physically correct mesh

Getting a mesh to import successfully only confirms it's topologically acceptable to the solver — it does not confirm the mesh is watertight, or that it correctly represents the intended geometry.
For a mesh meant to contain or guide particles, verify this behavior directly and cheaply — e.g. a short test dropping/settling a modest number of particles.

## Distinguishing intentional geometry from defects

A mesh with an opening, gap, or missing surface in it may be modeling a real, intentional feature (an inlet, an outlet, a vent) rather than a defect.
Before treating something found during import/healing as a problem to fix, consider whether the case description already implies that feature is supposed to be there — and if it's ambiguous, treat it as worth confirming rather than silently "fixing" (patching) or silently leaving it open.
