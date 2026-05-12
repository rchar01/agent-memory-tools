SHELL := /bin/sh
.DEFAULT_GOAL := help

PACKAGE ?= agent-memory-tools
CMD ?= agent-memory
PIPX ?= pipx
PYTHON ?= python3
MEMORY_DIR ?=
MEMORY_ARGS := $(if $(strip $(MEMORY_DIR)),--memory-dir "$(MEMORY_DIR)",)
DEFAULT_MEMORY_DIR := $(HOME)/.local/share/agent-memory-tools/memory

.PHONY: help check-pipx check-command install install-editable uninstall reinstall install-skills uninstall-skills update test verify backup

## Show available commands
help:
	@printf '%s\n' 'Available targets:'
	@awk '\
		/^## / { help = substr($$0, 4); next } \
		/^[a-zA-Z0-9_.-]+:/ { \
			if (help != "") { \
				target = $$1; \
				sub(/:.*/, "", target); \
				printf "  %-24s %s\n", target, help; \
				help = ""; \
			} \
		} \
	' $(MAKEFILE_LIST) | sort

## Install the CLI with pipx
install: check-pipx
	$(PIPX) install .

## Install the CLI in editable mode for development
install-editable: check-pipx
	$(PIPX) install --force --editable .

## Uninstall the pipx app environment, keeping memory data untouched
uninstall: check-pipx
	$(PIPX) uninstall $(PACKAGE)

## Reinstall the CLI from the current checkout
reinstall: check-pipx
	$(PIPX) install --force .

## Install agent-memory skills into ~/.agents/skills
install-skills:
	@./scripts/install-skills

## Remove agent-memory skills from ~/.agents/skills
uninstall-skills:
	@./scripts/uninstall-skills

## Back up memory, run tests, reinstall, then verify
update: backup test reinstall verify

## Run package tests
test:
	$(PYTHON) -m pytest -o addopts='' tests

## Verify the configured memory store
verify: check-command
	$(CMD) $(MEMORY_ARGS) verify

## Create a memory backup archive
backup:
	@if command -v "$(CMD)" >/dev/null 2>&1 && $(CMD) --help 2>/dev/null | awk '/backup/ { found = 1 } END { exit found ? 0 : 1 }'; then \
		$(CMD) $(MEMORY_ARGS) backup; \
	else \
		mem_dir="$(if $(strip $(MEMORY_DIR)),$(MEMORY_DIR),$${AGENT_MEMORY_DIR:-$(DEFAULT_MEMORY_DIR)})"; \
		if [ ! -d "$$mem_dir" ]; then \
			printf '%s\n' "Memory directory not found: $$mem_dir" >&2; \
			exit 1; \
		fi; \
		backup_dir="$$(dirname "$$mem_dir")/backups"; \
		stamp="$$(date -u +%Y%m%d-%H%M%SZ)"; \
		mkdir -p "$$backup_dir"; \
		tar -czf "$$backup_dir/agent-memory-backup-$$stamp.tar.gz" -C "$$(dirname "$$mem_dir")" "$$(basename "$$mem_dir")"; \
		printf '%s\n' "Created backup: $$backup_dir/agent-memory-backup-$$stamp.tar.gz"; \
	fi

check-pipx:
	@command -v "$(PIPX)" >/dev/null 2>&1 || { \
		printf '%s\n' "$(PIPX) not found. Install it with: sudo apt install pipx" >&2; \
		exit 1; \
	}

check-command:
	@command -v "$(CMD)" >/dev/null 2>&1 || { \
		printf '%s\n' "$(CMD) not found. Run: make install" >&2; \
		exit 1; \
	}
