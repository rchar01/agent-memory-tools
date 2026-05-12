---
name: agent-memory-retrieval
description: Retrieve compact, relevant memories with the installed `agent-memory` CLI without loading the whole memory store.
compatibility: opencode
metadata:
  audience: agents
  workflow: memory-retrieval
  domain: agent-memory
  allowed_agents: coder-1,coder-2,coder-3,code-reviewer,validator,git-committer,knowledge-writer
---

# Agent Memory Retrieval

## Purpose

Use this skill when an agent needs remembered project context, prior decisions, integration constraints, testing gotchas, or important file locations.

## Allowed Agents

- `coder-1`
- `coder-2`
- `coder-3`
- `code-reviewer`
- `validator`
- `git-committer`
- `knowledge-writer`

## Core Rule

- Do not open or load the whole memory directory into context.
- Use `agent-memory retrieve` so the tool reads `INDEX.md`, ranks candidates, opens selected active entries, and returns a compact brief.
- Coders, reviewers, committers, and knowledge writers must not write, clean, archive, or manually edit memory files.

## Commands

Retrieve by task text:

```sh
agent-memory retrieve --query "dashboard auth token"
```

Add project and tags when known:

```sh
agent-memory retrieve --query "dashboard auth token" --project dashboard --tags auth,jwt
```

Use a non-default memory store:

```sh
agent-memory --memory-dir /path/to/memory retrieve --query "auth token"
```

## Retrieval Guidance

- Prefer specific query terms from the task.
- Include `--project` for the current project when known.
- Include comma-separated `--tags` when the task has obvious domains.
- Default retrieval returns up to three memories; the CLI caps normal retrieval at five.
- If retrieved memory appears stale or wrong, report it instead of editing memory directly.

## Memory Location

Default memory lives at `~/.local/share/agent-memory-tools/memory` unless `AGENT_MEMORY_DIR` or `--memory-dir` overrides it.
