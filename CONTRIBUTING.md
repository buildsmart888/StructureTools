# Contributing

## Development Environment

1. Create and activate a virtual environment.
2. Install with dev extras:
```bash
pip install -e .[dev]
```
3. Install pre-commit hooks:
```bash
pre-commit install
```

## Tests
Run all tests:
```bash
pytest -q
```

## Lint & Type Check
```bash
ruff check .
ruff format --check .
mypy freecad/StructureTools/core
```

## Typing Policy

## Pull Requests

## Commit Messages

Follow Conventional Commits where practical (feat:, fix:, refactor:, test:, docs:, chore:).

## Code Style

Ruff rules enforce consistency; run `ruff check --fix .` before committing if needed.

Thanks for contributing!
