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

all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.venv/bin/pip:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	python3 -m venv .venv
	.venv/bin/pip install -U pip wheel


.PHONY: install
install: .venv/bin/pip ## Install Py5 and dependencies
	.venv/bin/pip install -r requirements.txt

.PHONY: clean
clean: ## Remove old virtualenv
	@echo "$(RED)==> Cleaning environment and build$(RESET)"
	rm -rf .venv pyvenv.cfg
