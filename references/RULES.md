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
