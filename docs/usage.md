# Usage

Agent Memory Tools installs the `agent-memory` executable for local Markdown memory operations.

## Install

Use `pipx` on Linux systems that protect system Python with PEP 668:

```bash
sudo apt install pipx
pipx ensurepath
make install
```

Restart your shell, or run:

```bash
source ~/.profile
```

Verify installation:

```bash
agent-memory --help
```

The equivalent direct command is:

```bash
pipx install .
```

## Alternative venv Install

If `pipx` is unavailable:

```bash
python3 -m venv ~/.local/share/agent-memory-tools/venv
~/.local/share/agent-memory-tools/venv/bin/pip install .
ln -s ~/.local/share/agent-memory-tools/venv/bin/agent-memory ~/.local/bin/agent-memory
```

Do not use `pip --break-system-packages` unless you intentionally want to bypass your OS Python protection.

## Make Targets

The project includes a small Makefile for common operations:

```bash
make help
make install
make install-editable
make install-skills
make uninstall-skills
make update
make uninstall
make test
make verify
make backup
```

`make update` performs the safe local update workflow:

```text
backup -> test -> reinstall -> verify
```

`make install-skills` copies repo skills into `${SKILLS_DIR:-$HOME/.agents/skills}`. It installs the default `role-scoped` profile unless `SKILL_PROFILE` is set.

Examples:

```bash
make install-skills
make install-skills SKILL_PROFILE=all-agents
make install-skills SKILL_GROUP=memory-manager
make install-skills SKILL_NAMES="memory-retrieval memory-verify"
```

Use `MEMORY_DIR` when operating on a non-default memory store:

```bash
make verify MEMORY_DIR=/path/to/memory
make backup MEMORY_DIR=/path/to/memory
```

## Memory Directory

Default location:

```text
~/.local/share/agent-memory-tools/memory
```

Set a global location:

```bash
export AGENT_MEMORY_DIR="$HOME/.agent-memory"
```

Override per command:

```bash
agent-memory --memory-dir /path/to/memory retrieve --query "auth token"
```

## Initialize

```bash
agent-memory init
```

Creates:

```text
memory/
├── INDEX.md
├── README.md
├── entries/
└── archive/
```

## Retrieve

Coders and reviewers should use retrieval instead of opening the whole memory directory.

```bash
agent-memory retrieve --query "dashboard auth token" --project dashboard --tags auth,jwt
```

Default retrieval returns up to three memories. Hard maximum is five.

## Agent Skills

OpenCode memory skill profiles live under `skillsets/` and can be installed with:

```bash
make install-skills
```

Profiles:

- `role-scoped`: default; only the mapped agents should use each skill.
- `all-agents`: permissive skillset; every installed memory skill is available to any agent.

Install the all-agents skillset:

```bash
make install-skills SKILL_PROFILE=all-agents
```

Install by agent group:

```bash
make install-skills SKILL_GROUP=memory-manager
make install-skills SKILL_GROUP=code-validator
```

To install elsewhere:

```bash
make install-skills SKILLS_DIR=/path/to/skills
```

To install or uninstall selected skills by name:

```bash
make install-skills SKILL_NAMES="memory-retrieval memory-verify"
make uninstall-skills SKILL_NAMES="memory-retrieval memory-verify"
```

Supported `SKILL_GROUP` values are `orchestrator`, `planner`, `context-builder`, `coder-1`, `coder-2`, `coder-3`, `code-reviewer`, `code-validator`, `memory-manager`, `git-committer`, and `all`.

Installed skills:

- `memory-retrieval` for agents allowed to retrieve compact memory briefs.
- `memory-write` for `memory-manager` entry creation.
- `memory-index-update` for `memory-manager` index regeneration.
- `memory-clean` for `memory-manager` maintenance, backups, deduplication, archiving, and superseding.
- `memory-verify` for `memory-manager` and `code-validator` integrity checks.

The role access matrix is documented in [Tooling and Agent Editing Specification](memory-tooling-and-agent-editing.md).

## Write

`memory-manager` creates entries through the write command:

```bash
agent-memory write --input new-memory.yaml
```

Example input:

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
  - src/auth/jwt.ts
retrieve_when:
  - login
  - JWT validation
  - dashboard authentication
```

The writer creates `entries/<id>.md`, updates `INDEX.md`, and verifies the store.

## Verify

```bash
agent-memory verify
agent-memory verify --json
```

Run verification after memory creation, cleanup, superseding, or archiving.

## Index Update

```bash
agent-memory index-update
```

Regenerates `INDEX.md` from active entries.

## Clean

Conservative cleanup operations:

```bash
agent-memory clean --find-duplicates
agent-memory clean --supersede old-auth-token-format --by auth-token-format-v2
agent-memory clean --archive old-auth-token-format --reason "promoted to docs"
```

Semantic merging is intentionally not automatic. The `memory-manager` decides merge policy; tools perform safe file operations.

## Backup

Create a timestamped backup archive before large cleanup or tool upgrades:

```bash
agent-memory backup
```

Choose an output path or directory:

```bash
agent-memory backup --output ~/backups/agent-memory-before-upgrade.tar.gz
agent-memory backup --output ~/backups/
```

See [Day-2 Operations](operations.md) for update and recovery workflows.
