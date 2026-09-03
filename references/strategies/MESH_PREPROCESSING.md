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

A harder blind spot: `simulate time 0` never evaluates Aspherix's mesh-quality hard limits (sub-degree sliver angles, >5 edge-neighbors) — those only trigger once a real run has a particle, `particle_contact_model`, and `wall_contact_model` present.
A mesh can pass the import check and still hard-error on first real use; that's a first discovery, not a wrong earlier check.
The same heal/remesh escalation from "Healing / topological repair" above applies, with `element_exclusion_list` (`mode write` to discover, `mode read` to skip) as the last resort for residual elements.

In an interactive session, prompt the user to visually inspect the mesh as part of that debugging — human eyes are very good at spotting the kind of defect (a flipped normal, a gap, an unexpected facet) that's tedious to characterize programmatically.
If a mesh viewer is available (e.g. ParaView, `fstl`), offer to open the mesh for the user yourself after prompting, rather than only pointing them to a viewer.

## Distinguishing intentional geometry from defects

A mesh with an opening, gap, or missing surface in it may be modeling a real, intentional feature (an inlet, an outlet, a vent) rather than a defect.
Before treating something found during import/healing as a problem to fix, consider whether the case description already implies that feature is supposed to be there — and if it's ambiguous, treat it as worth confirming rather than silently "fixing" (patching) or silently leaving it open.

## Deriving internal regions inside a mesh

When creating a region (eg. insertion zone) inside of a mesh, size it from the mesh's enclosed interior, not its bounding box - the box can include non-structural features (flange, lip, bracket), and the true interior is often narrower or differently shaped in ways easy to miss by reasoning about coordinates alone.

**Verify any such region with a real geometric check against the mesh's triangles before using it or showing it to the user** - not just checking that its corners or a few mesh vertices are clear.
This applies whether the session is interactive or autonomous.

Do the check with a mesh-processing library (`trimesh`), not by hand, and prefer a direct collision test over inferring position from sampled ray distances.
- Build the candidate region as its own simple mesh (box/cylinder).
- Test it against the wall mesh with `trimesh.collision.CollisionManager` (backed by `python-fcl`).
- `manager.in_collision_internal()` reports whether the region's boundary touches or crosses any wall triangle at all.

The collision test needs no watertightness or manifold mesh - it's a plain triangle-triangle intersection.
It works the same whether the mesh has holes, non-manifold edges, or an intentional opening; watertightness is neither guaranteed for a real mesh nor required here.

No collision plus one point already known to be inside the mesh together confirm the whole region is inside, since a region with no boundary crossing can't have leaked to the wrong side of the wall.
That "known-inside" point has to come from domain knowledge - the case description, or the user's own visual confirmation - not from an automated point-in-mesh classifier.

See `PYTHON.md` for getting `trimesh`/`python-fcl` installed without a global `pip install`.

In an interactive session, prompt the user to verify the region visually (eg. `Paraview`).
This is in addition to the geometric check, not a replacement for it.

For post-processing some regions may extend outside of the mesh domain if required (eg. a bounding box over a segment of a tube to count particles inside the tube is perfectly valid if particles are only inside the tube).

A short solver run with `check_overlap yes` on a modest particle count can be used as an extra cross-check.
Depending on the particle count this can be expensive.
*ONLY ATTEMPT THIS AFTER* the user has confirmed the region, never before.
