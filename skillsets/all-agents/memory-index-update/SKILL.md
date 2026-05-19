---
name: memory-index-update
description: Regenerate the Markdown memory index with `agent-memory index-update`.
compatibility: opencode
metadata:
  audience: agents
  workflow: memory-index-update
  domain: agent-memory
---

# Memory Index Update

## Purpose

Use this skill when any agent needs to regenerate `INDEX.md` from active memory entries.

## Allowed Agents

- Any agent may use this skill.

## Commands

```sh
agent-memory index-update
agent-memory verify
agent-memory --memory-dir /path/to/memory index-update
agent-memory --memory-dir /path/to/memory verify
```

## Index Rules

- `INDEX.md` includes active entries only.
- Archived and superseded memories are excluded from normal retrieval.
- Each index row must match the entry file, project, tags, importance, and summary.
- If verification fails after regeneration, stop and report the errors.
