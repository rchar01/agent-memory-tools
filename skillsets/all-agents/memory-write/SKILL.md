---
name: memory-write
description: Create durable Markdown memories through `agent-memory write`.
compatibility: opencode
metadata:
  audience: agents
  workflow: memory-write
  domain: agent-memory
---

# Memory Write

## Purpose

Use this skill when any agent decides completed work contains durable knowledge worth preserving.

## Allowed Agents

- Any agent may use this skill.

## Should This Become Memory?

Write memory only when it will help a future agent avoid confusion, repeat work, or breaking something.

Good memory candidates include architecture decisions, cross-project contracts, bug causes and fixes, important file locations, testing gotchas, migrations, shared conventions, integration assumptions, and repeated failure patterns.

Do not store secrets, full diffs, full terminal logs, temporary debugging noise, or generic repo rules better stored in `AGENTS.md`.

## Write Flow

1. Draft a short structured JSON, simple YAML, or Markdown-frontmatter input file.
2. Run `agent-memory write --input <file>`.
3. Run `agent-memory verify` if needed.
4. Stop and report errors if verification fails.

## Required Fields

- `id`: stable kebab-case concept name, not a task number.
- `project`: project the memory primarily belongs to.
- `tags`: lowercase kebab-case tags.
- `importance`: number from `0` to `1`.
- `summary`: short actionable summary.
- `title`: clear human-readable heading.

## Safety Model

The write command validates fields, renders Markdown, scans for unsafe content, locks the memory store, writes atomically, regenerates `INDEX.md`, and verifies consistency.
