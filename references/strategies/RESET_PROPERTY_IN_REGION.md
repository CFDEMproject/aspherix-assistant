# Resetting a per-particle property in a region

No native command is known that resets a built-in per-particle property (e.g. `charge`) every timestep for the particles in a region.
`set` (`set.html`) acts once when it is called, and `fix property/set` (`fix_property_set.html`) only works on custom `fix property/atom` properties.
Alternate `simulate` and `set` instead: a `while` loop (see `while_do.html`) that runs `simulate time <interval>` and then `set region <region-id> <property> <value>` once per iteration.
`set` takes a region directly (`set.html`), so no group is needed. It changes only the particles inside the region when it is called; a particle that has left keeps the value.

Rule of thumb, not verified against the documentation:
- Choose `<interval>` no larger than the time a particle needs to cross the region, otherwise crossings are missed between resets.
