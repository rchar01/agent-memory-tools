---
name: memory-index-update
description: Regenerate the Markdown memory index with `agent-memory index-update`; only `memory-manager` may use this skill.
compatibility: opencode
metadata:
  audience: agents
  workflow: memory-index-update
  domain: agent-memory
  allowed_agents: memory-manager
---

# Memory Index Update

## Purpose

Use this skill when acting as `memory-manager` to regenerate `INDEX.md` from active memory entries.

## Allowed Agent

- `memory-manager`.

## Not Allowed

- No other agent may regenerate or manually edit the memory index.
- Do not hand-edit `INDEX.md`; use the CLI so active entries, paths, tags, summaries, and importance stay consistent.

## Commands

Regenerate the index:

```sh
agent-memory index-update
```

Verify after regeneration:

```sh
agent-memory verify
```

Use a non-default memory store:

```sh
agent-memory --memory-dir /path/to/memory index-update
agent-memory --memory-dir /path/to/memory verify
```

## Index Rules

- `INDEX.md` includes active entries only.
- Archived and superseded memories are excluded from normal retrieval.
- Each index row must match the entry file, project, tags, importance, and summary.
- If verification fails after regeneration, stop and report the errors.
