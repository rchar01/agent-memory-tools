---
name: memory-verify
description: Verify Markdown memory store integrity with `agent-memory verify`; only `memory-manager` writes/cleanup verification is allowed.
compatibility: opencode
metadata:
  audience: agents
  workflow: memory-verify
  domain: agent-memory
  access_profile: role-scoped
  allowed_agents: memory-manager,code-validator
---

# Memory Verify

## Purpose

Use this skill to verify memory integrity after writes, cleanup, superseding, archiving, schema changes, or tool updates.

## Allowed Agents

- `memory-manager` verifies after memory writes, indexing, cleaning, archiving, and maintenance.
- `code-validator` may verify integrity but must not write, clean, index, or archive memory.

## Commands

```sh
agent-memory verify
agent-memory verify --json
agent-memory --memory-dir /path/to/memory verify
```

## Verification Checks

The verifier checks index consistency, required fields, duplicate IDs, filename matches, tag format, importance range, status values, archived entry placement, and unsafe content.

## Failure Rule

If verification fails, stop memory work and report the errors. Do not continue writing, cleaning, indexing, or claiming the memory store is healthy.
