# Insertion

Strategies for getting particles into a case reliably — picking the right `simulate` mode for how they were inserted, confirming a `pack` actually hit its target, and reaching a high cumulative target without retrying `pack`.

## `simulate mode until_filled`/`until_settled` - pick the mode that matches the insertion style

See `simulate.html` for what each mode actually checks - don't guess from the name.
In short: `until_filled` assumes a `pack`-then-`stream` pattern and is not a fit for a one-shot `pack` (use `until_settled` instead) or for a `rate_in_region` insertion with its own `target_particle_count`/`target_mass` (use a separate `until_condition_reached` on that target, then `until_settled` - `until_settled`'s own convergence check is not reliable while insertion is still running, per its documented note).

## Verify a `pack` insertion actually reached its target

See `insertion.html` for the `packing_generator` styles (`simple`/`dense`/`batch`) and the `dense`/`dense_experimental` volume-fraction ceiling.
`dense`'s undershoot tracks the resulting **volume fraction** (particle volume / region volume), not the raw target count - a higher target that also raises the volume fraction can converge *closer* to target, not further from it, matching the tool's own low-volume-fraction warning (below 5%, prefer `simple` instead) - so don't assume a bigger ask must undershoot proportionally worse.
Whichever style is used, check the actual inserted count against the target afterward rather than assuming it was met (see `RULES.md`'s "Cross-script Parameter Consistency" for why that matters downstream).

## Reaching a high cumulative insertion target - don't retry `pack`

A single one-shot `pack` insertion can't reach a high enough target on its own (see above), and retrying `pack` itself toward a region-occupancy target is a trap once particles are meant to leave the region after settling - see `insertion_pack.html`/`insertion_rate_in_region.html` for why.
Use `mode rate_in_region` with `insert_every_time` instead (self-limits correctly via a genuine cumulative `target_particle_count`/`target_mass`), sized as a recipe rather than guessed:

1. Pulse interval = region depth (fall direction) / insertion velocity, so each pulse clears the region before the next fires.
2. Max feasible volume fraction per pulse ~20-30% (`rate_in_region` has no `packing_generator`, so it saturates via plain random sequential placement well below a packed bed) - verify against a real run rather than trusting the estimate.
3. Pulse rate sized to request the full remaining target each pulse.
4. Number of pulses = target volume fraction / that per-pulse ceiling, with a safety margin, rounded up.
5. Bound the insertion with a fixed-time window sized from that pulse count, `disable_command` it, and only then call `simulate mode until_settled` - see `simulate.html` for why a still-active insertion isn't safe to leave running into it.
