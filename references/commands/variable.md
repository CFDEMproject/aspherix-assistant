# Variable Command Guidelines

Practical guidance for using Aspherix's `variable` command.
General rules (naming conventions, prefix restrictions, etc.) live in `../RULES.md` — this file is about *how* and *when* to reach for each variable style.

In practice, cases mostly need four of the available styles: `equal`, `string`, `atom`, and `boolean`.

## `equal` — single scalar value

```
variable name equal "formula"
```

Evaluates a formula to one numeric scalar, recomputed each time it's referenced.
Use for a single derived number: a group's mass, a particle count, a center-of-mass coordinate, an average velocity, etc.

```
variable particle_count equal count_particles(assembly_group,target_region)
variable total_mass equal mass(assembly_group)
```

### Prefer `variable equal` over `calculate` for one-off scalars

If a single number is needed (e.g. particle count or group mass) and it doesn't need to be tracked as its own named output over time, an `equal` variable is cheaper and simpler than setting up a full `calculate` command.
Reach for `calculate` when the value needs to be a persistent, independently-referenceable output (e.g. logged, dumped, or reused as a named result across the case) — otherwise prefer `variable equal`.

## `string` — single string value

```
variable name string "value"
```

Holds one string value and can be redefined later in the script (unlike `index`-style variables).
Use for things like file name fragments or labels that may need to change mid-script.

## `atom` — per-particle value

```
variable name atom "formula"
```

Evaluates a formula to one value per particle.
Use when a quantity needs to vary per-atom (e.g. for use in an insertion or output filter), not just as a single group-level scalar.

## `boolean` — logical condition

```
variable name boolean "formula with a logical operator"
```

Like `equal`, but the formula must contain at least one logical operator (`==`, `!=`, `<`, `<=`, `>`, `>=`, `&&`, `||`, `!`).
Use to drive `if` conditions, e.g. checking whether the system has reached a target kinetic energy before stopping.

```
variable settled boolean "ke(all,insertion_region) <= 0.001"
if "${settled}" then "quit"
```

### No spaces in function calls

Group functions used inside `equal`, `atom`, and `boolean` formulas (e.g. `count_particles(...)`, `mass(...)`, `ke(...)`) must not contain spaces — neither after commas separating arguments nor around parentheses.

Examples: (Avoid -> Prefer)
- `count_particles(assembly_group, target_region)` -> `count_particles(assembly_group,target_region)`
- `mass( assembly_group )` -> `mass(assembly_group)`

## Referencing other commands' output

`equal`, `atom`, and `boolean` formulas aren't limited to group functions (`count_particles(...)`, `mass(...)`, etc.) — they can also pull in results already produced by other commands in the script.

### `calculate` results — `id_CMDID`

A `calculate` command's result is referenced by prefixing its `id` with `id_`.
Vector results are indexed with `[N]`; mesh-averaged named properties use dot access.

```
calculate average id avg_vel quantity vx
calculate average id avg_pos quantities {y,z}

variable settled boolean "id_avg_vel <= 0.01"
variable y_pos equal id_avg_pos[1]
```

```
calculate average id mesh_avg quantity Temp
variable mesh_temp equal id_mesh_avg.Temp
```

Chaining a `calculate` into a `variable` this way is useful when the value needs a follow-up transformation (a boolean test, arithmetic with another quantity) that `calculate` alone doesn't do.

### Avoid `c_`/`f_` compute and fix references

The docs also describe `c_ID` (compute) and `f_ID` (fix) reference syntax for pulling legacy `compute`/`fix` results into a formula.
Per `../RULES.md`, `compute` and `fix` commands themselves are avoided in favor of `calculate` and native declarative commands — so these reference forms shouldn't come up in practice.
If a case still needs one, treat it as a signal that the underlying `compute`/`fix` command should be replaced with its native equivalent first, rather than reached into via a variable.

## Referencing variables

- `${name}` — immediate substitution, evaluated when the command line is parsed.
- `v_name` — deferred reference, evaluated at the point the enclosing command (e.g. `calculate`, `output_settings`) actually runs.

Use `${name}` for one-time substitution (e.g. in `print`), and `v_name` when the value needs to be re-evaluated over time (e.g. inside an output or trigger command).
