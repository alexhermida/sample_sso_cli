SHELL := /bin/bash
PKG_SRC :=	src
TEST_SRC :=	tests


.PHONY: venv
venv: # Create Python virtual environment
	python -m venv .venv

.PHONY: lint
lint: ## Run lint checks
	isort --check-only $(PKG_SRC) tests
	ruff $(PKG_SRC) tests
	black --check $(PKG_SRC) tests
	mypy --ignore-missing-imports --no-warn-no-return --show-error-codes --allow-redefinition src


.PHONY: tests
tests: ## Run unit tests
	pytest $(TEST_SRC) -s