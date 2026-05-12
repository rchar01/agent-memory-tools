# Memory Tooling and Agent Editing Specification

## Core Principle

Memory files are human-readable Markdown, but agents should not freely edit them by hand.

Core rule:

```text
Everyone may read memory only if useful.
Only memory-manager writes, cleans, indexes, or verifies memory.
```

Operating rule:

```text
Agents reason.
Tools perform structured memory operations.
memory-manager verifies memory quality.
```

## Agent To Memory Skill Map

| Agent | Memory skills |
| --- | --- |
| `orchestrator` | none directly; only routes memory tasks to `memory-manager` |
| `planner` | optional `memory-retrieval` for large or ambiguous planning |
| `context-builder` | `memory-retrieval` |
| `coder-1` | `memory-retrieval` |
| `coder-2` | `memory-retrieval` |
| `coder-3` | `memory-retrieval` |
| `code-reviewer` | `memory-retrieval` |
| `code-validator` | `memory-retrieval`, `memory-verify` |
| `memory-manager` | `memory-retrieval`, `memory-write`, `memory-index-update`, `memory-clean`, `memory-verify` |
| `git-committer` | optional `memory-retrieval` for commit context |

Install all OpenCode memory skills with:

```bash
make install-skills
```

Install one or more skills by name with:

```bash
make install-skills SKILL_NAMES="memory-retrieval memory-verify"
```

The skill sources live in `skills/` and mirror the tool boundaries below.

## Tool Responsibilities

### `memory-retrieval`

Used by:

- `planner`, optionally for large or ambiguous planning.
- `context-builder`.
- `coder-1`.
- `coder-2`.
- `coder-3`.
- `code-reviewer`.
- `code-validator`.
- `memory-manager`.
- `git-committer`, optionally for commit context.

Purpose: retrieve relevant memories without loading the full memory store into context.

Behavior:

```text
read memory/INDEX.md
rank candidate memories
open selected files from memory/entries/
return compact brief
```

No retrieval user should manually inspect the whole memory directory unless debugging memory itself.

### `memory-write`

Used by:

- `memory-manager`

Purpose: create memory entries safely.

The tool creates:

```text
memory/entries/<memory-id>.md
```

And updates:

```text
memory/INDEX.md
```

It must enforce:

- Valid memory id.
- Required frontmatter.
- Valid project field.
- Valid tags.
- Valid importance score.
- No duplicate id.
- Consistent index update.

The `memory-manager` decides what should be remembered. The CLI handles file creation, index update, locking, safety checks, and verification.

### `memory-index-update`

Used by:

- `memory-manager`

Purpose: regenerate `INDEX.md` consistently.

It should verify:

- Every active entry has an index row.
- Every index row points to an existing file.
- Archived and superseded memories are not listed as active.
- Summary text is short.
- Tags match entry frontmatter.
- Importance is valid.

### `memory-clean`

Used by:

- `memory-manager`

Purpose: back up, deduplicate, archive, and mark superseded memories.

It should support:

- Creating backups before broad or risky maintenance.
- Finding duplicate memories.
- Merging related memories with human/agent semantic judgment.
- Moving stale files to archive.
- Marking entries as superseded.
- Regenerating `INDEX.md`.
- Detecting broken links.
- Detecting malformed frontmatter.

The `memory-manager` decides cleanup policy; the CLI performs safe file operations.

### `memory-verify`

Used by:

- `memory-manager`
- `code-validator`

Purpose: verify memory integrity.

It checks:

- `INDEX.md` references existing files.
- All entries have required fields.
- Memory ids are unique.
- Tags are formatted consistently.
- Importance is numeric and between `0` and `1`.
- Status is valid: `active`, `superseded`, or `archived`.
- No obvious secrets are stored.
- No full diffs or large logs are stored.

Run this after:

- New memory creation.
- Index regeneration.
- Memory cleanup.
- Memory merge.
- Archive operation.

If verification fails, the agent should stop and report the issue instead of continuing.

`code-validator` may run verification but must not write, clean, index, or archive memory.

