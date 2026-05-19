---
name: memory-retrieval
description: Retrieve compact, relevant memories with the installed `agent-memory` CLI.
compatibility: opencode
metadata:
  audience: agents
  workflow: memory-retrieval
  domain: agent-memory
---

# Memory Retrieval

## Purpose

Use this skill when any agent needs remembered project context, prior decisions, testing gotchas, or important file locations.

## Allowed Agents

- Any agent may use this skill.

## Core Rule

- Read memory only when useful.
- Do not open or load the whole memory directory into context.
- Use `agent-memory retrieve` so the tool reads `INDEX.md`, ranks candidates, opens selected active entries, and returns a compact brief.

## Commands

```sh
agent-memory retrieve --query "dashboard auth token"
agent-memory retrieve --query "dashboard auth token" --project dashboard --tags auth,jwt
agent-memory --memory-dir /path/to/memory retrieve --query "auth token"
```

## Retrieval Guidance

- Prefer specific query terms from the task.
- Include `--project` for the current project when known.
- Include comma-separated `--tags` when the task has obvious domains.
- Default retrieval returns up to three memories; the CLI caps normal retrieval at five.
