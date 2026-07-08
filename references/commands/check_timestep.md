# Check Timestep Command Guidelines

`check_timestep` estimates the Rayleigh and Hertz time for a granular system and compares them against the chosen `simulation_timestep`, warning when the timestep is too large for numerical stability.
See `../RULES.md` for the general timestep-criteria rule this command satisfies.

## Syntax

```
check_timestep keyword value ...
```

## Keywords

| Keyword | Description | Default |
|---|---|---|
| `id` | command id | — |
| `rayleigh_fraction` | warn if timestep exceeds this fraction of Rayleigh time | `0.1` |
| `hertz_fraction` | warn if timestep exceeds this fraction of Hertz time | `0.1` |
| `check_overlap` | also check particle overlap distance | `no` |
| `maximum_overlap` | max allowed relative overlap before warning | `0.1` |
| `check_conduction` | also check heat conduction stability | `no` |
| `conduction_fraction` | warn if timestep exceeds this fraction of conduction stability time | `0.5` |

`check_conduction` requires `enable_heat_transfer` to be set up first.

```
check_timestep id check_ts rayleigh_fraction 10% hertz_fraction 10%
check_timestep hertz_fraction 15% check_overlap yes maximum_overlap 15%
check_timestep check_conduction yes conduction_fraction 20%
```

## What's checked

- **Rayleigh time** — depends only on material properties (density, shear modulus, Poisson's ratio); the minimum across all particles is used.
- **Hertz time** — estimated from each particle's self-collision at its maximum relative velocity; generally less restrictive than Rayleigh, especially in near-static conditions.
- **Skin ratio** — checks that the mesh/neighbor-list skin still exceeds how far particles travel relative to each other per timestep (ratio should stay above 1).
- **Particle overlap** (`check_overlap yes`) — relative overlap (overlap / smaller radius); keep below 10%.
- **Heat conduction** (`check_conduction yes`) — timestep vs. the conduction stability timescale.

## Timing

Like `status`, `check_timestep` doesn't take its own output-frequency argument — it's evaluated and printed every `write_to_terminal_timestep`.
See `status.md` for the same pattern applied to `status`/`status_style`.

Note: Aspherix also runs an automatic, implicit timestep check even without an explicit `check_timestep` command, warning when the timestep exceeds 20% of the Hertz/Rayleigh timescale. An explicit `check_timestep` call is still preferred when a case needs tighter fractions, overlap checking, or conduction checking, or when its results need to be referenced elsewhere (see below).

## Preferred usage

`check_overlap yes` is generally a good idea — enable it by default rather than only reaching for it when overlap problems are already suspected.

```
check_timestep id check_ts check_overlap yes
```

## Referencing results elsewhere

Like a `calculate` command, `check_timestep`'s results can be pulled into a `variable` or `status_style` column via `id_ID` (see `variable.md` for that reference syntax):

- `id_ID.rayleigh` / `id_ID.rayleigh_fraction`
- `id_ID.hertz` / `id_ID.hertz_fraction`
- `id_ID.skin` / `id_ID.skin_fraction`
- `id_ID.maximum_overlap_pp`, `id_ID.maximum_overlap_pw` — max particle-particle / particle-wall overlap
- `id_ID.maximum_overlap_pp_i`, `id_ID.maximum_overlap_pp_j`, `id_ID.maximum_overlap_pw_i` — particle IDs involved in the max overlaps
- `id_ID.conduction` / `id_ID.conduction_fraction`

Requires the command to have an explicit `id`, since the reference is built from it.

```
check_timestep id check_ts rayleigh_fraction 10% hertz_fraction 10%
variable timestep_ok boolean "id_check_ts.rayleigh_fraction < 1 && id_check_ts.hertz_fraction < 1"
```

