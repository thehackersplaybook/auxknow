# IsoPrompt - Makefile for build automation

# Colors
BLUE=\033[0;34m
YELLOW=\033[1;33m
RED=\033[0;31m
GREEN=\033[0;32m
RESET=\033[0m

.PHONY: help install install-dev clean format lint test validate build publish version

help:
	@echo "$(BLUE)AuxKnow - Available Make Targets$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-20s$(RESET) %s\n", $$1, $$2}'

install: ## Install package in development mode
	@echo "$(YELLOW)Installing auxknow in development mode...$(RESET)"
	python -m pip install -e .

install-dev: ## Install package with development dependencies
	@echo "$(YELLOW)Installing auxknow with development dependencies...$(RESET)"
	python -m pip install -e ".[dev]" build twine pytest-cov

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

format: ## Format code using black and isort
	python -m black auxknow/
	python -m isort auxknow/

lint: ## Run linters (flake8, mypy)
	python -m flake8 auxknow/ --max-line-length=88 --extend-ignore=E203,W503,E501,D100,D200,D202,D205,W293,W291,E722
	python -m mypy auxknow/ --ignore-missing-imports

test: ## Run tests with pytest
	python -m pytest tests/ -v --cov=auxknow --cov-report=term-missing

validate: clean format lint ## Run all validation steps

build: clean ## Build package distributions
	python -m build

all: clean format lint validate build publish

publish: ## Publish package to PyPI
	@echo "$(YELLOW)Building distributions...$(RESET)"
	python -m build
	@echo "$(YELLOW)Publishing to PyPI...$(RESET)"
	python -m twine upload dist/*

version: ## Show package version
	@if [ -f "auxknow/__init__.py" ]; then \
		echo "Package version: $$(python -c 'import auxknow; print(auxknow.__version__)')"; \
	else \
		echo "$(RED)Error: auxknow/__init__.py not found.$(RESET)"; \
		exit 1; \
	fi 