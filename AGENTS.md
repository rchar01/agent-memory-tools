# Agent Instructions

## Project Snapshot

- This is a standard-library-only Python CLI package installed as `agent-memory` from `agent_memory_tools.cli:main`.
- Runtime code lives in `src/agent_memory_tools/`; tests currently live in `tests/test_agent_memory_tools.py`.
- The CLI manages Markdown memory stores, not this repository's source files: default runtime data is `~/.local/share/agent-memory-tools/memory`, while repo-local `memory/`, `backups/`, and `.memory.lock` are ignored.
- Memory write/cleanup operations must go through CLI/library helpers so locking, atomic writes, index regeneration, safety scanning, and verification still happen.

## Developer Commands

- Run the full test suite with `python3 -m pytest -o addopts='' tests` or `make test`.
- Run one focused test with `python3 -m pytest -o addopts='' tests/test_agent_memory_tools.py::test_name`.
- Check CLI parsing without installing by running Python against `src`, for example `PYTHONPATH=src python3 -m agent_memory_tools.cli --help`.
- Install locally with `make install` or `make install-editable`; both require `pipx`.
- Install repo skills with `make install-skills`; override the target with `SKILLS_DIR=/path/to/skills`.
- `make update` intentionally runs `backup -> test -> reinstall -> verify` for an installed CLI.
- Use `agent-memory --memory-dir /tmp/some-memory ...` or a temp directory for manual CLI experiments so real user memory is not modified.

## Architecture Notes

- `cli.py` is only command dispatch; core behavior is split across small modules.
- `models.py` owns `MemoryEntry` validation and tag/list normalization.
- `markdown.py` implements the intentionally simple JSON/YAML/frontmatter parser and renderer; it is not full YAML.
- `writer.py` is the safe create path: validate, render, scan, lock, write, regenerate `INDEX.md`, verify.
- `index.py` is the source for active-entry discovery and `INDEX.md` format.
- `retrieval.py` ranks from `INDEX.md`, then opens only selected active entry files.
- `verifier.py` is the integrity gate for entries, index consistency, duplicate IDs, unsafe content, and summary warnings.
- `cleaner.py` handles duplicate reporting, archiving to `archive/YYYY-MM/`, and superseding active entries.
- `backup.py` archives the entire memory directory under a top-level `memory/` path.
- Agent-facing skill docs live under `skills/`; keep them aligned with `docs/memory-tooling-and-agent-editing.md` and CLI behavior.

## Testing And Safety Quirks

- Tests import from `src` by mutating `sys.path`; there is no test dependency configuration in `pyproject.toml`.
- There is no configured linter, formatter, typechecker, lockfile, or CI workflow in this repository right now.
- Keep CLI behavior and docs in sync when changing commands, memory format, validation, backup behavior, or install/update workflows.
- Safety scans in `security.py` deliberately reject likely secrets, prompt injection, invisible Unicode, large diffs, and large logs; update tests/docs when changing these rules.

## Agent Workflow Expectations

- Read relevant code before editing.
- Prefer minimal changes that match existing patterns.
- Keep `README.md`, `AGENTS.md`, and skill docs current when repository behavior changes.
- If your runtime provides specialized tools or subagents for codebase exploration, use them when the repository structure, ownership boundaries, or relevant files are unclear.
- If your runtime provides specialized tools or subagents for verification, use them for non-trivial test runs, runtime-backed checks, or command-heavy validation.
- If your runtime provides specialized tools or subagents for review, use them after substantial edits to catch regressions, missing updates, or doc/code drift.
- If your runtime provides specialized tools or subagents for research, use them when behavior depends on external tooling or upstream docs.
- Prefer local repository docs, scripts, and configuration first; use web research when local sources are insufficient or freshness matters.
- Summarize any specialist-tool or subagent findings you rely on.
- Do not revert unrelated worktree changes.
