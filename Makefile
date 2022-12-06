#!make
#----------------------------------------
# Settings
#----------------------------------------
.DEFAULT_GOAL := help
#--------------------------------------------------
# Variables
#--------------------------------------------------
PACKAGE=biomage_programmatic_interface

#--------------------------------------------------
# Targets
#--------------------------------------------------
install: clean ## Creates venv and installs the package
	@echo "==> Creating virtual environment..."
	@python3 -m venv venv/
	@venv/bin/pip install flake8
	@venv/bin/pip install black
	@venv/bin/pip install isort
	@echo "    [✓]"
	@echo

	@echo "==> Installing utility and dependencies..."
	@venv/bin/pip install --upgrade pip
	@venv/bin/pip install -e .
	@echo "    [✓]"
	@echo

uninstall: clean ## Uninstalls utility and destroys venv
	@echo "==> Uninstalling utility and dependencies..."
	@venv/bin/pip uninstall -y $(PACKAGE)
	@rm -rf venv/
	@echo "    [✓]"
	@echo

fmt: develop ## Formats python files
	@echo "==> Formatting files..."
	@venv/bin/black $(PACKAGE)
	@venv/bin/isort --profile=black $(PACKAGE)
	@echo "    [✓]"
	@echo

check: develop ## Checks code for linting/construct errors
	@echo "==> Checking if files are well formatted..."
	@venv/bin/flake8 $(PACKAGE)
	@echo "    [✓]"
	@echo

clean: ## Cleans up temporary files
	@echo "==> Cleaning up..."
	@find . -name "*.pyc" -exec rm -f {} \;
	@echo "    [✓]"
	@echo

.PHONY: install uninstall develop fmt check clean help
help: ## Shows available targets
	@fgrep -h "## " $(MAKEFILE_LIST) | fgrep -v fgrep | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-13s\033[0m %s\n", $$1, $$2}'
