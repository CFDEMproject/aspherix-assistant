# `while` Command Guidelines

`while`/`do`/`done` (`while_do.html`) is Aspherix's native do-while loop - the replacement for old LIGGGHTS `label`/`jump`/`loop` - and should be preferred per `RULES.md`'s "Aspherix Native Syntax" rule.

## Syntax

```
while boolean do
  t1
  t2
  ...
done
```

`boolean` is a quoted condition (see the `if` command's description for the boolean-expression grammar), typically referencing `equal`-style variables via `$name`/`${name}` immediate substitution.
These are re-evaluated fresh on every pass through the loop, not fixed once at parse time - confirmed directly against the documented examples, where a loop variable incremented inside the body changes the next pass's condition result.

`t1, t2, ..., tN` are one or more plain Aspherix commands, each on its own line.
Do NOT join separate body statements with a trailing `&` the way `if (...) then "cmd1" "cmd2" ...` does, and do not quote each one as if passing a command list.
Confirmed directly: joining a while body's separate statements with `&` (borrowing the `if...then` continuation style) silently mis-parses them into one malformed command - no error is raised, but the loop body's intended commands (e.g. a `simulate` call) never actually execute.
In a CFD-coupled case (`enable_cfd_coupling`) this manifests as a hang, with the CFD side waiting on a `simulate` call that never fires, rather than an obvious parse error - so an apparently-correct-looking while loop is a plausible root cause for that symptom.
A command that itself genuinely needs multiple lines (e.g. a long `mesh` command) still uses `&` normally *within* that one statement - the rule is "no `&` between separate body statements", not "no `&` at all inside a while body".

## Example

```
variable t_elapsed equal 0
variable t_total   equal 1
variable dt_chunk  equal 5e-4
while "${t_elapsed} < ${t_total}" do
    simulate time ${dt_chunk}
    set group some_group some_property 0
    variable t_elapsed equal ${t_elapsed}+${dt_chunk}
done
```

## Related commands

See `strategies/STRATEGIES.md`'s "Continuously resetting a built-in per-particle property for particles in a region" entry for a full worked pattern built on this loop plus `define_group`'s `update_every_time`.
