.PHONY: install format lint typecheck test run coverage

install:
	poetry install

format:
	poetry run black --line-length 100 src

lint:
	poetry run ruff check src

typecheck:
	poetry run mypy src

run:
	poetry run prefect server stop
	nohup poetry run prefect server start &
	poetry run python src/pipelines/orchestration/pipeline.py

all: install format lint typecheck