## Role Permissions

### Read-Only Memory Users

Allowed:

- Retrieve memory when it is useful.
- Use retrieved context for the current task.
- Mention useful memory candidates in task output.
- Flag stale or incorrect memory for `memory-manager`.

Not allowed:

- Edit `INDEX.md`.
- Create memory files.
- Modify memory entries.
- Archive memories.
- Clean memory.
- Regenerate the memory index.

This applies to `planner`, `context-builder`, `coder-1`, `coder-2`, `coder-3`, `code-reviewer`, and `git-committer`.

### Code Validator

Allowed:

- Retrieve cross-project memory.
- Check implementation against remembered contracts.
- Flag stale memory.
- Request memory updates from `memory-manager`.
- Run `memory-verify`.

Not allowed:

- Write, clean, index, archive, or manually edit memory.

### Memory Manager

Allowed:

- Retrieve memory.
- Decide if completed work deserves memory.
- Create and update memory through `memory-write`.
- Regenerate `INDEX.md` through `memory-index-update`.
- Back up, clean, deduplicate, archive, and supersede memory through `memory-clean`.
- Verify with `memory-verify`.

Avoid:

- Manual index editing.
- Manual file renaming.
- Manual archive movement.
- Creating memory for every task.

The `memory-manager` should ask:

```text
Will this help a future agent avoid confusion, repeat work, or breaking something?
```

## What Belongs In Tools Vs Agent Reasoning

Put deterministic, repeatable, error-prone operations into tools:

- Searching `INDEX.md`.
- Ranking memories.
- Opening selected files.
- Writing new memory files.
- Updating `INDEX.md`.
- Checking frontmatter.
- Detecting duplicate ids.
- Moving files to archive.
- Regenerating index.
- Validating links.
- Checking malformed entries.
- Checking for secrets.

Let agents decide semantic questions:

- Is this worth remembering?
- What is the correct summary?
- What tags best describe this memory?
- Is this memory stale?
- Does this code violate a remembered decision?
- Should this pattern become knowledge documentation?

Agents are good at semantic judgment; tools are better at safe file operations.

## Memory Write Flow

After a completed task:

```text
agent finishes task
orchestrator routes memory work to memory-manager
memory-manager decides whether memory is needed
if no: no memory action
if yes: draft memory content
memory-write creates entry file
memory-index-update updates INDEX.md when needed
memory-verify validates memory store
```

## Memory Retrieval Flow

During a task:

```text
agent receives task
agent reads task + repo instructions
agent invokes memory-retrieval only if useful
memory-retrieval returns compact brief
agent uses brief while working
```

Returned memory should be short:

- 1-5 entries.
- Top three by default.
- Summaries plus key decisions.
- Important files only.

## Memory Cleanup Flow

Periodic cleanup:

```text
orchestrator routes cleanup to memory-manager
memory-manager creates backup when cleanup is broad or risky
memory-manager scans INDEX.md and entries through CLI-backed flows
memory-clean finds duplicates/stale entries
memory-manager decides merge/archive/supersede
memory-clean performs file operations
memory-index-update regenerates INDEX.md when needed
memory-verify checks final state
```

Suggested cadence:

- Daily for active projects.
- Weekly otherwise.
- After large migrations.
- After many related tasks.

## Required Verification Checks

Any memory-writing or cleanup operation should verify:

- `INDEX.md` points to real files.
- All active files appear in `INDEX.md`.
- All entries have frontmatter.
- ID matches filename.
- ID is unique.
- Project exists or is known.
- Tags are present.
- Importance is between `0` and `1`.
- Status is `active`, `superseded`, or `archived`.
- Archived files are not active in `INDEX.md`.
- No secrets are present.
- No full terminal logs are stored.
- No giant diffs are stored.

## Final Rule Set

```text
Everyone may read memory only if useful.
Only memory-manager writes, cleans, indexes, or verifies memory.
Tools perform file operations.
Agents make semantic decisions.
```

Key boundary:

```text
Agents should not casually edit memory files; they should use memory tools that verify structure and prevent corruption.
```
