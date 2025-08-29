.PHONY: format lint typecheck test run coverage precommit-install precommit-run docker-build run

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
	PYTHONPATH=src/ poetry run streamlit run src/app/main.py --server.address=0.0.0.0 --server.port=8501

precommit-install:
	poetry run pre-commit install
	poetry run pre-commit install -t pre-push

precommit-run:
	poetry run pre-commit run --all-files

docker-build:
	docker build -t Q&A-law:latest .
