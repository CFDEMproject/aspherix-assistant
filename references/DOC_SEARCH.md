# Searching the Public Documentation

The public Aspherix documentation ([website](https://doc.aspherix-dem.com/), [index](https://doc.aspherix-dem.com/genindex.html)) is a static Sphinx + Read the Docs site.

## Finding the right page

Command reference pages are named after the command itself: `https://doc.aspherix-dem.com/<command_name>.html` (e.g. the `variable` command is at `variable.html`, `mesh_module motion` is at `mesh_module_motion.html`).
If you already know the command name, construct this URL directly instead of searching first.

If the exact command name isn't known, use `objects.inv` — the site's Sphinx object inventory — as the authoritative index of every documented page, rather than crawling `genindex.html` or pulling whole pages into a scratch file to find the right one.
It's a zlib-compressed binary file, not HTML, so a URL-fetching tool that expects renderable content (e.g. Claude Code's WebFetch) can't parse it directly; fetch and decompress it with a shell command instead:

```
curl -s https://doc.aspherix-dem.com/objects.inv -o /tmp/objects.inv
python3 -c "import zlib; d=open('/tmp/objects.inv','rb').read(); print(zlib.decompress(d.split(b'\n',4)[4]).decode())"
```

Each line is `name domain:role priority uri displayname`.
`std:doc` entries are full pages (`uri` is the page's `.html` filename); `std:label` entries are anchors within a page.

## Fetching a page

Most coding-agent harnesses (Claude Code's WebFetch, Gemini CLI's web_fetch, etc.) fetch a URL through a small subagent that only sees the URL and the prompt you give it — it can't browse or search the site itself, and it starts with no context on the Aspherix DSL or this skill.
Once you've resolved the exact page (above), pass that URL with a narrow, specific prompt naming exactly what to extract (e.g. "list the full syntax and all optional arguments for the `variable` command, with their defaults"), not an open-ended "summarize this page".
A vague prompt on a large reference page tends to make the subagent return either too little (missing an argument you needed) or the whole page verbatim — which is how full pages end up dumped into scratch files instead of just the answer.

If the harness has no such fetch tool at all, `curl` the page and extract the relevant section directly (e.g. `curl -s <url> | lynx -dump -stdin` or similar) rather than dumping the raw HTML into context or a scratch file.
