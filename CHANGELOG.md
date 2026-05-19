# Changelog

All notable changes to `agent-memory-tools` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-05-19

### Added

- `role-scoped` and `all-agents` skill profiles under `skillsets/`.
- Skill installation by agent group with `SKILL_GROUP`, including `memory-manager`, `code-validator`, and `all`.

### Changed

- Skill installation now reads from profile-specific `skillsets/` sources instead of a single `skills/` source tree.

## [1.0.0] - 2026-05-12

### Added

- Transparent Agent Memory Tools logo in the README using the new brand asset.

## [0.2.0] - 2026-05-12

### Added

- `memory-index-update` skill for `memory-manager` index regeneration workflows.
- Named skill install and uninstall support with `SKILL_NAMES="memory-retrieval memory-verify"`.

### Changed

- Renamed shipped skills from `agent-memory-*` to focused `memory-*` names.
- Consolidated memory write, clean, index, archive, and maintenance permissions under one `memory-manager` agent.
- Folded backup guidance into `memory-clean` instead of shipping a standalone backup skill.
- Updated memory tooling docs and agent access maps for `planner`, `context-builder`, `code-validator`, `memory-manager`, and optional retrieval users.

## [0.1.0] - 2026-05-12

### Added

- Role-specific OpenCode skill docs for retrieval, writing, cleaning, verification, and backup workflows.
- `make install-skills` and `make uninstall-skills` helpers for installing repo skills.
- README introduction explaining how local Markdown memory is preserved separately from the installed CLI.
- Installation guidance for cloning from the Codeberg repository and installing from a local checkout.

## [0.0.1] - 2026-05-12

### Added

- Initial `agent-memory` CLI for local Markdown memory stores.
- Commands for initializing, writing, retrieving, indexing, verifying, cleaning, and backing up memory data.
- Safety checks for likely secrets, prompt-injection text, invisible Unicode, large diffs, and large logs.
- Atomic writes, file locking, index regeneration, and post-write verification for memory updates.
- Documentation for install, usage, operations, memory format, and agent editing boundaries.
