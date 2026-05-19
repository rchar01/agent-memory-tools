---
name: memory-verify
description: Verify Markdown memory store integrity with `agent-memory verify`.
compatibility: opencode
metadata:
  audience: agents
  workflow: memory-verify
  domain: agent-memory
---

# Memory Verify

## Purpose

Use this skill to verify memory integrity after writes, cleanup, superseding, archiving, schema changes, or tool updates.

## Allowed Agents

- Any agent may use this skill.

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
