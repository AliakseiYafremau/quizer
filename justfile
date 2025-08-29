[private]
@default:
    just --list


# Setup environment
@setup:
    uv sync
    uv pip install -e .


# Run tests
@test:
    pytest


# Run coverage
@coverage:
    coverage run -m pytest
    coverage html


# Run linter and formatter
@lint:
    ruff format
    ruff check --fix
    mypy .