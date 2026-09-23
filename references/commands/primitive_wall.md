# Primitive Wall Command Guidelines

`primitive_wall` creates a wall from an analytic shape (plane, cylinder, or disk) instead of a triangulated mesh.
Prefer it over `mesh` for any wall that fits one of these shapes and never needs to translate or rotate, since it avoids importing, preprocessing, and re-binning a mesh for geometry that's already exact.

## What it can't do

There's no motion mechanism: `primitive_wall` has no equivalent of `mesh_module motion`, so it can't translate or rotate.
The `shear` keyword only imposes a surface velocity (useful for simulating a spinning disk or a rotating-drum wall) — the wall's own position stays fixed.
If the wall needs to actually move, use a `mesh` with `mesh_module motion` instead.

A fixed `temperature` (for heat conduction) is equivalent to `mesh_module heattransfer`'s `heat_transfer_mode constant`; use `mesh_module heattransfer` itself only when the wall's temperature needs to change dynamically.

## Shapes and their keywords

See `primitive_wall.html` for the full keyword tables; in short:

- `type plane` — either a finite plane (`origin`, `point_1`, `point_2`, forming an orthogonal corner) or an infinite axis-aligned plane (`normal_axis`, `offset`).
- `type cylinder` — either a finite, open-ended cylinder (`center_bottom`, `center_top`, `radius`) or an infinite axis-aligned cylinder (`axis`, `center`, `radius`).
- `type disk` — `center`, `normal`, `radius`, with an optional `inner_radius` to punch a hole through the middle.

## Examples

```
primitive_wall id plane material steel type plane normal_axis z offset 0.
primitive_wall id finite_plane material steel type plane origin (0,0,0) point_1 (0,0,1) point_2 (0,1,0)
primitive_wall id cylinder material steel type cylinder axis z center (0.,0.,0.) radius 1.
primitive_wall id finite_cylinder material plastic type cylinder center_bottom (0,1,0) center_top (1,2,4) radius 0.3
primitive_wall id disk material steel type disk center (1,0,0) normal (0,1,1) radius 0.1
primitive_wall id disk_with_hole material steel type disk center (0.1,0.1,0) normal (1,0,1) radius 0.1 inner_radius 0.05
```

`shear` turns a plane, cylinder, or disk into a stand-in for a moving surface without any actual mesh motion:

```
# a shearing floor: constant surface velocity across the whole plane
primitive_wall id floor material steel type plane normal_axis z offset 0.01 shear y 1.3

# a rotating drum: cylinder parallel to x, shear velocity (0,1,0) makes the surface appear to rotate
primitive_wall id drum_wall material steel type cylinder axis x center (0.,0.,0.) radius 1. shear (0,1,0)
```

## Restrictions

The docs' own Restrictions section says "none" — contact history is checkpointed to binary restart files like a mesh wall's, and none of `modify_command`'s options apply to it.
VTK/VTM output for a `primitive_wall` hasn't been confirmed against the docs; verify against actual output before relying on it being written out the same way a `mesh` wall's is.
