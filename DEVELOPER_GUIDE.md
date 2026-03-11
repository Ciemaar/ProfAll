# Developer Guide

Welcome to the `profall` repository! This guide will help you set up your development environment.

## Requirements

1. Python >= 3.12
1. Docker Compose
1. Hatch (`pip install hatch`)
1. Tox (`pip install tox`)

## Local Development

All build tools, configurations, dependencies, and rules are located strictly in `pyproject.toml`.

To set up an editable environment with dev tools:

```bash
pip install -e ".[dev]"
```

## Running Tests

We use `pytest` for all unit testing. To ensure you have an active database for local testing, start the ephemeral server:

```bash
docker-compose up -d
```

Run tests with `tox`:

```bash
tox
```

Or directly with pytest and coverage metrics:

```bash
pytest --cov=src/profall --cov-report=term-missing
```

### Coverage Rules

Coverage must be maintained at **>95%**. This is strictly enforced in PR reviews.

## Code Quality

We use `ruff` exclusively for formatting and linting. Type-checking defaults to `pyright`.

```bash
ruff format src/ tests/
ruff check src/ tests/
pyright src/ tests/
```

We also enforce MD formatting:

```bash
mdformat **/*.md
```

## Pull Requests

Before submitting a pull request, ensure `pre-commit` runs flawlessly.

To set up pre-commit:

```bash
pre-commit install
```
