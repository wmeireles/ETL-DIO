.PHONY: help install test lint run-mock run-real clean mock-server

help:
	@echo "Comandos disponíveis:"
	@echo "  make install      - Instala dependências"
	@echo "  make test         - Executa testes"
	@echo "  make lint         - Executa linter"
	@echo "  make run-mock     - Executa ETL em modo mock"
	@echo "  make run-real     - Executa ETL em modo real"
	@echo "  make mock-server  - Inicia mock server"
	@echo "  make clean        - Remove arquivos temporários"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=src.etl --cov-report=term-missing

test-quick:
	pytest tests/ -v

lint:
	flake8 src/ tests/

run-mock:
	python -m src.etl.main --csv SDW2023.csv --mode mock

run-real:
	python -m src.etl.main --csv SDW2023.csv --mode real

run-dry:
	python -m src.etl.main --csv SDW2023.csv --mode mock --dry-run

mock-server:
	python scripts/mock_server.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
