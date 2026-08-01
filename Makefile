.PHONY: help install setup format lint test clean pre-commit-install pre-commit-run

# Variables
PYTHON := python
PIP := $(PYTHON) -m pip
PRECOMMIT := $(PYTHON) -m pre_commit

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

setup: install pre-commit-install ## Configuración completa del entorno
	@echo "Entorno configurado correctamente"

pre-commit-install: ## Instalar pre-commit hooks
	$(PRECOMMIT) install
	@echo "Pre-commit hooks instalados"

pre-commit-run: ## Ejecutar pre-commit en todos los archivos
	$(PRECOMMIT) run --all-files

pre-commit-update: ## Actualizar versiones de pre-commit hooks
	$(PRECOMMIT) autoupdate

format: ## Formatear código con Black e isort
	black .
	isort .
	@echo "Código formateado"

lint: ## Analizar código con Ruff
	ruff check .
	@echo "Análisis completado"

lint-fix: ## Analizar y corregir automáticamente
	ruff check --fix .
	@echo "Problemas corregidos automáticamente"

security: ## Análisis de seguridad con Bandit
	bandit -c pyproject.toml -r .
	@echo "Análisis de seguridad completado"

typecheck: ## Verificar tipos con mypy
	mypy .
	@echo "Verificación de tipos completada"

test: ## Ejecutar tests con pytest
	pytest -v
	@echo "Tests ejecutados"

test-cov: ## Ejecutar tests con cobertura
	pytest -v --cov=. --cov-report=html --cov-report=term-missing
	@echo "Reporte de cobertura generado en htmlcov/"

notebook-format: ## Formatear notebooks
	nbqa black .
	nbqa isort .
	@echo "Notebooks formateados"

notebook-clean: ## Limpiar outputs de notebooks
	nbstripout **/*.ipynb
	@echo "Notebooks limpiados"

clean: ## Limpiar archivos temporales
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	@echo "Archivos temporales eliminados"

all: format lint test ## Formatear, analizar y testear

check: format lint security typecheck test ## Verificación completa del código

verify: pre-commit-run test ## Verificación rápida (pre-commit + tests)
