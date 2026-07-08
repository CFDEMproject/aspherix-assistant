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

The exception here is `id` where using a descriptive name for each command is considered good practice.

## Naming Convention

Use descriptive names for variables and commands.
Choose a consistent style and stick to it.
Avoid short and ambiguous names, avoid prefixes.

Aspherix uses `id_`, `v_`, `f_` and `c_` to disambiguate command names, variable names, fix names and compute names.
These prefixes MUST always be avoided

## Simulation Output

Simulation output may create a lot of data.
Be considerate with output intervals, especially with large simulations with long run times.

The same is true for restart files.

## Timestep Criteria

Large timesteps may cause numerical instability.
Refer to the `check_timestep` command.
