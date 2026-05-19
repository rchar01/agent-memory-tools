# News

This file gives a short, release-oriented view of what changed between versions.

## v1.1.0 - 2026-05-19

Skill installation now supports `role-scoped` and `all-agents` profiles under `skillsets/`, plus agent-group installs with `SKILL_GROUP`.

## v1.0.0 - 2026-05-12

This release adds the transparent Agent Memory Tools logo to the README using the new brand asset.

## v0.2.0 - 2026-05-12

This release updates the shipped skills to the focused `memory-*` model, adds `memory-index-update`, and makes `memory-manager` the only agent that writes, cleans, indexes, archives, or maintains memory.

Skill installation now supports selected skills by name, for example `make install-skills SKILL_NAMES="memory-retrieval memory-verify"`.

## v0.1.0 - 2026-05-12

This release adds role-specific OpenCode skills for memory retrieval, write, clean, verify, and backup workflows. Install them with `make install-skills`.

The README now explains how the package preserves memory as local Markdown files, where to clone the repository, and how to install from a local checkout.

## v0.0.1 - 2026-05-12

Initial release of `agent-memory-tools`, including the `agent-memory` CLI for safe local Markdown memory retrieval, writing, verification, cleanup, and backup.
