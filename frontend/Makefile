.PHONY: install format lint typecheck test run coverage

install:
	poetry install

format:
	poetry run black --line-length 100 src tests

lint:
	poetry run ruff check src tests

typecheck:
	poetry run mypy src

test:
	poetry run pytest tests --cov=src --cov-report=term-missing --cov-fail-under=70

coverage:
	poetry run pytest tests --cov=src --cov-report=html --cov-fail-under=70

run:
	PYTHONPATH=src/ poetry run streamlit run src/app/main.py --server.address=0.0.0.0 --server.port=7860

all: install format lint typecheck test
