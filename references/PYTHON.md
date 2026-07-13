# Python

Guidance for any Python script this skill runs or writes — mesh generation, input pre-processing, post-processing plots, or anything else — not specific to any one of those use cases.

## Respect the existing environment

Check what's already set up before running or installing anything, and use whatever's already there rather than assuming a bare `python`/`pip` is the right entry point.

- Look for `uv.lock`/`pyproject.toml` (uv), a `.venv`/`venv` directory, a `Pipfile` (pipenv), or an `environment.yml` (conda/mamba).
- If the project uses `uv`, run scripts via `uv run ...` rather than invoking `python` directly.
- If a `.venv`/`venv` exists without `uv`, use its interpreter (e.g. `.venv/bin/python`) rather than the system one.
- If nothing project-specific exists, check whether a virtual environment is already active (`$VIRTUAL_ENV`, `$CONDA_DEFAULT_ENV`) before falling back to the system interpreter.

## Never install globally

Do not `pip install` (or equivalent) into the system/global Python.
If a script needs a package that isn't available in whatever environment applies (above), create an isolated environment for it first — e.g. `uv venv` (or let `uv run` manage it automatically via inline script dependencies), or `python -m venv` — rather than installing globally.

If it's genuinely unclear what environment tooling is available or expected, ask rather than silently defaulting to a global install.
