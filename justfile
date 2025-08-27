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


# Run linter and formatter
@lint:
    ruff format
    ruff check --fix
    mypy .