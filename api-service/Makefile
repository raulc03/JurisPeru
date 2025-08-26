.PHONY: format lint typecheck test run coverage precommit-install precommit-run docker-build

format:
	poetry run black --line-length 100 src tests
	poetry run ruff format src tests

lint:
	poetry run ruff check src tests

typecheck:
	poetry run mypy src

test:
	poetry run pytest tests --cov=src --cov-report=term-missing --cov-fail-under=70

coverage:
	poetry run pytest tests --cov=src --cov-report=html --cov-fail-under=70

run:
	poetry run uvicorn src.app.main:app --host 0.0.0.0 --reload

precommit-install:
	poetry run pre-commit install
	poetry run pre-commit install -t pre-push

precommit-run:
	poetry run pre-commit run --all-files

docker-build:
	docker build -t 02_project:latest .
