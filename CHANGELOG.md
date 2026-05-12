# Changelog

All notable changes to `agent-memory-tools` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
