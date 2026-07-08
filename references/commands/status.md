# Status Command Guidelines

`status` and `status_style` work together to print run-time status info (kinetic energy, particle count, time, etc.) during a simulation.
`status` controls *how often* it's printed; `status_style` controls *what* gets printed and *where*.

## `status` — timing

```
status N
```

`N` is the timestep interval: status is printed every `N` timesteps, plus always at the start and end of a simulation.
`N = 0` (the default) prints only at simulation start and end.

```
status 100
```

### Variable-driven intervals

`N` can be a `v_name` reference to an `equal`-style variable instead of a fixed number.
The variable is re-evaluated at each trigger point, so it can produce a non-uniform schedule — useful with `stagger()`, `logfreq()`, or `stride()`.

```
variable s equal logfreq(10,3,10)
status v_s
```

This prints status at timesteps `0, 10, 20, 30, 100, 200, 300, 1000, 2000, ...`.

See `variable.md` for general `variable` usage.

### Prefer `write_to_terminal_timestep` over `status N`

Setting `write_to_terminal_timestep` also drives status output, and is the preferred way to set the status cadence — prefer it over calling `status N` directly.
Unlike `status N` (a timestep count), `write_to_terminal_timestep` is expressed in simulation time units, and it is shared with other commands that print diagnostics (e.g. `check_timestep`), so setting it once keeps all terminal output on a consistent cadence instead of configuring each command's frequency separately.

```
write_to_terminal_timestep 0.001
```

## `status_style` — content and destination

```
status_style destination {keyword,keyword,...} [destination {keyword,keyword,...} ...] [comment_style "string"] [mode set|add|remove]
```

It writes to up to three destinations, and each destination gets its own list of columns.

### Destinations

- `terminal` — screen and log file.
- `file` — `simulation_data_aspherix.csv`.
- `all` — all of the above.

### Column keywords

Built-in: `step`, `elapsed`, `elaplong`, `dt`, `time`, `cpu`, `tpcpu`, `spcpu`, `cpuremain`, `part`, `cu`, `timestamp`, `atoms`, `particles`, `ke`, `erotate`, `vol`, `lx`, `ly`, `lz`, `xlo`, `xhi`, `ylo`, `yhi`, `zlo`, `zhi`, `xy`, `xz`, `yz`, `xlat`, `ylat`, `zlat`, `pxx`, `pyy`, `pzz`, `pxy`, `pxz`, `pyz`, `fmax`, `fnorm`, `cella`, `cellb`, `cellc`, `cellalpha`, `cellbeta`, `cellgamma`.

Custom references (same reference forms as in `variable` formulas — see `variable.md`):
- `id_ID`, `id_ID[I]`, `id_ID[I][J]`, `id_ID.property_name` — `calculate` command results.
- `v_name` — a variable.

### Optional keywords

- `comment_style "string"` — prepend header lines with the given string. Default: none.
- `mode set|add|remove` — how this call's columns combine with a prior `status_style` call. `set` (default) overwrites, `add` appends, `remove` removes.

### Default

```
status_style all {time,step,atoms,ke,cu}
```

### Examples

```
status_style terminal {time,step,atoms,ke,cu,vol} file {time,step,atoms,ke,cu,id_mesh[1],id_mesh[2],id_mesh[3]}
```

```
status_style all {time,step,particles,ke,cu,id_mesh[1],id_mesh[2],id_mesh[3]} comment_style "%%"
```

```
status_style mode add terminal {v_terminal} file {id_servo.center_of_mass_x}
```

### Preferred usage

- Use the `all` destination (terminal, log, and CSV file together), unless a case specifically needs to keep one destination's columns different from the others.
- Use `mode add` rather than the default `mode set`. `set` overwrites any columns already configured (including the built-in default `{time,step,atoms,ke,cu}`), so a later `set` call can silently drop output that was already there; `add` appends instead, so nothing already configured gets lost.

```
status_style mode add all {my_custom_column}
```
