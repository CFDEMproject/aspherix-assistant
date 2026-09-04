# RULES

## Aspherix Input Scripts Format

Aspherix input scripts uses the `.asx` suffix.
Avoid using the older LIGGGHTS `in.` prefix for input scripts.

## Aspherix Native Syntax

Always prefer to use newer native Aspherix *natural language* syntax over the older LIGGGHT-style commands.
Mixing old-style and new-style commands will often produce errors.

### No `fix` commands

Legacy LIGGGHTS-style `fix <id> <group-id> <style> ...` commands should **always** be avoided.
Prefer to use Aspherix's native declarative commands instead.

Examples:
- `fix <id> <group> move/mesh ...` -> `mesh_module motion ...`

### No `compute` commands, prefer `calculate` commands

Legacy LIGGGHTS-style `compute <id> <group-id> <style> ...` commands should be avoided.
Prefer to use Aspherix's native `calculate` commands instead.

Examples: (Avoid -> Prefer)
- `compute <id> <group> reduce [min|max|sum|ave] ...` -> `calculate [minimum|maximum|sum|average] ...`
- `compute <id> <group> com ...` -> `calculate center_of_mass ...`

### Prefer `define_group`, avoid `group`

Prefer the newer Aspherix's native `define_group` command over the older LIGGGHT-style `group` command.

### Always use `simulate`, avoid `run` commands

Legacy LIGGGHTS-style `run` commands shoud **always** be avoided.
Always use the Aspherix's native `simulate` command.

### Prefer `output_settings`, avoid `dump` commands

Legacy LIGGGHTS-style `dump` commands shoud be avoided.
Prefer to use the Aspherix's native `output_settings` command for generating output.

## Command Ordering and Cross-Command Dependencies

Several commands only work once others have already been declared, and the error you get often doesn't name the missing command directly - confirmed repeatedly by hitting the actual error rather than reading ahead:

- `particle_shape` must be declared before `simulation_domain` (and before any other command that creates the simulation box).
- `material_interaction_properties` must be declared before `particle_contact_model`/`wall_contact_model` reference the materials involved.
- A mesh with `solid yes` is not on its own enough to make it act as a wall in the simulation - `wall_contact_model` (a separate command from `particle_contact_model`, which only governs particle-particle contact) must also be declared, or Aspherix rejects every mesh at `simulate` time ("mesh `<id>` should be used for either insertion, wall or massflow measurement").
- `enable_gravity` is not on by default - required for any real dynamics, including `simulate mode until_filled`/`until_settled`.
- A material's own self-interaction (friction, restitution, etc. against itself) belongs on `material_properties`, not `material_interaction_properties` (which is only for a *pair* of distinct materials and errors with "materials are identical" otherwise).
  All materials need a matching *count* of properties declared, even ones that never actually contact each other in the case.

## Default Values

Always prefer to use default values for commands when they are available.
Only override default values if it is required.

The exception here is `id`: give a command a descriptive `id` whenever its result needs to be referenced elsewhere (a `calculate`, `check_timestep`, or similar command — see `commands/variable.md` for the `id_` reference syntax this enables). `output_settings` is a case where this exception usually doesn't apply — its output is normally consumed by ParaView, not referenced by `id_` from another command — so using the `id` keyword there is generally not required.

## Naming Convention

Use descriptive names for variables and commands.
Choose a consistent style and stick to it.
Avoid short and ambiguous names, avoid prefixes.

`id_`, `v_`, `f_` and `c_` are reserved reference prefixes: Aspherix prepends them automatically when a command's result, a variable, a fix, or a compute is referenced elsewhere (e.g. a `calculate` command with `id avg_vel` is referenced as `id_avg_vel`; a variable named `count` is referenced as `v_count`) — see `commands/variable.md` for the full reference syntax.
This is not a naming style you opt into; don't manually choose an `id`/variable name that itself starts with one of these strings (e.g. don't name a variable `v_count`), since that just produces a confusing doubled-up reference (`v_v_count`) rather than disambiguating anything.

## Simulation Output

Simulation output may create a lot of data.
Be considerate with output intervals, especially with large simulations with long run times.

The same is true for restart files.

The two output intervals differ hugely in cost, so don't set them to the same cadence by default.
`write_output_timestep` (see `commands/output_settings.md`) writes a full per-particle/per-mesh snapshot each time, so it's the one to be conservative with.
`write_to_terminal_timestep` (see `commands/status.md`) writes a handful of scalars to the terminal/log/CSV, so it's cheap enough to sample much more often — and doing so is genuinely useful, since it's what makes a running simulation's log file and CSV time series usable for monitoring and runtime analysis.
As a rule of thumb, set `write_to_terminal_timestep` to a smaller value than `write_output_timestep` rather than deriving one from the other or leaving both at the same cadence.

## Timestep Criteria

Large timesteps may cause numerical instability.
Refer to the `check_timestep` command.

## Cross-script Parameter Consistency

Shared parameters (e.g. `simulation_timestep`) across split scripts (`init.asx`, `main.asx`, ...) aren't enforced automatically — confirm they still match before running.

This includes a stop condition expressed as "N% of an earlier state" (e.g. a settled particle/mass count from a prior `fill`-style script) — Aspherix's variable system cannot snapshot a value from earlier in the *same* script for later comparison either, let alone across scripts (referencing one variable from inside another's formula either crashes at evaluation via `${name}`, or silently re-evaluates live every time via `v_name` — neither freezes a value; see `commands/variable.md`).
This kind of threshold has to be computed externally, from the prior script's *actual* achieved output, and hardcoded - never derived from the originally intended target.
Confirmed directly: a threshold sized for an intended count that insertion didn't fully reach (see `strategies/STRATEGIES.md`'s packing-generator entry) made `simulate mode until_condition_reached` satisfy on its very first check - no error, just a silent early exit that looks like the run did nothing.

A threshold on an *extensive* quantity — total `ke(...)`, total mass, a particle count — must likewise be rescaled whenever the particle count is, since it states a total over the system rather than a per-particle condition.
Derive it as `<per-particle value> * <this script's actual count>`, or avoid the problem with an intensive criterion — `simulate mode until_settled` breaks on a velocity threshold, which holds at any scale.

State handed between scripts needs the same care: `read_restart` reads whatever file is at the path, with no record of what wrote it (`read_restart.html`), so record provenance beside it — script, achieved count, timestamp — and check that before the phase that consumes it.
Write intermediate restarts during long runs, since one reached only at the end is lost if the run is aborted.
