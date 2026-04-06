# ProfAll Modernization Session Prompt

## Overall Goal

Modernize the `ProfAll` repository to adhere strictly to modern Python architectural, tooling, and stylistic rules while maintaining its core capability as a nearly zero-overhead `.pth` global execution hook.

## Tasks Completed

1. **Architecture and Configuration**

   - Transferred project structure to a `src/profall/` package layout.
   - Replaced legacy `setup.py` and `requirements.txt` with a centralized `pyproject.toml` using the `hatchling` build backend.
   - Grouped all development dependencies under the `[project.optional-dependencies] dev` block.

1. **Core Refactoring**

   - Upgraded from legacy `influxdb` to the modern `influxdb-client` (v2 API).
   - Moved `.pth` injection/removal logic out of manual setup files and into a fully typed `click` CLI application.
   - Refactored `profall.py` to `src/profall/core.py` utilizing Python 3.12+ features.
   - Guaranteed the `.pth` hook preserves a minimal execution path by enforcing lazy imports on all heavy external libraries and configurations.

1. **Tooling and Quality**

   - Enforced formatting and linting exclusively via `ruff`.
   - Setup `pyright` for strict type checking.
   - Configured `mdformat` to handle strictly 80-character wrapped Markdown.
   - Established `.pre-commit-config.yaml` to run `ruff`, `pyright`, `pytest`, `mdformat`, and `codespell` locally.

1. **Testing**

   - Wrote comprehensive tests with `pytest` utilizing `unittest.mock` isolating external behaviors.
   - Added an ephemeral `docker-compose.yml` for InfluxDB integration testing.
   - Exceeded the 95% threshold requirement by reaching 99% test coverage.
   - Setup cross-environment compatibility checks using `tox`.

1. **CI/CD Configuration**

   - Created `.github/workflows/ci.yml` running the complete quality suite (ruff, pyright, mdformat) and `pytest` (with ephemeral containers) across Python 3.12, 3.13, and 3.14 on all PRs/Pushes to main.

1. **Documentation**

   - Wrote descriptive `pydocstyle` compliant docstrings.
   - Rebuilt `README.md`, `USER_GUIDE.md`, and `DEVELOPER_GUIDE.md` files.
   - Introduced `AGENTS.md` explicitly defining critical architectural constraints, lazy loading requirements, and session prompt continuation.
   - Minimized and modernized the ad-hoc scripts relocating them to `scratch/` and removing dynamic username limitations.

## Key Learnings

- **Lazy Imports**: Python `.pth` startup scripts necessitate extremely careful import discipline. External packages (even seemingly minor ones) must be imported locally inside execution functions rather than at the module scope to preserve global performance.
- **InfluxDB API**: InfluxDB v2 shifted from a direct write syntax to a synchronous/asynchronous batch API format utilizing `.tag()` and `.field()` builder methods inside `WriteAPI`.
- **Pytest Testing Path Overrides**: To test modules that interact with `__main__` behavior, relying directly on `sys.modules` overriding is fragile. Pathing the file reading logic to directly leverage the host's absolute path via `Path(__file__)` works around location-dependent pytest context errors.
