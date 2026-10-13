# Resetting a per-particle property in a region

No native command is known that resets a built-in per-particle property (e.g. `charge`) every timestep for the particles in a region.
`set` (`set.html`) acts once when it is called, and `fix property/set` (`fix_property_set.html`) only works on custom `fix property/atom` properties.
Alternate `simulate` and `set` instead:
- `define_group` with `region` and `update_every_time <interval>` (see `define_group.html`), optionally narrowed with `intersect`.
- A `while` loop (see `while_do.html`) that runs `simulate time <interval>` and then `set group <group> <property> <value>` once per iteration.

Rules of thumb, not verified against the documentation:
- Use the same chunk size as `update_every_time`, so that group membership is current when `set` runs.
- Choose `<interval>` no larger than the time a particle needs to cross the region, otherwise crossings are missed between resets.
