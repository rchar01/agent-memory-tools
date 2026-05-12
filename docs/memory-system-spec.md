# Memory System Specification

## Purpose

The memory system stores durable knowledge from completed work so future agents can retrieve relevant context without loading full task history.

Memory is not a task log, chat transcript, or diff dump. It stores only information useful for future work.

The system is:

- Global.
- Markdown-based.
- Shared across projects.
- Retrieved selectively.
- Human-readable.
- Maintained by dedicated memory agents.

## Directory Structure

```text
memory/
├── INDEX.md
├── entries/
│   ├── auth-token-format.md
│   ├── billing-redis-tests.md
│   └── ...
├── archive/
│   └── 2026-05/
└── README.md
```

`INDEX.md` is a short searchable index of active memories. Retrieval tools use it to discover candidate entries.

`entries/` contains one Markdown file per active memory.

`archive/` contains old, stale, merged, or low-value memories. Archived memories are normally excluded from retrieval.

`README.md` explains memory rules and local permissions for that memory store.

## Core Rule

Do not load all memory into a coding agent context.

Good flow:

```text
coder asks memory-retrieval
tool reads INDEX.md
tool opens selected files
tool returns 1-5 relevant memories
```

Bad flow:

```text
coder opens all memory files
coder dumps the memory store into context
```

Only the retrieval brief should enter the active agent context.

## Index Format

`INDEX.md` must be short and scan-friendly.

Example:

```md
# Memory Index

## Active Memories

### auth-token-format

File: `entries/auth-token-format.md`  
Project: `backend`  
Tags: `auth, jwt, contract, dashboard`  
Importance: `0.9`  
Summary: JWT validation moved to shared middleware; dashboard depends on token shape.

---
```

Each index entry must include:

- Memory id.
- File path.
- Project.
- Tags.
- Importance.
- One-sentence summary.

The index must not contain full details.

## Entry Format

Each memory entry is a separate Markdown file with frontmatter.

```md
---
id: auth-token-format
project: backend
tags: [auth, jwt, contract, dashboard]
importance: 0.9
created: 2026-05-12
updated: 2026-05-12
status: active
---

# JWT validation moved to shared middleware

## Summary

JWT validation now happens in shared backend middleware instead of individual route handlers.

## Decisions

- Do not parse JWT tokens directly inside route handlers.
- Use `src/middleware/auth.ts` for token validation.
- Keep token payload shape stable because dashboard and workers depend on it.

## Impact

- Backend auth routes are simpler.
- Dashboard may break if token payload fields change.
- Background workers should be checked before changing token format.

## Related projects

- backend
- dashboard
- workers

## Important files

- `src/middleware/auth.ts`
- `src/auth/jwt.ts`
- `dashboard/src/lib/auth.ts`

## When to retrieve this memory

- login
- JWT validation
- auth middleware
- dashboard authentication
- token payload changes

## Notes

This memory replaces older scattered auth validation notes.
```

## Memory ID Naming

Memory IDs must be stable, readable, and kebab-case.

Good:

- `auth-token-format`
- `billing-redis-tests`
- `dashboard-order-status`
- `shared-api-client`
- `worker-retry-policy`

Bad:

- `memory-1`
- `task-123`
- `fix-bug`
- `notes`

The ID should describe the durable concept, not the task that created it.

## What Goes Into Memory

Store durable knowledge that future agents should remember:

- Architecture decisions.
- Cross-project contracts.
- Bug causes and fixes.
- Important file locations.
- Testing gotchas.
- Migration notes.
- Shared conventions.
- Integration assumptions.
- Dependency relationships.
- Repeated failure patterns.

Examples:

- Dashboard depends on exact order status enum names from orders-api.
- Billing integration tests require Redis, but unit tests should not.
- Frontend API calls should use the shared client in `lib/api/client.ts`.
- Auth token payload changes must be checked against dashboard and workers.

## What Does Not Go Into Memory

Do not store:

- Full diffs.
- Full terminal logs.
- Temporary debugging noise.
- Secrets, API keys, or credentials.
- Every tiny task result.
- Information better kept in repo `AGENTS.md`.
- Raw stack traces unless they document a recurring gotcha.

A task does not automatically produce a memory. Only durable knowledge becomes memory.

## Memory vs AGENTS.md vs Knowledge Docs

`AGENTS.md` stores static project rules, such as test commands, coding style, framework conventions, and repo-specific constraints.

Memory stores dynamic historical knowledge: what changed, why a decision was made, what broke before, and what future agents should remember.

Knowledge docs store long-form durable documentation: architecture overviews, ADRs, system design notes, and integration maps.

Use this split:

```text
AGENTS.md = local rules
memory = remembered experience
knowledge docs = long-term documentation
```

## Retrieval Behavior

Only agents that need context should retrieve memory.

Primary users:

- `planner`, optionally for large or ambiguous planning
- `context-builder`
- `coder-1`
- `coder-2`
- `coder-3`
- `code-reviewer`
- `code-validator`
- `memory-manager`
- `git-committer`, optionally for commit context

Only `memory-manager` writes, cleans, indexes, archives, or otherwise modifies memory.

Retrieval flow:

```text
agent receives task
memory-retrieval reads INDEX.md
tool selects candidate entries
tool opens selected files
tool returns compact brief
agent continues task
```

Returned brief should include:

- Memory id.
- Project.
- Tags.
- Importance.
- Summary.
- Key decisions/impact.
- Important files.

## Retrieval Ranking

Prefer memories by:

- Project match.
- Tag match.
- Summary keyword match.
- Importance.
- Recency.
- Cross-project relevance.

Suggested priority:

```text
same project + matching tags = highest priority
```

Default retrieval is top three memories. Maximum normal retrieval is five.

## Archive Behavior

Move old or low-value memories to:

```text
memory/archive/YYYY-MM/
```

Archived memories should not be listed in `INDEX.md` and should not be retrieved unless explicitly requested.

## Cross-Project Work

Because memory is global, every memory must include:

- Project.
- Tags.
- Related projects, when relevant.

This allows a coder working in one project to retrieve relevant memories from another project.

## Quality Standard

Each memory should be:

- Short.
- Specific.
- Actionable.
- Tagged.
- Project-aware.
- Easy to delete or merge.

Bad:

```md
Fixed auth bug.
```

Good:

```md
Login failed locally because cookie domain was forced to production domain. Use env-specific cookie domain in `src/config/cookies.ts`.
```
