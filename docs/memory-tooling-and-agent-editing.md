# Memory Tooling and Agent Editing Specification

## Core Principle

Memory files are human-readable Markdown, but agents should not freely edit them by hand unless their role explicitly allows it.

Operating rule:

```text
Agents reason.
Tools perform structured memory operations.
Review/cleaning agents verify memory quality.
```

## Tool Responsibilities

Install the matching OpenCode skills with:

```bash
make install-skills
```

The skill sources live in `skills/` and mirror the tool boundaries below.

### `memory-retrieval`

Used by:

- `coder-1`
- `coder-2`
- `coder-3`
- `code-reviewer`
- `validator`
- `git-committer`
- `knowledge-writer`

Purpose: retrieve relevant memories without loading the full memory store into context.

Behavior:

```text
read memory/INDEX.md
rank candidate memories
open selected files from memory/entries/
return compact brief
```

The coding agent should not manually inspect the whole memory directory unless debugging memory itself.

### `memory-write`

Used by:

- `memory-summarizer`

Purpose: create new memory entries safely.

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

The memory-summarizer decides what should be remembered. The tool handles file creation and index update.

### `memory-index-update`

Used by:

- `memory-summarizer`
- `memory-cleaner`

Purpose: regenerate or update `INDEX.md` consistently.

It should verify:

- Every active entry has an index row.
- Every index row points to an existing file.
- Archived memories are not listed as active.
- Summary text is short.
- Tags match entry frontmatter.
- Importance is valid.

### `memory-clean`

Used by:

- `memory-cleaner`

Purpose: deduplicate, merge, archive, and mark superseded memories.

It should support:

- Finding duplicate memories.
- Merging related memories, with human/agent semantic judgment.
- Moving stale files to archive.
- Marking entries as superseded.
- Regenerating `INDEX.md`.
- Detecting broken links.
- Detecting malformed frontmatter.

The memory-cleaner decides cleanup policy; the tool performs safe file operations.

### `memory-verify`

Used by:

- `memory-summarizer`
- `memory-cleaner`
- `validator`

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
- Memory cleanup.
- Memory merge.
- Archive operation.

If verification fails, the agent should stop and report the issue instead of continuing.

## Role Permissions

### Coders

Allowed:

- Use memory retrieval.
- Use retrieved context while coding.
- Mention useful memory candidates in task output.
- Flag stale or incorrect memory.

Not allowed:

- Edit `INDEX.md`.
- Create memory files.
- Modify memory entries.
- Archive memories.
- Clean memory.

Reason: coders are execution workers. They should not pollute or restructure the memory system.

### Memory Summarizer

Allowed:

- Decide if completed work deserves memory.
- Write proposed memory content.
- Create memory through `memory-write`.
- Update `INDEX.md` through `memory-index-update`.
- Verify with `memory-verify`.

Avoid:

- Manual index editing.
- Manual file renaming.
- Manual archive movement.
- Broad deduplication across many memories.

The summarizer should not create a memory for every task. It should ask:

```text
Will this help a future agent avoid confusion, repeat work, or breaking something?
```

### Memory Cleaner

Allowed:

- Merge memory entries.
- Archive stale entries.
- Mark memories as superseded.
- Rewrite/regenerate index.
- Remove low-value clutter.

Should verify with:

```text
memory-verify
```

The cleaner is the only agent that should broadly restructure memory.

### Code Reviewer

Allowed:

- Retrieve memory relevant to review.
- Compare code against remembered decisions.
- Flag conflicts with memory.

Not allowed:

- Edit memory directly.
- Create new memory.
- Archive memory.

If a reviewer finds useful memory should be updated, it should request a memory-summarizer follow-up task.

### Validator

Allowed:

- Retrieve cross-project memory.
- Check implementation against remembered contracts.
- Flag stale memory.
- Request memory update.
- Run `memory-verify`.

Not allowed:

- Edit memory directly unless explicitly delegated through memory-summarizer or memory-cleaner.

### Git Committer

Allowed:

- Retrieve relevant memory.
- Use memory to draft better commit messages.
- Reference known decisions in PR descriptions.

Not allowed:

- Write memory.
- Clean memory.
- Modify memory files.

### Knowledge Writer

Allowed:

- Retrieve memory.
- Summarize repeated decisions into knowledge docs.
- Suggest memories to archive after promotion.

Not allowed:

- Delete memories directly.
- Rewrite memory index directly.

If the knowledge-writer promotes memories into durable docs, it should ask memory-cleaner to mark those entries as superseded or archived.

## What Belongs in Tools vs Agent Reasoning

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
coder finishes task
orchestrator routes output to memory-summarizer
memory-summarizer decides whether memory is needed
if no: no memory action
if yes: draft memory content
memory-write creates entry file
memory-index-update updates INDEX.md
memory-verify validates memory store
```

## Memory Retrieval Flow

During a coding task:

```text
coder receives task
coder reads task + repo instructions
coder invokes memory-retrieval when relevant
memory-retrieval returns compact brief
coder uses brief while coding
```

Returned memory should be short:

- 1-5 entries.
- Top three by default.
- Summaries plus key decisions.
- Important files only.

## Memory Cleanup Flow

Periodic cleanup:

```text
orchestrator schedules memory-cleaner
memory-cleaner scans INDEX.md and entries/
memory-clean finds duplicates/stale entries
memory-cleaner decides merge/archive/supersede
memory-clean performs file operations
memory-index-update regenerates INDEX.md
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
Coders retrieve memory.
Memory-summarizer writes memory.
Memory-cleaner maintains memory.
Validator verifies consistency.
Knowledge-writer promotes memory into docs.
Tools perform file operations.
Agents make semantic decisions.
```

Key boundary:

```text
Agents should not casually edit memory files; they should use memory tools that verify structure and prevent corruption.
```
