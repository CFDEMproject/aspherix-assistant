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
Don't run a dropping/settling test on every mesh as a matter of course — a full case run is expensive, and a passing import check is sufficient by default.
Reach for a short, cheap dropping/settling test of a modest number of particles specifically when debugging — e.g. particles are leaking through a wall, piling up somewhere unexpected, or another symptom suggests the mesh doesn't actually behave as intended despite importing cleanly.

In an interactive session, prompt the user to visually inspect the mesh as part of that debugging — human eyes are very good at spotting the kind of defect (a flipped normal, a gap, an unexpected facet) that's tedious to characterize programmatically.
If a mesh viewer is available (e.g. ParaView, `fstl`), offer to open the mesh for the user yourself after prompting, rather than only pointing them to a viewer.

## Distinguishing intentional geometry from defects

A mesh with an opening, gap, or missing surface in it may be modeling a real, intentional feature (an inlet, an outlet, a vent) rather than a defect.
Before treating something found during import/healing as a problem to fix, consider whether the case description already implies that feature is supposed to be there — and if it's ambiguous, treat it as worth confirming rather than silently "fixing" (patching) or silently leaving it open.

## Deriving internal regions inside a mesh

When creating a region (eg. insertion zone) inside of a mesh size the region from the mesh's enclosed interior, not its bounding box.
The bounding box may include non-structural features (flange, lip, bracket) that can extend past what's actually enclosed.
Create the region from a mid-span cross-section.
In an interactive session you may prompt the user to verify the region visually (eg. `Paraview`).
When operating autonomously you need to verify the enclosure correctly (collision detection between triangles and the region) rather than just checking the region is clear of mesh vertices.

For post-processing some regions may extend outside of the mesh domain if required (eg. a bounding box over a segment of a tube to count particles inside the tube is perfectly valid if particles are only inside the tube).
