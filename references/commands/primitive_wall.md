# Primitive Wall Command Guidelines

See `primitive_wall.html` for syntax, restrictions (no motion mechanism), and output behavior (no VTK output). Prefer it over a `mesh` for any wall that never moves. A fixed `temperature` is equivalent to `mesh_module heattransfer`'s `heat_transfer_mode constant`; use `mesh_module heattransfer` itself only for dynamic thermal behavior.
