.PHONY: format lint typecheck

format:
	poetry run black --line-length 100 src

lint:
	poetry run ruff check src

typecheck:
	poetry run mypy src

all: format lint typecheck
