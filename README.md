# Agent Memory Tools

Local, installable Markdown memory tools for coding agents.

The package installs one executable:

```bash
agent-memory
```

Source repository:

```text
https://codeberg.org/rch/agent-memory-tools.git
```

It manages a global memory directory with this shape:

```text
memory/
├── INDEX.md
├── README.md
├── entries/
└── archive/
```

## Install

Clone the repository first:

```bash
git clone https://codeberg.org/rch/agent-memory-tools.git
cd agent-memory-tools
```

Recommended Linux install from the checkout with `pipx`:

```bash
sudo apt install pipx
pipx ensurepath
make install
```

Restart your shell, or run:

```bash
source ~/.profile
```

Verify:

```bash
agent-memory --help
```

`pipx` is recommended because many Linux distributions mark system Python as externally managed under PEP 668. Avoid `pip --break-system-packages` unless you intentionally want to bypass that protection.

To install directly without `make`:

```bash
pipx install .
```

Alternative venv install:

```bash
python3 -m venv ~/.local/share/agent-memory-tools/venv
~/.local/share/agent-memory-tools/venv/bin/pip install .
ln -s ~/.local/share/agent-memory-tools/venv/bin/agent-memory ~/.local/bin/agent-memory
```

Development install from the cloned checkout:

```bash
make install-editable
```

Update an installed CLI from the same checkout:

```bash
git pull
make update
```

## Memory Directory

By default memory is stored at:

```text
~/.local/share/agent-memory-tools/memory
```

Override it globally:

```bash
export AGENT_MEMORY_DIR="$HOME/.agent-memory"
```

Or per command:

```bash
agent-memory --memory-dir /path/to/memory retrieve --query "auth token"
```

## Commands

Show project maintenance commands:

```bash
make help
```

Update the installed CLI from this checkout:

```bash
make update
```

Uninstall the CLI while keeping memory data untouched:

```bash
make uninstall
```

Pass a non-default memory directory to verification or backup targets:

```bash
make verify MEMORY_DIR=/path/to/memory
make backup MEMORY_DIR=/path/to/memory
```

## CLI Commands

Initialize memory:

```bash
agent-memory init
```

Retrieve relevant memories:

```bash
agent-memory retrieve --query "dashboard auth token" --project dashboard --tags auth,jwt
```

Create a memory from a structured file:

```bash
agent-memory write --input new-memory.yaml
```

Regenerate the index:

```bash
agent-memory index-update
```

Verify integrity:

```bash
agent-memory verify
```

Cleanup operations:

```bash
agent-memory clean --find-duplicates
agent-memory clean --supersede old-auth-token-format --by auth-token-format-v2
agent-memory clean --archive old-auth-token-format --reason "promoted to docs"
```

Back up memory data before upgrades or large cleanup:

```bash
agent-memory backup
```

## Write Input Format

`agent-memory write` accepts JSON, simple YAML, or a full Markdown memory file with frontmatter.

Example YAML:

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

## Agent Rules

- Coders use `retrieve` only.
- Memory summarizers use `write`, `index-update`, and `verify`.
- Memory cleaners use `clean`, `index-update`, and `verify`.
- Validators can use `retrieve` and `verify`.
- Tools perform file operations; agents make semantic decisions.

## Safety

The tools enforce:

- Kebab-case memory ids.
- Required frontmatter and summary.
- `importance` between `0` and `1`.
- Valid status values.
- No duplicate ids.
- Active entries listed in `INDEX.md`.
- Index rows point to existing files.
- Basic secret, prompt-injection, giant diff, and giant log checks.
- Atomic writes and a lock file around write/cleanup operations.

## Docs

- [Usage](docs/usage.md)
- [Day-2 Operations](docs/operations.md)
- [Memory System Specification](docs/memory-system-spec.md)
- [Tooling and Agent Editing Specification](docs/memory-tooling-and-agent-editing.md)
