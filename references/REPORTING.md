# Reporting

After building or modifying a case setup, report back to the user in plain terms — don't just hand over files silently.
The goal is that someone reviewing the work can tell what was built and trust it without having to re-derive it from the `.asx` script.

Reporting is on by default: produce a report even if the user didn't ask for one, and even if the surrounding workflow doesn't itself require one.

In an unattended/automated context — a subagent, an autonomous run, anything where whoever reviews the output wasn't present for the conversation — reporting is mandatory, not just default: there's no one to ask a follow-up, so the report is the only record of what happened and why. In an interactive session with the user present, they can still explicitly opt out of a report for a given task (e.g. during rapid iteration where they just want the file); absent that, the default still applies.

In an interactive session, default to reporting this as a normal reply.
Write it to a file instead when the surrounding workflow explicitly calls for one (e.g. a test harness that expects a summary artifact), the user asks for one, or the content itself doesn't fit a chat reply (e.g. generated plots, large tables — see "Where results go" below).

Whenever none of those triggers apply and the report stays a normal reply, always close by offering to save it to a file — this is not optional or situational, do it every time. Don't write the file unprompted; just ask.

In an unattended/automated context there is no chat reply anyone will see, so a file is the only sensible destination — write the report to a file even if nothing above would otherwise have called for one.

Don't invent a fixed filename or folder convention on your own in any of these cases — match what the workflow/user expects, or otherwise pick something sensible for the case at hand.

## Granularity

Whether reporting happens per case, or as a single consolidated summary, depends on context — there is no fixed rule.
A single case built in isolation gets one report for that case.
A workflow touching multiple components or multiple cases (e.g. several variants of one case, or several cases in one session) may warrant one report per case, or one combined summary covering all of them — judge which is more useful for the reviewer to skim given how the work is organized, and be consistent about it within a session.

## Content and format

The following is the default content and structure — the user can override it for a given task or session, either by adding to it (e.g. an extra category to always cover) or replacing it outright with their own format.
Once overridden, follow the override rather than reverting to the default on the next case.

Cover, in plain language:

- What the case sets up — the physical setup, not a line-by-line script narration.
- Any assumption made to fill a gap the request left underspecified (a value, a shape, a mechanism it didn't pin down), and why that choice was reasonable.
- Any place the request was ambiguous and how it was interpreted.
- Any deviation from what was literally asked for, and why (e.g. a command limitation forced a different approach — see `POST_PROCESSING.md` for an example).
- Whether the script was actually run, and the outcome: ran to completion, or a solver/setup error and what it said.
If it wasn't run (e.g. the `aspherix` executable isn't available), say so instead of leaving it unstated.
- If the run produced results — a tracked quantity, a `calculate`-derived metric, a notable value from the post-processing output (see `POST_PROCESSING.md`) — report what running it actually showed, not just that it completed.

If nothing was ambiguous, assumed, or deviated from, say so explicitly rather than omitting the section — an empty section reads as "not checked", not "nothing to report".

### Where results go

Whether results are folded into the same report or broken out separately (e.g. a dedicated results section, or a separate file for a case with substantial post-processing output like plots or tables) depends on context, same as granularity above.
A small single case's results fit fine inline with the rest of its report.
A case with heavier post-processing (multiple tracked metrics, generated plots, per-variant comparisons) may warrant separating results out so the setup report stays skimmable — judge what's reasonable given how much there is to show, rather than defaulting to either extreme.

This applies to any case-building work, not just first-time setups — the same categories apply when modifying an existing case (what changed, why, and whether it was re-verified).
