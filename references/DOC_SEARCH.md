# Searching the Public Documentation

The public Aspherix documentation ([website](https://doc.aspherix-dem.com/)) is a static Sphinx + Read the Docs site covering several products (Solver, GUI, Calibration, CFDEMcoupling), each under its own path.
This skill only deals in `.asx` input scripts, so it only ever needs the **Solver** section, at `https://doc.aspherix-dem.com/solver/` ([index](https://doc.aspherix-dem.com/solver/genindex.html)) — every URL below is relative to that path.

## Finding the right page

Command reference pages are named after the command itself: `https://doc.aspherix-dem.com/solver/<command_name>.html` (e.g. the `variable` command is at `variable.html`, `mesh_module motion` is at `mesh_module_motion.html`).
If you already know the command name, construct this URL directly instead of searching first.

If the exact command name isn't known, use `objects.inv` — the site's Sphinx object inventory — as the authoritative index of every documented page, rather than crawling `genindex.html` or pulling whole pages into a scratch file to find the right one.
It's a zlib-compressed binary file, not HTML, so a URL-fetching tool that expects renderable content (e.g. Claude Code's WebFetch) can't parse it directly; use `scripts/doc_index.py` (in this skill's own repo) to fetch and decompress it instead of reaching for inline `curl`/`python3 -c`:

```
scripts/doc_index.py          # full inventory
scripts/doc_index.py variable # only entries whose name/displayname contains "variable"
```

Each line is `name domain:role priority uri displayname`.
`std:doc` entries are full pages (`uri` is the page's `.html` filename); `std:label` entries are anchors within a page.

## Page structure

Command pages follow a consistent Sphinx layout, so name the section you need instead of asking for the whole page.
All real content lives inside `<section id="...">` blocks; everything outside them (sidebar nav, footer, prev/next links) is boilerplate and can be ignored.
The recurring sections, in order, are: `#syntax` (argument list), `#style-specific-syntax` (only on commands with sub-styles, e.g. `mesh_module_motion`'s `linear`/`rotate`/`wiggle`/... each get their own subsection), `#examples`, `#description` (semantics), `#additional-information`, `#restrictions`, `#related-commands`.
For a syntax/argument question, ask for the `Syntax` (and `Style specific syntax` if relevant) section specifically; for "how does this work" questions, ask for `Description`; for a working snippet, ask for `Examples`.

## Fetching a page

Once you've resolved the exact page and section name (above), escalate through these three strategies in order — stop at the first one that gives you a complete, accurate answer.

### Strategy 1: a fetch tool, with a verbatim-constrained prompt

Most coding-agent harnesses (Claude Code's WebFetch, Gemini CLI's web_fetch, etc.) fetch a URL through a small model that only sees the URL and the prompt you give it — it can't browse or search the site itself, starts with no context on the Aspherix DSL or this skill, and, being small, tends to summarize or paraphrase dense reference content (a full argument list, a `List_<family>`-style enumeration) rather than reproducing it exactly.
Counter that directly in the prompt:

- Name exactly what to extract (e.g. "the full syntax and all optional arguments for the `variable` command, with their defaults"), not an open-ended "summarize this page".
- Tell it not to paraphrase: *"reproduce the exact argument names, types, and defaults verbatim — do not summarize, paraphrase, or omit any entry."*
- For tabular/enumerated content, ask for a markdown table with named columns rather than prose — a table forces per-row enumeration instead of compression.

If the result still looks incomplete (an argument you expected is missing, or you got prose where you asked for a table), retry the same URL with an even narrower prompt scoped to a single argument before moving to Strategy 2 — most such tools cache by URL for a short window, so repeat asks against the same page are cheap.

Treat a Strategy 1 claim that specific content is *entirely absent* from the page with the same suspicion as an incomplete table, not as authoritative — confirmed directly: asked for a documented property-name table, got back "the page does not include this," then re-fetched the same section with `scripts/fetch_section.py` and found it present and complete.
A small fetch-model summarizing a page can wrongly report "not here" for content that plausibly belongs there, not just paraphrase what it did find.

### Strategy 2: a subagent runs `scripts/fetch_section.py`

When Strategy 1 is unavailable, or still isn't reliable enough for content where exact fidelity matters, and the harness supports spawning a subagent for a tool call (e.g. Claude Code's `Agent` tool), delegate the fetch to one rather than running it yourself.
The subagent runs:

```
scripts/fetch_section.py <url> <section-id>
```

and returns only the extracted text. `scripts/fetch_section.py <url> --list` prints every section id on a page first, if you're not sure of the exact id (see "Page structure" above for how ids map to the recurring section names).
This is a plain HTML→text extraction with no model involved anywhere in the fetch — the precision backstop when Strategy 1's summarization isn't good enough.
Running it in a subagent, rather than inline, keeps the raw HTML and script output out of your own context window; only the clean extracted text comes back.

### Strategy 3: run `scripts/fetch_section.py` yourself

If the harness has no way to spawn a subagent at all, run the same script directly instead — same command, same output as Strategy 2, just accepting that the output lands in your own context since there's no alternative.
