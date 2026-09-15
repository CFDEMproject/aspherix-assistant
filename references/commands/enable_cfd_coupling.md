# Enable CFD Coupling Command Guidelines

`enable_cfd_coupling` connects a running Aspherix simulation to a CFD simulation over a socket, so drag (and optionally heat transfer, species/liquid/attrition transport, surface film, photon reflection) is computed on the CFD side and applied to particles on the DEM side.
See `../RULES.md`'s Command Ordering section for general command-ordering rules — this command has its own, stricter placement requirement below.

## Syntax

```
enable_cfd_coupling keyword value ...
```

Key keywords: `verbose`, `port_file_path`, `port_base`, `timeout`, `keep_port_file`, `treat_multispheres_as_spheres`, `add_fluid_mass` (with `added_mass_coefficient`/`fluid_density`), `heat_transfer`, `species_convection` (with `species_name`/`species_initial_value`), `liquid_transport`, `track_spray_collisions`, `attrition_transport`, `surface_film` (with `variable_properties`), `photon_reflection` (with `surface_refractive_index`).

```
enable_cfd_coupling
enable_cfd_coupling verbose 1
enable_cfd_coupling heat_transfer yes
enable_cfd_coupling species_convection yes species_name H2O species_initial_value 0.01
```

## Ordering

This command must be the last command in the input script before output is configured.
In particular, it must not precede `enable_gravity`, `enable_heat_transfer`, `simulation_timestep`, or `particle_template` if those are used in the case.
It also resets the write interval set by `write_output_timestep` if an `output_settings` command was declared earlier, so declare `output_settings` after `enable_cfd_coupling`, not before.

## Restrictions

Requires a CFDEMcoupling simulation running alongside using the `twoWaySocket` model (or an equivalent setup) — this command only opens/configures the DEM-side socket, it does not start the CFD side.
Cannot be combined with `enable_buoyancy`.

## Restart checkpointing is not driven from the Aspherix side

`../strategies/STRATEGIES.md`'s "Writing a periodic restart checkpoint" entry (the `restart`/`write_restart` commands) applies to a standalone Aspherix run, not a coupled one.
In a coupled case, restart synchronization between the DEM and CFD sides is driven from the CFD side, not by any `enable_cfd_coupling` keyword or by Aspherix's own `restart` command - don't assume `restart N file1 file2` alone produces a restart point the coupled CFD run can resume from in sync.
