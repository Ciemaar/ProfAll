# Agent Instructions for ProfAll

1. **Minimal Imports in Critical Path (`profall.core` and `profall.hook`)**:

   - The hook loaded via `profall.pth` is evaluated every time Python starts up on the user's system.
   - You MUST keep imports in this critical path to an absolute minimum.
   - Specifically, **DO NOT import heavy libraries** (like `pydantic-settings` or `pydantic`) at the module level.
   - Any heavy library or configuration parsing must be deferred until it is absolutely necessary (e.g., inside functions that only run when a profiling or execution mode is active).

1. **Project Architecture**:

   - This project strictly uses `pyproject.toml` as the single source of truth for dependencies, build settings, tools, and scripts.
   - Tests are run via `pytest` and `tox`.
   - Linter, formatter, and type-checker is `ruff` and `pyright`.
   - Do not re-introduce `setup.py`, `setup.cfg`, `requirements.txt`, or `tox.ini`.

1. **Database Client**:

   - The system utilizes the modern `influxdb-client` (v2 API) to send execution telemetry.

Follow these rules unconditionally for any enhancements to this repository.
