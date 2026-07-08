# Output Settings Command Guidelines

`output_settings` generates the per-timestep simulation output files (particles, meshes, contact/bond networks, Eulerian fields) — VTM/VTK by default.
It's the native replacement for the legacy `dump` command; see `../RULES.md`.

## Syntax

```
output_settings keyword value [keyword value ...]
```

Zero or more keyword/value pairs, grouped into particle, geometry, interaction, Eulerian, and general settings.
Calling it again defaults to `mode modify`, layering new keywords onto the existing configuration rather than replacing it — pass `mode replace` to start over.

## Timing — prefer `write_output_timestep`

Output frequency (`write_every_time`) defaults to `dt_out * dt`, driven by the global `write_output_timestep` command (time units, not a timestep count) — the same pattern as `status`/`status_style` preferring `write_to_terminal_timestep` over a per-command interval.
Set `write_output_timestep` once rather than overriding `write_every_time` per `output_settings` call, so file output and terminal/status output stay on deliberately chosen, independent cadences.

```
write_output_timestep 0.01
```

## Particle output

`write_particles` defaults to `yes` and the default `particle_properties` set is already sensible for most cases — a bare `output_settings` call is often enough to get particle output, with no `particle_properties` needed.

- `write_particles` {yes|no} — default `yes`.
- `particle_properties` {none|all|{prop_1, prop_2, ...}} — which per-particle properties to write. Only set this when a case genuinely needs a non-default set (e.g. a `calculate`-derived property like `id_Temp`, or trimming for a very large case). Standard properties: `id`, `radius`, `diameter`, `type`, `mass`, `x`, `y`, `z`, `vx`, `vy`, `vz`, `omegax`, `omegay`, `omegaz`, `fx`, `fy`, `fz`, `tqx`, `tqy`, `tqz`. Shape-dependent: `shapex`, `shapey`, `shapez`, `blockiness1`, `blockiness2`, `quat1..4`, `angmomx/y/z`. Physics-model outputs use `calculate`'s `id_` reference form (e.g. `id_Temp`, `id_heatFlux`) — see `variable.md` for that reference syntax.
- `particle_properties_exclude` {prop_1, ...} — exclude specific properties instead of listing everything to keep, when the default set has just a few properties too many.

```
output_settings particle_properties_exclude {tqx, tqy, tqz}
```

## Mesh (geometry) output

`write_meshes` also defaults to `yes` and picks up imported meshes automatically — `meshes`/`mesh_properties` are only needed to narrow the default set down.

- `write_meshes` {yes|no} — default `yes`.
- `meshes` {mesh_1, ...} — which imported meshes to output; only set when a case needs to output a subset of meshes.
- `mesh_properties` / `mesh_properties_exclude` — mesh attributes such as wear, stress, deformation; only set when a specific non-default attribute (e.g. wear) is actually needed.

## Interaction (contact/bond network) output

- `write_particle_contact_network` / `write_wall_contact_network` {yes|no} — default `no`.
- `write_particle_bond_network` / `write_wall_bond_network` {yes|no}.
- `particle_network_command_ids` / `wall_network_command_ids` — filter which contact/bond calculations get written.

## Eulerian output

- `write_eulerian_fields` {yes|no}.
- `eulerian_fields` {e_1, ...} — which spatial-averaging commands to write.

## File/format keywords

- `id` value — command id, default `output_setting`.
- `file` filename — default `post/dump_particle_*.vtm`; `*` is replaced by the timestep number.
- `folder` foldername — relative output directory.
- `ascii` {yes|no} — default `no` (binary).
- `compressor` {none|zlib|lz4} — default `none`.
- `parallel` {yes|no} and `number_of_output_processors` nout — distributed output control.
- `write_decomposition` {yes|no} — include processor domain info.
- `legacy_timeseries` {yes|no} — default `no`; the generated `aspherix_simulation.pvd` indexes by physical time rather than step number.

## Preferred usage

- Prefer the defaults. Per `../RULES.md`, only override a default when required — for `output_settings` that usually means a bare `output_settings` call is enough, and `particle_properties`/`mesh_properties` shouldn't be spelled out explicitly unless the case actually needs a non-default set.
- Be considerate with output frequency (`write_output_timestep`) — large simulations with long run times can generate a lot of data; see `../RULES.md`.
- When trimming is genuinely needed, prefer `particle_properties_exclude`/`mesh_properties_exclude` over restating the whole set with `particle_properties`/`mesh_properties` — it's shorter and stays correct if the defaults change.
- `output_settings` automatically triggers a default `status_style` (if not already set), and is aware of newly added meshes/properties across repeated `simulate` calls — repeated calls should rely on the default `mode modify` rather than restating the full configuration each time.

## Related commands

- `../RULES.md` — `output_settings` is the required native replacement for `dump`.
- `status.md` — `status`/`status_style` and `output_settings` are both gated by their own global timestep commands (`write_to_terminal_timestep` and `write_output_timestep` respectively), not by arguments on the command itself.
