# Contributing to SchemaGuard

First off, thanks for taking the time to contribute!

## Setup Development Environment
```bash
git clone git@github.com:RosenFFF/SchemaGuard.git
cd SchemaGuard
pip install -e '.[dev]'
```

## Running Tests
We use pytest for our testing framework.
```bash
python -m pytest
```

## Code Style
We use `ruff` for linting and formatting.
```bash
ruff check .
ruff format .
```

## Commit Messages
We follow conventional commits format. For example:
- `feat: add new feature`
- `fix: resolve bug`
- `docs: update documentation`
- `test: add missing tests`

## Pull Request Process
1. Create a new branch from `main`.
2. Make your changes and write tests.
3. Ensure all tests pass.
4. Submit a Pull Request with a clear description.

## Issue Reporting Guidelines
Please use the issue tracker to report bugs or suggest features. Be clear and provide reproducible steps when reporting a bug.
