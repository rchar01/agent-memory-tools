---
name: agent-memory-backup
description: Create safe `.tar.gz` backups of the Markdown memory directory with `agent-memory backup` before risky maintenance or upgrades.
compatibility: opencode
metadata:
  audience: agents
  workflow: memory-backup
  domain: agent-memory
  allowed_agents: memory-cleaner,memory-summarizer,validator
---

# Agent Memory Backup

## Purpose

Use this skill before broad cleanup, schema changes, tool upgrades, or any operation where restoring the memory store may be needed.

## Allowed Agents

- `memory-cleaner`
- `memory-summarizer`
- `validator`

## Commands

Create a default backup next to the memory directory:

```sh
agent-memory backup
```

Choose an output file:

```sh
agent-memory backup --output ~/backups/agent-memory-before-upgrade.tar.gz
```

Choose an output directory:

```sh
agent-memory backup --output ~/backups/
```

Back up a non-default memory store:

```sh
agent-memory --memory-dir /path/to/memory backup
```

## Backup Model

- The archive contains the memory directory under a top-level `memory/` path.
- Default output is a timestamped `agent-memory-backup-*.tar.gz` in a sibling `backups/` directory.
- Restore is intentionally manual because overwriting memory data is destructive and should be a deliberate human action.

## When To Use

- Before large cleanup or deduplication.
- Before schema or format changes.
- Before updating an installed CLI used against important memory data.
- Before investigating suspected memory corruption.
