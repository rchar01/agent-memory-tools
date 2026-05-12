# News

This file gives a short, release-oriented view of what changed between versions.

## v0.1.0 - 2026-05-12

This release adds role-specific OpenCode memory skills for retrieval, write, index update, clean, and verify workflows. Install all skills with `make install-skills`, or selected skills with `SKILL_NAMES="memory-retrieval memory-verify"`.

The skill access model now uses a single `memory-manager` for writing, cleaning, indexing, archiving, and maintenance.

The README now explains how the package preserves memory as local Markdown files, where to clone the repository, and how to install from a local checkout.

## v0.0.1 - 2026-05-12

Initial release of `agent-memory-tools`, including the `agent-memory` CLI for safe local Markdown memory retrieval, writing, verification, cleanup, and backup.
