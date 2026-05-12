---
name: memory-write
description: Create durable Markdown memories through `agent-memory write`; only `memory-manager` may use this skill.
compatibility: opencode
metadata:
  audience: agents
  workflow: memory-write
  domain: agent-memory
  allowed_agents: memory-manager
---

# Memory Write

## Purpose

Use this skill when acting as `memory-manager` after completed work may contain durable knowledge worth preserving.

## Allowed Agent

- `memory-manager`.

## Not Allowed

- No other agent may create memory entries.
- Do not manually edit `INDEX.md` or write files directly into `entries/`.
- Do not create a memory for every task.

## Should This Become Memory?

Write memory only when it will help a future agent avoid confusion, repeat work, or breaking something.

Good memory candidates:

- architecture decisions
- cross-project contracts
- bug causes and fixes
- important file locations
- testing gotchas
- migrations
- shared conventions
- integration assumptions
- repeated failure patterns

Do not store:

- secrets, API keys, credentials, or tokens
- full diffs
- full terminal logs
- temporary debugging noise
- generic repo rules better stored in `AGENTS.md`

## Write Flow

1. Use task summarization, decision extraction, and tagging judgment before writing.
2. Draft a short structured JSON, simple YAML, or Markdown-frontmatter input file.
3. Run `agent-memory write --input <file>`.
4. Run `agent-memory verify` if the write command did not already provide enough verification context.
5. Stop and report errors if verification fails.

## Required Fields

- `id`: stable kebab-case concept name, not a task number.
- `project`: project the memory primarily belongs to.
- `tags`: lowercase kebab-case tags.
- `importance`: number from `0` to `1`.
- `summary`: short actionable summary.
- `title`: clear human-readable heading.

Useful optional fields:

- `decisions`
- `impact`
- `related_projects`
- `important_files`
- `retrieve_when`
- `notes`

## Example Input

```yaml
id: auth-token-format
project: backend
tags: [auth, jwt, dashboard]
importance: 0.9
title: JWT validation moved to shared middleware
summary: JWT validation now happens in shared backend middleware, and dashboard depends on token payload shape.
decisions:
  - Do not parse JWT tokens directly inside route handlers.
  - Use src/middleware/auth.ts for token validation.
impact:
  - Dashboard may break if token payload fields change.
related_projects: [backend, dashboard, workers]
important_files:
  - src/middleware/auth.ts
retrieve_when:
  - JWT validation
  - dashboard authentication
```

Create it:

```sh
agent-memory write --input new-memory.yaml
agent-memory verify
```

## Safety Model

The write command validates fields, renders Markdown, scans for unsafe content, locks the memory store, writes atomically, regenerates `INDEX.md`, and verifies consistency.
