---
name: memory-clean
description: Maintain the Markdown memory store with cleanup, deduplication, archiving, backups, and verification.
compatibility: opencode
metadata:
  audience: agents
  workflow: memory-clean
  domain: agent-memory
---

# Memory Clean

## Purpose

Use this skill when any agent needs to deduplicate, archive, supersede, back up, or otherwise maintain memory quality.

## Allowed Agents

- Any agent may use this skill.

## Cleanup Flow

1. Create a backup before broad cleanup, deduplication, archive work, or risky restructuring.
2. Inspect duplicates or stale candidates through CLI output and targeted retrieval.
3. Decide semantic cleanup policy.
4. Run `agent-memory clean ...` for file operations.
5. Run `agent-memory verify`.
6. Stop and report if verification fails.

## Backup Commands

```sh
agent-memory backup
agent-memory backup --output ~/backups/agent-memory-before-cleanup.tar.gz
agent-memory backup --output ~/backups/
```

The archive contains the memory directory under a top-level `memory/` path. Restore is intentionally manual because overwriting memory is destructive.

## Cleanup Commands

```sh
agent-memory clean --find-duplicates
agent-memory clean --archive old-auth-token-format --reason "promoted to docs"
agent-memory clean --supersede old-auth-token-format --by auth-token-format-v2
agent-memory verify
```

## Cleanup Rules

- Archived memories move to `archive/YYYY-MM/` and are excluded from normal retrieval.
- Superseded memories stay in `entries/` with `status: superseded` and are excluded from `INDEX.md`.
- Semantic merging is not automatic; choose the surviving memory deliberately.
