### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

ROOT_FOLDER=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
VENV_FOLDER=$(ROOT_FOLDER)/.venv
BIN_FOLDER=$(VENV_FOLDER)/bin

all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## Clean installation and instance
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	@rm -rf $(VENV_FOLDER) .*_cache


$(VENV_FOLDER): ## Install dependencies
	@echo "$(GREEN)==> Install environment$(RESET)"
	@uv sync

.PHONY: install
install: $(VENV_FOLDER) ## Install project dependencies

.PHONY: sync
sync: $(VENV_FOLDER) ## Sync project dependencies
	@echo "$(GREEN)==> Sync project dependencies$(RESET)"
	@uv sync

# QA
.PHONY: lint
lint: ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Lint codebase$(RESET)"
	@uv run pre-commit run -a

.PHONY: format
format: ## Check and fix code base according to Plone standards
	@echo "$(GREEN)==> Format codebase$(RESET)"
	@uv run ruff check --select I --fix --config $(ROOT_FOLDER)/pyproject.toml
	@uv run ruff format --config $(ROOT_FOLDER)/pyproject.toml

# Helpers
.PHONY: create
create: ## Create a new sketch
	@echo "$(GREEN)==> Create a new sketch for a given date $(RESET)"
	@uv run sketches create

.PHONY: create-today
create-today: ## Create a new sketch for today
	@echo "$(GREEN)==> Create a new sketch for today $(RESET)"
	@uv run sketches create today

.PHONY: run-today
run-today: ## Run today's sketch
	@echo "$(GREEN)==> Run today's sketch $(RESET)"
	@uv run py5-live-coding "$$(uv run sketches path today)"

.PHONY: publish-today
publish-today: ## Publish today's sketch
	@echo "$(GREEN)==> Publish today's sketch $(RESET)"
	@uv run sketches all today
