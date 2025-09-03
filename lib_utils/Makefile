.PHONY: install format lint typecheck

install:
	poetry install

format:
	poetry run black --line-length 100 src

lint:
	poetry run ruff check src

typecheck:
	poetry run mypy src

all: install format lint typecheck
