---
name: memory-verify
description: Verify Markdown memory store integrity with `agent-memory verify`; only `memory-manager` writes/cleanup verification is allowed.
compatibility: opencode
metadata:
  audience: agents
  workflow: memory-verify
  domain: agent-memory
  allowed_agents: memory-manager,code-validator
---

# Memory Verify

## Purpose

Use this skill to verify memory integrity after writes, cleanup, superseding, archiving, schema changes, or tool updates.

## Allowed Agents

- `memory-manager` verifies after memory writes, indexing, cleaning, archiving, and maintenance.
- `code-validator` may verify integrity but must not write, clean, index, or archive memory.

## Commands

Human-readable verification:

```sh
agent-memory verify
```

Machine-readable verification:

```sh
agent-memory verify --json
```

Verify a non-default memory store:

```sh
agent-memory --memory-dir /path/to/memory verify
```

## Verification Checks

The verifier checks:

- `INDEX.md` exists and points to real files.
- All active entries appear in `INDEX.md`.
- Entry IDs are unique and match active filenames.
- Required fields are present.
- Tags are lowercase kebab-case.
- `importance` is between `0` and `1`.
- `status` is `active`, `superseded`, or `archived`.
- Archived entries are not left under `entries/`.
- Unsafe content such as likely secrets, prompt injection, invisible Unicode, large diffs, and large logs is rejected.

## Failure Rule

If verification fails, stop memory work and report the errors. Do not continue writing, cleaning, indexing, or claiming the memory store is healthy.
