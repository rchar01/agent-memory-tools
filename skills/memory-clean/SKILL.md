---
name: memory-clean
description: Let `memory-manager` maintain the Markdown memory store with cleanup, deduplication, archiving, backups, and verification.
compatibility: opencode
metadata:
  audience: agents
  workflow: memory-clean
  domain: agent-memory
  allowed_agents: memory-manager
---

# Memory Clean

## Purpose

Use this skill when acting as `memory-manager` to deduplicate, archive, supersede, back up, or otherwise maintain memory quality.

## Allowed Agent

- `memory-manager`.

## Not Allowed

- No other agent may clean, archive, back up for cleanup, or manually edit memory.
- Do not manually move files or edit `INDEX.md`; use the CLI so index regeneration and verification stay consistent.

## Cleanup Flow

1. Create a backup before broad cleanup, deduplication, archive work, or risky restructuring.
2. Inspect duplicates or stale candidates through CLI output and targeted retrieval.
3. Decide semantic cleanup policy as `memory-manager`.
4. Run `agent-memory clean ...` for file operations.
5. Run `agent-memory verify`.
6. Stop and report if verification fails.

## Backup Commands

Create a default backup next to the memory directory:

```sh
agent-memory backup
```

Choose an output file or directory:

```sh
agent-memory backup --output ~/backups/agent-memory-before-cleanup.tar.gz
agent-memory backup --output ~/backups/
```

The archive contains the memory directory under a top-level `memory/` path. Restore is intentionally manual because overwriting memory is destructive.

## Cleanup Commands

Find duplicate or overlapping active memories:

```sh
agent-memory clean --find-duplicates
```

Archive an active memory:

```sh
agent-memory clean --archive old-auth-token-format --reason "promoted to docs"
```

Mark one active memory as superseded by another:

```sh
agent-memory clean --supersede old-auth-token-format --by auth-token-format-v2
```

Verify final state:

```sh
agent-memory verify
```

## Cleanup Rules

- Archived memories move to `archive/YYYY-MM/` and are excluded from normal retrieval.
- Superseded memories stay in `entries/` with `status: superseded` and are excluded from `INDEX.md`.
- Semantic merging is not automatic; choose the surviving memory deliberately.
- Preserve durable facts unless they are stale, merged, promoted to docs, or low value.

## Safety Model

Cleanup commands use the same memory lock and index regeneration model as writes. Verification must pass before cleanup is considered complete.
