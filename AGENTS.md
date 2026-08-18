# Agent Instructions for ProfAll

1. **Repository Context (ProfAll)**:

   - `profall` is a global Python profiler that uses a `.pth` hook installed in site-packages to record execution telemetry and reports it to InfluxDB v2 using `influxdb-client`.

1. **Session Summarization**:

   - Each session should be summarized in a `session_prompt.md` file (or similar session prompt file) that records what was done in the session in the form of a prompt.
   - This file should be updated as the instructions and goals are clarified throughout the session.

1. **Execution Commands**:

   - Setup dev environment with `pip install -e ".[dev]"`.
   - Start the ephemeral test database with `docker-compose up -d`.
   - Run tests with `pytest --cov=src/profall --cov-report=term-missing` or `tox`.

1. **Project Architecture Rules**:

   - Use `src/<package_name>` layout.
   - Exclusively use `pyproject.toml` as the single source of truth (no `setup.py`, `setup.cfg`, `requirements.txt`, or `tox.ini`).
   - Put dev tools in `[project.optional-dependencies] dev` group.
   - Use `hatchling` as the build backend.

1. **Minimal Imports in Critical Path (`profall.core` and `profall.hook`) (Project Exception Rule)**:

   - The hook loaded via `profall.pth` is evaluated every time Python starts up on the user's system.
   - You MUST keep imports in this critical path to an absolute minimum to minimize Python startup overhead.
   - Specifically, **DO NOT import heavy libraries** (like `pydantic-settings` or `pydantic`) at the module level. DO NOT use them for environment configuration in this project.
   - Any heavy library or configuration parsing must be deferred until it is absolutely necessary (e.g., inside functions that only run when a profiling or execution mode is active).

1. **Quality & Tooling Preferences**:

   - Use `click` exclusively for CLIs.
   - Use `ruff` for linting/formatting.
   - Use `pyright` for type checking.
   - Use `mdformat` for Markdown (80-character wrap).
   - Use `codespell` for spelling.
   - Enforce checks locally via `pre-commit`.

1. **Coding Standards**:

   - Write for Python 3.12/3.13+.
   - Use modern typing (built-in generics and `|` operator, avoid importing from `typing`, no `Any`).
   - Strictly use `pathlib.Path` for file operations.
   - Use context managers for cleanup.

1. **Testing & CI Standards**:

   - Use `pytest` with `unittest.mock` for isolation.
   - Maintain >95% test coverage via `pytest-cov`.
   - Orchestrate cross-environment tests with `tox`.
   - Use `docker compose` to spin up ephemeral external servers for tests.
   - Require GitHub Actions for CI.

1. **Documentation Standards**:

   - Maintain `README.md`, `USER_GUIDE.md`, and `DEVELOPER_GUIDE.md`.
   - Docstrings are strictly enforced on all modules, classes, and methods using Ruff's pydocstyle D ruleset without placeholder text.

Follow these rules unconditionally for any enhancements to this repository.
